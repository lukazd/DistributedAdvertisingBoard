from flask import Flask, request
application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello App!"

@application.route("/getAdsForUser", methods=['GET'])
def getAdsForUser():
    user_id = request.args.get('user_id')
    return "Welcome: " + user_id

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
