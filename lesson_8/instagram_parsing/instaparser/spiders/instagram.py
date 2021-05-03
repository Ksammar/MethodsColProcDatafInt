import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import quote
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    username = "miste65536"
    enc_password = "#PWD_INSTAGRAM_BROWSER:10:1619973187:Ad1QAFVajExW1nrMwam1xfAJ+HbF4d1OOsIj0pi0imeqU5hi/EhdERgRDtT8YO+cQWKX/aNV4weRBvn8WIzoEua0micpRNamyVFqFicRqFGeS6hXL3L+Bgjz897c9vc+yPycNnrdmsQtasBEDA=="
    user_to_parse_url_template = "/%s"
    user_to_parse = "ai_machine_learning"
    posts_hash = "32b14723a678bd4628d70c1f877b94c9"
    follow_hash = {'followers': "5aefa9893005572d237da5068082d8d5",
    'followings': "3dec7e2c57367ef3da3d987d89f9dbc8"}
    variabls_follow = ['followers', 'followings']
    user_hash = "d4d88dc1500312af6f937f7b804c68c3"
    user_variables = {"user_id": "0"}
    followers = []

    follow_variables = {
        'first': 24,
        'id': "30859820772"
    }
    graphql_url = "https://www.instagram.com/graphql/query/?"
    def __init__(self, search):
        super().__init__()
        self.user_to_parse = search

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.user_login,
            formdata={
                "username": self.username,
                "enc_password": self.enc_password
            },
            headers={
                'x-csrftoken': csrf_token
            }
        )

    def user_login(self, response: HtmlResponse):
        data = response.json()
        if data['authenticated']:
            for user in self.user_to_parse:
                yield response.follow(
                    self.user_to_parse_url_template % user,
                    callback=self.user_data_parse,
                    cb_kwargs={
                        "username": user,
                    }
                )

    def make_str_variables(self, variables):
        str_variables = quote(
            str(variables).replace(" ", "").replace("'", '"')
        )
        return str_variables

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        self.follow_variables['id'] = user_id
        variables = deepcopy(self.follow_variables)
        str_variables = self.make_str_variables(variables)
        for i, f_hash in enumerate(self.variabls_follow):
            url = f"{self.graphql_url}query_hash={self.follow_hash[f_hash[i]]}&variables={str_variables}"
            yield response.follow(
                url,
                callback=self.user_follow_parse,
                cb_kwargs={
                    "username": username,
                    "variables": deepcopy(variables),
                    "options": i
                }
            )

    def user_post_parse(self, response: HtmlResponse, username, user_id, variables):
        print()

        data = response.json()
        # наиболее предпочтительный вариант
        # try:
        info = data["data"]["user"]['edge_owner_to_timeline_media']
        # posts = info['edges']
        # работа с постами
        # for post in posts:
        #     item = InstaparserItem()
        #     item['user_id'] = user_id
        #     node = post['node']
        #     item['photo'] = node["display_url"]
        #     item['likes'] = node['edge_media_preview_like']['count']
        #     item['post_data'] = node
        #     yield item

        page_info = info['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            str_variables = self.make_str_variables(variables)
            url = f"{self.graphql_url}query_hash={self.posts_hash}&variables={str_variables}"
            yield response.follow(
                url,
                callback=self.user_post_parse,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    # на будущее: изучите в чем отличие глубокого копирования
                    "variables": deepcopy(variables),
                }
            )

    def user_follow_parse(self, response: HtmlResponse, username, variables, options):
        print()
        data = response.json()
        try:
            if options == 0:
                info = data["data"]["user"]['edge_followed_by']
            elif options == 1:
                info = data["data"]["user"]['edge_followed_by']
            following = info['edges']
            for follow in following:
                item = InstaparserItem()
                node = follow['node']
                item['_id'] = node["id"]
                item['photo'] = node["profile_pic_url"]
                item['name'] = node["full_name"]
                item['username'] = node["username"]
                item['following'] = variables["id"]
                yield item
        except Exception as e:
            print(e)
        page_info = info['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            str_variables = self.make_str_variables(variables)
            url = f"{self.graphql_url}query_hash={self.follow_hash[self.variabls_follow[options]]}&variables={str_variables}"
            yield response.follow(
                url,
                callback=self.user_followers_parse,
                cb_kwargs={
                    "username": username,
                    "variables": deepcopy(variables),
                    "options": options
                }
            )

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
