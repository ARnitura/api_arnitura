import requests
import json
#
print(requests.post(url='http://31.31.198.122:5000/api/get_photo_texture', headers={'texture_id': '1'}).text)
print(requests.post(url='https://arkreslo.ru/api/get_counts_manufacturer', data={'id_manufacturer': '2'}).text)
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
# print(requests.post(url='https://arkreslo.ru/api/get_info_ip', data={'inn': 7812014560}).json())
# print(requests.post(url='http://192.168.0.108:5001/api/get_info_post', data={'id_post': 8}).json())



# print(requests.get(url='https://1c.surpk.ru/schedule/api/weeks/date/2022-03-13').text)
# request = requests.get(url='https://1c.surpk.ru/schedule/api/lessons/week/621bd04ca7878823a02a0f2b').json()
# for object_schedule in request:
#     if object_schedule['group']['name'] == '015':
#         print(object_schedule['subject']['name'])
