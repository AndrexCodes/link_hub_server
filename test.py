import json
config = {
    'Authorization': 'ef8y72cho837hc43874cowuhxo87hecx298302983e94232dhowiucxw',
    "LinkHubId": "",
    'LinkHubName': "First LinkHub"
}

with open('config.json', 'w') as file:
    file.write(json.dumps(config))
    file.close()