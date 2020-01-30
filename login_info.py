from json import loads
from os import path

cwd = path.dirname(path.realpath(__file__))

with open(f'{cwd}/creds.json', mode='r') as f:
    data = loads(f.read())
    username = data['username']
    password = data['password']
