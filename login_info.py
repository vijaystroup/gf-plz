import os
from json import loads

path = os.path.dirname(__file__)

with open(f'{path}/creds.json', mode='r') as f:
    data = loads(f.read())
    username = data['username']
    password = data['password']
