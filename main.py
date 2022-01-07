from flask import Flask, send_file

app = Flask(__name__)


@app.route('/')
def main():
    return send_file('files/pufik.glb')


if __name__ == '__main__':
    app.run(port=7001)