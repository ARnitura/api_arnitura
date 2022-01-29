from flask import Flask, send_file, request, jsonify

from data import db_session
from data.manufacturer import Manufacturer
from data.post import Post

application = Flask(__name__)


@application.route('/')
def main():
    return send_file('files/model.glb')


@application.route('/api/get_manufacturer',
                   methods=['GET', 'POST'])  # Получение сущности производителя
def get_manufacturer():
    if request.method == 'POST':
        form = db_sess.query(Manufacturer).filter(Manufacturer.id == request.form['id']).one()
        return jsonify(avatar_photo=form.avatar_photo,
                       name=form.name,
                       count=form.count,
                       address=form.address,
                       mail=form.mail,
                       phone_number=form.phone_number,
                       site=form.site)


@application.route('/api/get_count_like',
                   methods=['GET', 'POST'])  # Получение лайков по айди записи
def get_count_like():
    if request.method == 'POST':
        form = db_sess.query(Post).filter(Post.id == request.form['id']).one()
        return jsonify(count_likes=form.like_count)


@application.route('/api/download_app')  # Получение лайков по айди записи
def get_count_like():
    return '''<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Redirect</title>
<script type="text/javascript"> // <![CDATA[
//iPhone Version:
if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i))) {
    window.location = "https://ВАША_ССЫЛКА_НА СТРАНИЦУ_В_APP_STORE";
}
//Android Version:
if(navigator.userAgent.match(/android/i)) {
    window.location = "https://ВАША_ССЫЛКА_НА СТРАНИЦУ_В_GOOGLE_PLAY";
}
</script>
</body>
</html>'''


if __name__ == '__main__':
    db_session.global_init('db/furniture.db')
    db_sess = db_session.create_session()
    application.run(host='0.0.0.0', port=5001, debug=True)
