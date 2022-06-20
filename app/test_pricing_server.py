import requests
# import unittest
import datetime as dt


print(dt.datetime.now())

response = requests.get('http://127.0.0.1:8080/users/measdf')

print(f'{response.status_code=}')
print(f'{response.text=}')
assert(response.ok is True, 'response is not OK')

print(dt.datetime.now())