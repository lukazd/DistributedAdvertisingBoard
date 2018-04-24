from flask import Flask, request, abort, jsonify
from google.cloud import firestore
application = Flask(__name__)

db = firestore.Client()

@application.route("/")
def hello():
    return "Hello App!"

@application.route("/getAdsForUser", methods=['GET'])
def getAdsForUser():
    user_id = request.args.get('user_id')

    if user_id is None:
        return abort(400)

    docs = db.collection(u'ads').where(u'category', u'==', u'carAds').get()

    ads = []
    for doc in docs:
        ads.append(doc.to_dict())

    person = db.collection(u'personInfo').document(user_id).get().to_dict()

    result = {"person" : person, "ads" : ads}

    return jsonify(result)

@application.route("/rateAd", methods=['POST'])
def rateAd():
    data = request.form
    user_id = data["user_id"]
    rating = data["rating"]
    ad_id = data["ad_id"]

    print(user_id)
    print(rating)
    print(ad_id)

    return "Thanks for submitting rating"


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
