# -*- coding: utf-8 -*-
import json
import smtplib

import sentry_sdk
import pymorphy2
import datetime
import os
from flask_cors import CORS, cross_origin
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlalchemy.exc
from flask import Flask, send_file, request, render_template
from urllib.parse import urlparse, parse_qs
from data import db_session
from data.manufacturer import Manufacturer
from data.order import Order
from data.post import Post
from data.furniture import Furniture
from data.series import Series
from data.type_furniture import Type
from data.material import Material
from data.sort_furniture import Sort
from data.user import User

application = Flask(__name__)
morph = pymorphy2.MorphAnalyzer()
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
application.config['JSON_AS_ASCII'] = False
from dadata import Dadata

db_session.global_init('db/furniture.db')

@application.route('/')
def main():
    return 'ARnitura'


@application.route('/api/get_manufacturer', methods=['GET', 'POST'])  # Получение сущности производителя
def get_manufacturer():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Manufacturer).filter(Manufacturer.id == int(request.form.get('id'))).one()
        db_sess.close()
        return json.dumps({"avatar_photo": form.avatar_photo,
                           "name": form.name,
                           "address": form.address,
                           "mail": form.mail,
                           "phone_number": form.phone_number,
                           "site": form.site,
                           })


@application.route('/api/maps_info', methods=['GET', 'POST'])  # Получение информации о количестве карт для материала
def maps_info():
    if request.method == 'POST':
        onlyfiles = [f for f in os.listdir(os.getcwd() + '/image/manufacturers/' + request.form.get('id_manufacturer') +
                                           '/models/textures/' + request.form.get('id_texture') + '/')]
        return json.dumps({'maps': ', '.join(onlyfiles)})


@application.route('/api/get_counts_manufacturer', methods=['GET', 'POST'])  # Получение счетчиков производителей
def get_counts_manufacturer():
    if request.method == 'POST':
        likes_count = 0
        db_sess = db_session.create_session()
        form = db_sess.query(Manufacturer).filter(Manufacturer.id == int(request.form.get('id_manufacturer'))).one()
        toLikes = db_sess.query(Post).filter(Post.manufacturer_id == int(request.form.get('id_manufacturer'))).all()
        for post in toLikes:
            likes_count += len(post.list_likes.split(','))
        # Количество лайков, чтобы посчитать нужно получить все посты этого производителя и получить кол-во через split()
        list_favourites = form.list_favourites  # Количество добавленных в избранное, считается когда пользователь добавляет у себя на устройстве в избранное
        list_products = len(toLikes)  # Количество товаров = количество постов
        list_orders = form.list_orders  # Количество заказов
        db_sess.close()
        return json.dumps({'likes_count': likes_count, 'list_favourites': list_favourites,
                           'list_products': list_products, 'list_orders': list_orders})


@application.route('/api/get_count_like',
                   methods=['GET', 'POST'])  # Получение лайков по айди записи
def get_count_like():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Post).filter(Post.id == request.form['id_post']).one()
        db_sess.close()
        count_likes = len(form.list_likes.split(', '))
        return json.dumps({'count_likes': count_likes})


@application.route('/api/put_like',
                   methods=['GET', 'POST'])  # Поставить лайк
def put_like():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(Post).filter(Post.id == request.form['id_post']).one()
        if request.form['id_user'] not in form.list_likes.split(', '):
            form.list_likes = form.list_likes + ', ' + request.form['id_user']
            count_likes = len(form.list_likes.split(', '))
            db_sess.commit()
            db_sess.close()
            return json.dumps({'description': 'success',
                               'count_likes': count_likes}), 200  # Возвращаем 200 если все хорошо и пользователь ставит лайк
        else:
            list_likes = form.list_likes.split(', ')
            index_to_del = form.list_likes.split(', ').index(request.form['id_user'])
            list_likes.pop(index_to_del)
            form.list_likes = ', '.join(list_likes)
            db_sess.commit()
            count_likes = len(form.list_likes.split(', '))
            db_sess.close()
            return json.dumps({'description': 'cancelled',
                               'count_likes': count_likes}), 409  # Возвращаем 409 если пользователь уже ставил лайк на эту запись


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
                if form[i].list_likes is not None:
                    count_likes = len(form[i].list_likes.split(', '))
                else:
                    count_likes = 0
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
                   methods=['GET', 'POST'])  # Метод получения информации о посте
