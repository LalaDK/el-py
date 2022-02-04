import json
import requests

cookieJar = None
baseUrl = "https://www.ok.dk/"


def initialize():
    global cookieJar
    req = requests.get(baseUrl)
    cookieJar = req.cookies


def authorize(email, password):
    global cookieJar
    data = json.dumps({
            "values": {
                "email": email,
                "password": password,
                "persists": "true"
            }
            })
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(data))
               }
    url = f'{baseUrl}min-ok-forside/login/authenticate'
    req = requests.post(url, cookies=cookieJar, data=data, headers=headers)
    cookieJar = req.cookies


def fetchData(aftalenr, fra, til):
    global cookieJar
    url = (baseUrl
           + "min-ok-forside/el-overblik/forbrug/downloadrawdata?"
           + "aftalenr=" + aftalenr
           + "&fra=" + fra
           + "&til=" + til)

    req = requests.post(url, cookies=cookieJar)
    return req.text
