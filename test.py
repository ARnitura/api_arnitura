import requests
import json
#
# print(requests.post(url='https://arkreslo.ru/api/get_posts').text)
# print(requests.post(url='https://arkreslo.ru/api/get_product_3_furniture', data={'filter_from': '0',
#                                                                                      'filter_to': '100000',
#                                                                                      'id': 1}).text)
#  print(requests.post(url='http://192.168.0.5:5001/api/get_manufacturer', data={'id': 2}).text)  # Тест получения сущности продавца
#  print(requests.post(url='http://192.168.0.5:5001/api/get_count_like', data={'id': 3}).text)  # Тест на получение лайков записи
#  print(requests.post(url='https://arkreslo.ru/api/get_list_furniture', data={'id': 3}).text)
#  print(requests.post(url='http://192.168.166.118:5001/api/get_product_3_furniture', data={'filter_from': '0',
#                                                                                      'filter_to': '100000',
#                                                                                      'id': 1}).text)
# print(requests.get(url='http://192.168.0.5:5001/api/get_photos?id=2&photo_name=image_company').text)
print(requests.post(url='http://192.168.0.108:5001/api/get_info_ip', data={'inn': 7812014560}).json()['0'])
