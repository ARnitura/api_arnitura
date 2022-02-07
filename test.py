import requests
import json

#  print(requests.post(url='http://192.168.0.5:5001/api/get_manufacturer', data={'id': 1}).text)  # Тест получения сущности продавца
#  print(requests.post(url='http://192.168.0.5:5001/api/get_count_like', data={'id': 1}).text)  # Тест на получение лайков записи
print(requests.post(url='https://apikreslo.herokuapp.com/api/get_list_furniture').text)