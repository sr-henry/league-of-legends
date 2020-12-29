import json
import requests

## https://developer.riotgames.com/docs/lol

base = 'https://127.0.0.1:2999/liveclientdata/'

certificate = 'riotgames.pem'

def playername():
    response = requests.get(base + 'activeplayername', verify=certificate)
    return json.loads(response.content.decode('utf-8'))


def activeplayer():
    response = requests.get(base + 'activeplayer', verify=certificate)
    return json.loads(response.content.decode('utf-8'))

def playerlist():
    response = requests.get(base + 'playerlist', verify=certificate)
    return json.loads(response.content.decode('utf-8'))
