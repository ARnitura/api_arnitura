# -*- coding: utf-8 -*-
import json
import sentry_sdk
from flask_cors import CORS, cross_origin
import sqlalchemy.exc
from flask import Flask, send_file, request, jsonify
from urllib.parse import urlparse, parse_qs
from data import db_session
from data.manufacturer import Manufacturer
from data.post import Post
from data.furniture import Furniture
from data.series import Series
from data.type_furniture import Type
from data.material import Material
from data.sort_furniture import Sort

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
application.config['JSON_AS_ASCII'] = False
from dadata import Dadata

db_session.global_init('db/furniture.db')


@application.route('/')
def main():
    return send_file('files/model.glb')


@application.route('/api/get_manufacturer', methods=['GET', 'POST'])  # Получение сущности производителя
def get_manufacturer():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Manufacturer).filter(Manufacturer.id == int(request.form.get('id'))).one()
        db_sess.close()
        return json.dumps({"avatar_photo": form.avatar_photo,
                           "name": form.name,
                           "count": form.count,
                           "address": form.address,
                           "mail": form.mail,
                           "phone_number": form.phone_number,
                           "site": form.site})


@application.route('/api/get_count_like',
                   methods=['GET', 'POST'])  # Получение лайков по айди записи
def get_count_like():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Post).filter(Post.id == request.form['id']).one()
        db_sess.close()
        return jsonify(count_likes=form.like_count)


@application.route('/api/download_app')
def download_app():
    return '''<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Redirect</title>
<script type="text/javascript"> // <![CDATA[
//iPhone Version:
if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i))) {
    window.location = "https://apps.apple.com/ru/app/kreslo/id1558098345";
}
//Android Version:
if(navigator.userAgent.match(/android/i)) {
    window.location = "https://play.google.com/store/apps/details?id=com.ThreeDStudio.Kreslo";
}
</script>
</body>
</html>'''


@application.route('/api/get_list_furniture',
                   methods=['GET', 'POST'])  # Метод получения списка состоящего из айди категорий фурнитуры
def get_list():
    if request.method == 'POST':
        list_furniture = {}
        db_sess = db_session.create_session()
        form = db_sess.query(Type).all()
        db_sess.close()
        for i in range(len(form)):
            list_furniture[str(i)] = ({'id': form[i].id, 'sort': form[i].type})
        print(list_furniture)
        return json.dumps(list_furniture)


@application.route('/api/get_sort_furniture', methods=['GET',
                                                       'POST'])  # Метод получения списка состоящего из айди определенной фурнитуры учитывая фильтр цены
def get_filter_list():
    if request.method == 'POST':
        list_furniture = {}
        db_sess = db_session.create_session()
        form = db_sess.query(Post).filter(Post.type_id == request.form.get('id'),
                                          Post.price >= float(request.form.get('filter_from')),
                                          Post.price <= float(request.form.get('filter_to'))).all()
        db_sess.close()
        for i in range(len(form)):
            list_furniture[str(i)] = ({'id': form[i].id, 'list_furniture': form[i].list_furniture,
                                       'photo': form[i].photo, 'post_name': form[i].post_name,
                                       'price': form[i].price})
        print(list_furniture)
        return json.dumps(list_furniture)


@application.route('/api/get_product_3_furniture', methods=['GET',
                                                            'POST'])
# Метод получения списка состоящего из айди каждого продукта с учетом фильтра цены
def get_product_list():
    if request.method == 'POST':
        count = 1
        list_furniture = {}
        db_sess = db_session.create_session()
        form = db_sess.query(Type).all()  # Получаем все типы товаров
        db_sess.close()
        for i in form:  # По каждому типу берем 3 продукта
            db_sess = db_session.create_session()
            product = db_sess.query(Furniture).filter(Furniture.type_furniture == i.id,
                                                      Furniture.price >= float(request.form.get('filter_from')),
                                                      Furniture.price <= float(
                                                          request.form.get('filter_to'))).all()
            # Получаем объекты мебели с учетом цены
            db_sess.close()
            list_furniture[count] = {}
            len_list = 3
            # Получаем все товары по айди с учетом фильтров
            if len(product) <= 3:
                len_list = len(product)
            for j in range(len_list):
                # Закидываем первые 3 товара каждого типа в список и возвращаем его
                if len(product) == 0:
                    list_furniture[count][j] = {}
                    break
                list_furniture[count][j] = {'id': product[j].id, 'manufacturer_id': product[j].manufacturer_id,
                                            'photo': product[j].photo_furniture, 'post_name': product[j].name,
                                            'price': product[j].price}
            count += 1
        return json.dumps(list_furniture)


@application.route('/api/get_posts',
                   methods=['GET', 'POST'])  # Метод получения списка категорий фурнитуры
