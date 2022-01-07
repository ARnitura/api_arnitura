from flask import Flask, send_file

application = Flask(__name__)


@application.route('/')
def main():
    return send_file('files/model.glb')


if __name__ == '__main__':
    application.run(port=7001)