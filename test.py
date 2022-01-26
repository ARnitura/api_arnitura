import requests

print(requests.post(url='http://192.168.0.5:5001/api/get_manufacturer', data={'id': 1}).text)
print(requests.post(url='http://192.168.0.5:5001/api/get_count_like', data={'id': 1}).text)