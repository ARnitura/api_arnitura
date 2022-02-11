import json
import sentry_sdk
import sqlalchemy.exc
from flask import Flask, send_file, request, jsonify
from urllib.parse import urlparse, parse_qs
from data import db_session
from data.manufacturer import Manufacturer
from data.post import Post
from data.type_furniture import Type

application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False

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
            product = db_sess.query(Post).filter(Post.type_id == i.id,
                                                 Post.price >= float(request.form.get('filter_from')),
                                                 Post.price <= float(request.form.get('filter_to'))).all()
            db_sess.close()
            list_furniture[count] = {}
            len_list = 3
            # Получаем все товары по айди с учетом фильтров
            if len(product) <= 3:
                len_list = len(product)
            for j in range(len_list):  # Закидываем первые 3 товара каждого типа в список и возвращаем его
                if len(product) == 0:
                    list_furniture[count][j] = {}
                    break
                list_furniture[count][j] = {'id': product[j].id, 'list_furniture': product[j].list_furniture,
                                            'photo': product[j].photo, 'post_name': product[j].post_name,
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
                list_post[str(i)] = ({"id": form[i].id,
                                      "type_id": form[i].type_id,
                                      "manufacturer_id": form[i].manufacturer_id,
                                      "list_furniture": form[i].list_furniture,
                                      "photo": form[i].photo,
                                      "post_name": form[i].post_name,
                                      "like_count": form[i].like_count,
                                      "favourites_count": form[i].favourites_count,
                                      "description": form[i].description,
                                      # size: form[i].id,
                                      "width": form[i].width,
                                      "length": form[i].length,
                                      "height": form[i].height,
                                      "price": form[i].price})
            print(list_post)
            return json.dumps(list_post)
    except sqlalchemy.exc.PendingRollbackError:
        db_sess.close()
        db_sess = db_session.create_session()


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
            list_furniture[str(i)] = ({'id': form[i].id, 'list_furniture': form[i].list_furniture,
                                       'photo': form[i].photo})
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
            list_furniture[str(i)] = ({'id': form[i].id, 'list_furniture': form[i].list_furniture,
                                       'photo': form[i].photo})
        return json.dumps(list_furniture)


if __name__ == '__main__':
    sentry_sdk.init(
        "https://54b0b37c37764ef9b81a6b1717fa4839@o402412.ingest.sentry.io/6192564",
        traces_sample_rate=1.0
    )
    application.run(host='0.0.0.0', port=5001)

