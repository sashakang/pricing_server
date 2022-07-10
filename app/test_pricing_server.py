import requests
# import unittest
from datetime import datetime as dt


print(dt.now())

response = requests.get('http://127.0.0.1:8000/users/measdf')

print(f'{response.status_code=}')
print(f'{response.text=}')
# assert(response.ok is True, 'response is not OK')

response = requests.put('http://127.0.0.1:8000/put/items/test_name')

print(f'{response.status_code=}')
print(f'{response.text=}')
# assert(response.ok is True, 'response is not OK')

response = requests.get('http://127.0.0.1:8000/ping')

print(f'{response.status_code=}')
print(f'{response.text=}')

response = requests.get('http://127.0.0.1:8000/test')

print(f'{response.status_code=}')
print(f'{response.text=}')

print(dt.now())