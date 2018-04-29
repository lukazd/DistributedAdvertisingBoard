import sys,os
import threading

from flask import Flask, request, abort, jsonify
from google.cloud import firestore

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '..', 'DistributedAdvertisingBoard/iota'))
import iota_payments

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
        ads.append({"ad_id" : doc.id, "ad" : doc.to_dict()})

    person = db.collection(u'personInfo').document(user_id).get().to_dict()

    result = {"person" : person, "ads" : ads}

    return jsonify(result)

@application.route("/rateAd", methods=['POST'])
def rateAd():
    data = request.form
    user_id = data["user_id"]
    rating = data["rating"]
    ad_id = data["ad_id"]

    if user_id is None or ad_id is None or rating is None:
        return abort(400)

    return "Thanks for submitting rating"

@application.route("/logOut", methods=['POST'])
def logOut():
    data = request.form
    user_id = data["user_id"]
    payment = data.get('payment', type=int)

    if user_id is None or payment is None:
        return abort(400)

    iota_payment_thread = threading.Thread(target=iota_payments.create_and_send_transactions, args=("VEYONVNFFAQPKYMMOJZJ9JLQNBVGQMMLSDNTWZQYCYYNNJIBOKJHHGCIKKNEVEAXQO9MJXEQLFPQCIEAW", payment, 'SenseAd Payment'))
    iota_payment_thread.setDaemon(True)
    iota_payment_thread.start()

    return "Thanks for submitting rating"


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