def get_posts():
    global db_sess
    try:
        if request.method == 'POST':
            list_post = {}
            db_sess = db_session.create_session()
            form = db_sess.query(Post).all()
            db_sess.close()
            for i in range(len(form)):
                db_sess = db_session.create_session()
                res = db_sess.query(Furniture).filter(Furniture.id == form[i].id_furniture).first()
                db_sess.close()
                count_likes = len(form[i].list_likes.split(', '))
                list_post[str(i)] = ({"id": form[i].id,
                                      "manufacturer_id": form[i].manufacturer_id,
                                      "list_furniture": form[i].list_furniture,
                                      "photo": res.photo_furniture,
                                      "like_count": count_likes,
                                      "description": res.description,
                                      "price": res.price})
            print(list_post)
            return json.dumps(list_post)
    except sqlalchemy.exc.PendingRollbackError:
        db_sess.close()
        db_sess = db_session.create_session()


@application.route('/api/get_info_post',
                   methods=['GET', 'POST'])  # Метод получения списка категорий фурнитуры
def get_info_post():
    try:
        if request.method == 'POST':
            post_description = {}
            db_sess = db_session.create_session()
            post = db_sess.query(Post).filter(Post.id == request.form.get('id_post')).first()  # Пост
            sort = db_sess.query(Sort).filter(Sort.id == post.id_sort_furniture).first()
            series = db_sess.query(Series).filter(Series.id == post.id_series).first()  # Серия
            furniture = db_sess.query(Furniture).filter(Furniture.id == post.id_furniture).first()  # Объект мебели
            material = db_sess.query(Material).filter(Material.id == furniture.id_material).first()  # Материал
            db_sess.close()
            post_description['0'] = ({'series_furniture': series.name, 'description_furniture': furniture.description,
                                      'name_furniture': furniture.name,
                                      'material_furniture': material.name, 'sort_furniture': sort.sort,
                                      'width': furniture.width, 'length': furniture.length,
                                      'height': furniture.height, 'price_furniture': furniture.price})
            # Нужно передать: Серия(+), Sort(+), Описание(+), Материал(+), Размеры(ширина/длина/высота), цена
            print(post_description)
            return json.dumps(post_description)
    except sqlalchemy.exc.PendingRollbackError:
        db_sess.rollback()
        db_sess.close()


@application.route('/api/get_photo_avatar',
                   methods=['GET'])  # Метод получения автарки производителя
def get_photo_avatar():
    data = parse_qs(urlparse(request.url).query)
    return send_file('image/' + data.get('id')[0] + '/' + data.get('photo_name')[0] + '.png')


@application.route('/api/get_photos',
                   methods=['GET'])  # Метод получения фото товаров производителя
def get_photos():
    data = parse_qs(urlparse(request.url).query)
    return send_file('image/' + data.get('id')[0] + '/photos/' + data.get('photo_name')[0] + '.jpg')


@application.route('/api/get_list_photos',
                   methods=['GET', 'POST'])  # Метод получения cписка названий фото товаров производителя
def get_list_photos():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Post).filter(Post.manufacturer_id == request.form.get('id')).all()
        db_sess.close()
        list_furniture = {}
        for i in range(len(form)):
            db_sess = db_session.create_session()
            res = db_sess.query(Furniture).filter(Furniture.id == form[i].id_furniture).first()
            db_sess.close()
            list_furniture[str(i)] = ({'id': form[i].id, 'list_furniture': form[i].list_furniture,
                                       'photo': res.photo_furniture})
        return json.dumps(list_furniture)


@application.route('/api/get_list_photos_post',
                   methods=['GET', 'POST'])  # Метод получения cписка названий фото товаров производителя в посте
def get_list_photos_post():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Post).filter(Post.id == request.form.get('id')).all()
        db_sess.close()
        list_furniture = {}
        for i in range(len(form)):
            db_sess = db_session.create_session()
            res = db_sess.query(Furniture).filter(Furniture.id == form[i].id_furniture).first()
            db_sess.close()
            list_furniture[str(i)] = ({'id': form[i].id, 'list_furniture': form[i].list_furniture,
                                       'photo': res.photo_furniture})
        return json.dumps(list_furniture)


@application.route('/api/get_info_ip',
                   methods=['GET', 'POST'])  # Метод получения информации ип или ооо
@cross_origin()
def get_info_ip():
    if request.method == 'POST':
        list_info = {}
        dadata = Dadata("7c6d0539ad0f102c392688afa71c46f629cbc8ea")
        result = dadata.find_by_id("party", request.form.get('inn'))
        name = result[0]["value"]  # Наименование
        if "management" in result[0]["data"]:
            print("ООО")
            print(result[0]["data"]["management"]["name"],
                  result[0]["data"]["management"]["post"])  # Руководитель и должность (большой) (7812014560)
        else:
            print("ИП")
            print(result[0]["data"]["fio"]["surname"], result[0]["data"]["fio"]["name"],
                  result[0]["data"]["fio"]["patronymic"])  # Руководитель и должность (малый) (644802061247)
        print(result[0]["data"]["address"]["value"])  # Адресс
        list_info[0] = ({'name': name, 'manager': '1', 'mark': '1', 'address': 'адрес'})
        # Имя: name, Менеджер: manager, Торговая марка: mark, Адрес: address
        return json.dumps(list_info)


if __name__ == '__main__':
    sentry_sdk.init(
        "https://54b0b37c37764ef9b81a6b1717fa4839@o402412.ingest.sentry.io/6192564",
        traces_sample_rate=1.0
    )
    application.run(host='0.0.0.0', port=5001, debug=True)
