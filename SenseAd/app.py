import sys,os
import threading
import random
import datetime
import dateutil
import adsense

from flask import Flask, request, abort, jsonify
from google.cloud import firestore

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '..', 'DistributedAdvertisingBoard/iota'))
import iota_payments

def birthday(date):
    format_str = '%m/%d/%Y' # The format
    bday = datetime.datetime.strptime(date, format_str)

    # Get the current date
    now = datetime.datetime.utcnow()
    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, bday)
    age = age.years

    return age

application = Flask(__name__)

TRAINING_PHASE = True

db = firestore.Client()

@application.route("/")
def hello():
    return "Hello App!"

@application.route("/getAdsForUser", methods=['GET'])
def getAdsForUser():
    user_id = request.args.get('user_id')

    if user_id is None:
        return abort(400)

    person = db.collection(u'personInfo').document(user_id).get().to_dict()

    recommendations = person.get("recommendations")

    docs = db.collection(u'ads').get()
    docs = list(docs)

    ads = []

    if recommendations is None:
        recommendations = []
        random_docs = random.sample(docs, 10)
        for doc in random_docs:
            recommendations.append(doc.id)

    for doc in docs:
        doc_id = doc.id
        doc_c = doc.to_dict()
        if (doc_c["ad_id"] in recommendations):
            ads.append({"ad_id" : doc.id, "ad" : doc.to_dict()})

    if (not TRAINING_PHASE):
        sensor = db.collection(u'sensorData').document('1').get().to_dict()
        temperature = sensor["temperature"]
        pressure = sensor["pressure"]
        humidity = sensor["humidity"]
        traffic = sensor["traffic"]
        adsense.predict_categories(person["sex"], birthday(person["bday"]))

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

    rating_number = 1
    if (rating == "Like"):
        rating_number = 3
    if (rating == "Neutral"):
        rating_number = 2

    data = {
        u'user_id': user_id,
        u'ad_id': ad_id,
        u'rating': rating_number
    }

    db.collection(u'ratings').document(user_id +'-' + ad_id).set(data)

    ad = db.collection(u'ads').document(ad_id).get().to_dict()
    ad_category = ad["category"]

    person = db.collection(u'personInfo').document(user_id).get().to_dict()
    person_sex = person['sex']
    person_age = str(birthday(person['bday']))

    sensor = db.collection(u'sensorData').document('1').get().to_dict()
    temperature = str(sensor["temperature"])
    pressure = str(sensor["pressure"])
    humidity = str(sensor["humidity"])
    traffic = str(sensor["traffic"])

    if (TRAINING_PHASE):
        # sex,age,temperature,humidity,pressure,traffic,category,like
        train_file = open("train.txt", "a")
        data_list = [person_sex,person_age,temperature,humidity,pressure,traffic,ad_category,str(rating == "Like")]
        data_to_write = ",".join(data_list)
        train_file.write(data_to_write)
        train_file.close()

    return "Thanks for submitting rating"

@application.route("/logOut", methods=['POST'])
def logOut():
    data = request.form
    user_id = data["user_id"]
    payment = data.get('payment', type=int)

    if user_id is None or payment is None:
        return abort(400)

    person = db.collection(u'personInfo').document(user_id).get().to_dict()

    iota_payment_thread = threading.Thread(target=iota_payments.create_and_send_transactions, args=(person["iotaCode"], payment, 'SenseAd Payment'))
    iota_payment_thread.setDaemon(True)
    iota_payment_thread.start()

    return "Thanks for submitting rating"

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
