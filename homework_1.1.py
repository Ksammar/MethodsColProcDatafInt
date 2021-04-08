# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json;
# написать функцию, возвращающую список репозиториев.
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_repo(nameuser):
    repos = requests.get('https://api.github.com/users/' + nameuser + '/repos')
    if repos.status_code == 200:
        return repos


user = os.getenv("user_github", None)
token = os.getenv("token_repo", None)
url = 'https://api.github.com/user/repos'
r = requests.get(url, auth=(user, token))
repos = requests.get(url, auth=(user, token))
print(r)
repos.json()[1]
if repos.status_code == 200:
    path = 'user_repos.json'
    with open(path, 'w') as f:
        json.dump(repos.json(), f)
for repo in repos.json():
    print(repo['html_url'])

# username = input("Enter the github username:")
username = "Konstantin-Buzuev"
path = 'user_repos2.json'
repos = get_repo(username)
repos.json()[1]
with open(path, 'w') as f:
    json.dump(repos.json(), f)
for repo in repos.json():
    print(repo['html_url'])
