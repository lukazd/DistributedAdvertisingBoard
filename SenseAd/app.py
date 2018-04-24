from flask import Flask
application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello App!"

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
