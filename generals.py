from datetime import datetime
import requests
import threading
import time
import json

cpanel_server = ""
config = {
    'Authorization': 'ef8y72cho837hc43874cowuhxo87hecx298302983e94232dhowiucxw',
    "LinkHubId": id,
    'LinkHubName': "First LinkHub"
}

def setHubConfig(config: object):
    with open('config.json', 'w') as file:
        file.write(json.dumps(config))
        file.close()

def getHubConfig():
    with open('config.json', 'r') as file:
        data = json.loads(file.read())
        return data

def ExtractTime(user_time=None):
    d = datetime.strptime(user_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return [d.hour, d.minute]

def pingServer():
    # while True:
    #     response = requests.get(cpanel_server, headers=getHubConfig())
    #     response = json.loads(response.text)
    #     setHubConfig(config=response)
    #     time.sleep(5*60*60) # Ping Every 5 Hours
    pass

x = threading.Thread(target=pingServer)
x.start()