def get_info_post():  # TODO: Почистить код обработки времени
    try:
        if request.method == 'POST':
            post_description = {}
            db_sess = db_session.create_session()
            post = db_sess.query(Post).filter(Post.id == request.form.get('id_post')).first()  # Пост
            manufacturer_name = db_sess.query(Manufacturer).filter(Manufacturer.id == post.manufacturer_id).first().name
            sort = db_sess.query(Sort).filter(Sort.id == post.id_sort_furniture).first()
            series = db_sess.query(Series).filter(Series.id == post.id_series).first()  # Серия
            furniture = db_sess.query(Furniture).filter(Furniture.id == post.id_furniture).first()  # Объект мебели
            model_id = furniture.model  # id модели(для импорта в ар)
            material_id = furniture.id_material  # id Материалов
            material_name = []  # Названия материалов
            for material in material_id.split(' '):
                material_name.append(db_sess.query(Material).filter(Material.id == material).first().name)
            data_publication = post.data_publication
            time_publication = post.time_publication
            db_sess.close()
            diff = datetime.datetime.today() - datetime.datetime.strptime(data_publication + ' ' + time_publication,
                                                                          '%d.%m.%y %H:%M')  # Вычитаем даты и получаем разницу в минутах
            time = diff.seconds + (86400 * diff.days)
            if time <= 60:  # Секунды
                seconds = morph.parse('Cекунда')[0]
                post_time = str(time) + ' ' + seconds.make_agree_with_number(int(str(time)[-1])).word + ' назад'
            elif 1 <= time // 60 <= 60:  # Минуты
                minutes = morph.parse('Минута')[0]
                post_time = str(time // 60) + ' ' + minutes.make_agree_with_number(
                    int(str(time // 60)[-1])).word + ' назад'
            elif 1 <= time // 60 // 60 < 24:  # Часы
                hour = morph.parse('Час')[0]
                post_time = str(time // 60 // 60) + ' ' + hour.make_agree_with_number(
                    int(str(time // 60 // 60))).word + ' назад'
            elif 1 <= time // 60 // 60 // 24:  # Дни
                hour = morph.parse('День')[0]
                post_time = str(time // 60 // 60 // 24) + ' ' + hour.make_agree_with_number(
                    int(str(time // 60 // 60 // 24))).word + ' назад'
            post_description['0'] = ({'series_furniture': series.name, 'description_furniture': furniture.description,
                                      'name_furniture': furniture.name,
                                      'material_id_furniture': material_id,
                                      'material_name_furniture': ', '.join(material_name),
                                      'sort_furniture': sort.sort,
                                      'width': furniture.width, 'length': furniture.length,
                                      'height': furniture.height, 'price_furniture': furniture.price,
                                      'post_time': post_time, 'manufacturer_id': post.manufacturer_id,
                                      'avatar_furniture': furniture.photo_furniture, 'model_id': model_id,
                                      'manufacturer_name': manufacturer_name})
            # Отдается: Название серии, Описание поста, название мебели, id материалов, название материалов,
            # название категории, ширина, длина, высота, цена мебели, время создания поста, id производителя,
            # аватара производителя, id модели мебели
            return json.dumps(post_description)
    except sqlalchemy.exc.PendingRollbackError:
        db_sess.rollback()
        db_sess.close()


@application.route('/api/get_photo_texture',
                   methods=['GET'])  # Метод получения аватарки материала
def get_photo_texture():
    data = parse_qs(urlparse(request.url).query)
    db_sess = db_session.create_session()
    form = db_sess.query(Post).where(Post.id == data.get('post_id')[0]).first()
    db_sess.close()
    onlyfiles = [f for f in os.listdir(os.getcwd() + '/image/manufacturers/' + str(form.manufacturer_id) +
                                       '/models/textures/' + data.get('texture_id')[0] + '/')]
    for files in onlyfiles:
        if 'basecolor' in files.lower():
            return send_file(os.getcwd() + '/image/manufacturers/' + str(form.manufacturer_id) + '/models/textures/' +
                             data.get('texture_id')[0] + '/' + files)


@application.route('/api/get_photo_avatar',
                   methods=['GET'])  # Метод получения аватарки производителя
def get_photo_avatar():
    data = parse_qs(urlparse(request.url).query)
    return send_file('image/manufacturers/' + data.get('id')[0] + '/' + data.get('photo_name')[0] + '.png')


@application.route('/api/set_user_avatar', methods=['GET', 'POST'])  # Изменение аватарки пользователя
def set_user_avatar():
    if request.method == 'POST':
        if not os.path.isdir(os.getcwd() + '/image/users/' + request.form.get('user_id')):
            os.makedirs(os.getcwd() + '/image/users/' + request.form.get('user_id'))
        onlyfiles = [f for f in os.listdir(os.getcwd() + '/image/users/' + request.form.get('user_id') + '/')]
        for i in onlyfiles:
            if 'avatar' in i:
                try:
                    os.remove(path=os.getcwd() + '/image/users/' + request.form.get('user_id') + '/' + str(i))
                except FileNotFoundError:
                    continue
        uploaded_file = request.files['file_field']
        if uploaded_file.filename != '':
            uploaded_file.save(
                'image/users/' + request.form.get('user_id') + '/' + 'avatar.' + uploaded_file.filename.split('.')[-1])
        return json.dumps({'status': 200})


@application.route('/api/get_photos',
                   methods=['GET'])  # Метод получения фото товаров производителя
def get_photos():
    data = parse_qs(urlparse(request.url).query)
    return send_file('image/manufacturers/' + data.get('id')[0] + '/photos/' + data.get('photo_name')[0] + '.jpg')


@application.route('/api/get_list_photos',
                   methods=['GET', 'POST'])  # Метод получения списка названий фото товаров производителя
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
                   methods=['GET', 'POST'])  # Метод получения списка названий фото товаров производителя в посте
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
        print(result[0]["data"]["address"]["value"])  # Адрес
        list_info[0] = ({'name': name, 'manager': '3', 'mark': '3', 'address': 'адрес'})
        # Имя: name, Менеджер: manager, Торговая марка: mark, Адрес: address
        return json.dumps(list_info)


@application.route('/api/auth_user',
                   methods=['GET', 'POST'])  # Авторизация пользователя
def auth_user():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        form = db_sess.query(User).filter(User.login == request.form.get('login'),
                                          User.password == request.form.get('password')).first()
        #  Вытягиваем запись авторизируемого пользователя
        db_sess.close()
        if form is None:
            return json.dumps({'error': 'No found user'}), 400
        else:
            list_furniture = {}
            list_furniture[str(0)] = ({
                'id': form.id,
                'firstname': form.firstname, 'lastname': form.lastname,
                'patronymic': form.patronymic, 'avatar': form.avatar,
                'phone': form.phone, 'mail': form.mail,
                'address': form.address, 'login': form.login,
                'list_favourites': form.list_favourites, 'list_orders': form.list_orders})
            return json.dumps(list_furniture)


@application.route('/api/reg_manufacturer',
                   methods=['GET', 'POST'])  # Регистрация производителя на сайте
def reg_manufacturer():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        date = datetime.datetime.now().date().strftime('%d.%m.%y')
        time = datetime.datetime.now().time().strftime('%H:%M')
        new_manufacturer = Manufacturer(inn=request.form.get('inn'), name=request.form.get('name'),
                                        password=request.form.get('password'),
                                        address=request.form.get('address'),
                                        data_reg=date, time_reg=time)
        db_sess.add(new_manufacturer)
        db_sess.commit()
        last_id = db_sess.query(Manufacturer).order_by(Manufacturer.id)[-1].id
        #  Регистрируем производителя и получаем его айди
        db_sess.close()
        return json.dumps({'description': 'success', 'id': str(last_id)}), 200


@application.route('/api/get_photo_user_avatar',  # Получение аватарки пользователя
                   methods=['GET', 'POST'])
def get_photo_user_avatar():
    data = parse_qs(urlparse(request.url).query)
    onlyfiles = [f for f in os.listdir(os.getcwd() + '/image/users/' + data['user_id'][0] + '/')]
    for i in onlyfiles:
        if 'avatar' in i:
            return send_file('image/users/' + data.get('user_id')[0] + '/' + i)
    # Сделать доступной аватарки с учетом разрешения
    return json.dumps({'status': '404'})


@application.route('/api/get_state_like',
                   methods=['GET', 'POST'])  # Получение состояния лайка на посте
def get_state_like():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        res = db_sess.query(Post).filter(Post.id == request.form.get('id_post')).first()
        db_sess.close()
        if request.form.get('id_user') in res.list_likes.split(', '):
            return json.dumps({'state': 'on'}), 200
        else:
            return json.dumps({'state': 'off'}), 400


@application.route('/api/edit_info_user',
                   methods=['GET', 'POST'])  # Редактирование информации о пользователе
def edit_info_user():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        res = db_sess.query(User).filter(User.id == request.form.get('user_id')).first()
        res.phone = request.form.get('number')
        res.mail = request.form.get('mail')
        res.address = request.form.get('address')
        db_sess.commit()
        db_sess.close()
        return json.dumps({'description': 'success'}), 200


@application.route('/api/edit_fullname_user',
                   methods=['GET', 'POST'])  # Редактирование имени пользователя
def edit_fullname_user():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        res = db_sess.query(User).filter(User.id == request.form.get('user_id')).first()
        res.lastname = request.form.get('lastname')
        res.firstname = request.form.get('firstname')
        res.patronymic = request.form.get('patronymic')
        db_sess.commit()
        db_sess.close()
        return json.dumps({'description': 'success'}), 200


@application.route('/api/download_model',
                   methods=['GET', 'POST'])  # Скачивание модели
def download_model():
    if request.method == 'GET':
        data = parse_qs(urlparse(request.url).query)
        path = 'image/manufacturers/' + data.get('manufacturer_id')[0] + '/models/' + data.get('model_id')[0] + '.fbx'
        return send_file(path)


@application.route('/api/download_texture',
                   methods=['GET', 'POST'])  # Скачивание текстуры
def download_texture():
    if request.method == 'GET':
        data = parse_qs(urlparse(request.url).query)
        path = 'image/manufacturers/' + data.get('manufacturer_id')[0] + '/models/textures/' + data.get('texture_id')[0] \
               + '/' + data.get('selected_texture')[0]
        return send_file(path)


@application.route('/api/new_order', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        try:
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            patronymic = request.form.get('patronymic')
            mail = request.form.get('mail')
            phone = request.form.get('phone')
            address = request.form.get('address')
            json_order = request.form.get('listToBuy')
            name = f"{lastname} {firstname} {patronymic}"
            # Данные с формы

            fromaddr = "info@arnitura.ru"  # Отправитель
            toaddr = request.form.get('mail')  # Адресат
            mypass = "maqpyn-nyhbaf-3sEfwe"  # Пароль от кабинета отправителя

            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = phone

            html = """<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
        <title>Заказ Arnitura</title>
    </head>
    <body>
    <div class="constraint text">
        Заказ №
        <label class="holder">
            <input class="input_radius" disabled type="text">
        </label>
    </div>
    <div class="constraint text">
        Дата заказа
        <label class="holder">
            <input class="input_radius" disabled type="text">
        </label>
    </div>
    <div class="constraint text">
        Адрес доставки<br/>
        <label>
            <input class="indent" disabled type="text"><br/>
        </label>
    </div>
    <div class="constraint text">
        Контактные данные<br/>
        <label>
            <input class="indent" disabled placeholder="ФИО" type="text"><br/>
            <input class="indent" disabled placeholder="Тел." type="text"><br/>
            <input class="indent" disabled placeholder="E-mail" type="text">
        </label>
    </div>
    <div class="constraint text" style="margin-top: 50px; text-align: center;">
        Товары
    </div>
    <div style="display: flex; flex-direction: row;">
        <div class="text" style="display: flex; align-items: center; margin-right: 10px;">1</div>
        <div style="display: flex; width: 100%; flex-direction: column; border: 1px solid rgba(0, 0, 0, 0.5);
            border-radius: 7px;">
            <div class="order_cell">
                <div class="info_cell text">Тип
                    <input class="indent" disabled placeholder="" type="text">
                </div>
                <div class="info_cell text">Наименование
                    <input class="indent" disabled placeholder="" type="text">
                </div>
                <div class="info_cell text">Цвет
                    <input class="indent" disabled placeholder="" type="text">
                </div>
                <div class="info_cell text">Материал
                    <input class="indent" disabled placeholder="" type="text">
                </div>
            </div>
            <div class="text" style="margin-right: 10px; margin-bottom:20px; text-align: right">
                <input class="input_radius" disabled placeholder="" type="text">
                2000 руб
            </div>
        </div>
    </div>
    <div class="constraint6">
        <p class="text">Итого:</p>
        <button><p class="text_button">Оплатить</p></button>
    </div>
    </body>
    <style>
    
        .text {
            font-family: 'Inter', sans-serif;
            font-style: normal;
            font-weight: 400;
            font-size: 15px;
            line-height: 18px;
            color: #000000;
        }
    
        .info_cell {
            display: flex;
            flex-direction: column;
            width: 100%;
        }
    
        .order_cell {
            padding: 30px;
            display: flex;
            flex-direction: row;
            margin: 0 10px;
            width: 100%;
        }
    
        .constraint {
            margin-left: 5%;
        }
    
        .holder {
            margin-top: 1em;
            margin-left: 1em;
        }
    
        .input_radius {
            margin: 3px;
            width: 80px;
            height: 15px;
            border: 1px solid rgba(0, 0, 0, 0.5);
            border-radius: 7px;
        }
    
        .indent {
            width: 277px;
            height: 15px;
            margin: 3px;
            border: 1px solid rgba(0, 0, 0, 0.5);
            border-radius: 7px;
        }
    
        .constraint6 {
            float: right;
        }
    
        .text_button {
            font-family: 'Inter', sans-serif;
            font-style: normal;
            font-weight: 600;
            font-size: 20px;
            line-height: 24px;
            display: contents;
            color: #FFFFFF;
        }
    
        button {
            background: rgba(0, 148, 255, 0.75);
            border-radius: 7px;
            width: 153px;
            height: 37px;
            border: 0;
        }
    
    
    
        ::placeholder {
            font-family: 'Inter', sans-serif;
            font-style: normal;
            font-weight: 300;
            font-size: 13px;
            line-height: 16px;
            padding-left: 2%;
    
            color: rgba(0, 0, 0, 0.45);
        }
    
    </style>
    </html>"""
            msg.attach(MIMEText(html, 'html'))
            text = msg.as_string()
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(fromaddr, mypass)
            server.sendmail(fromaddr, toaddr, text)

            db_sess = db_session.create_session()
            new_order_db = Order(name=name, phone=phone, mail=mail, address=address, json_order=json_order)
            db_sess.add(new_order_db)
            db_sess.commit()
            db_sess.close()
            return json.dumps({'status': 200})
        except smtplib.SMTPRecipientsRefused:
            return json.dumps({'status': 501})


@application.route('/privacypolicy')
def privacy():
    with open('templates/document/privacy.txt', 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    sentry_sdk.init(
        "https://54b0b37c37764ef9b81a6b1717fa4839@o402412.ingest.sentry.io/6192564",
        traces_sample_rate=1.0
    )
    application.run(host='0.0.0.0', port=5003, debug=True)
