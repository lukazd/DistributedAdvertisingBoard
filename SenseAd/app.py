from flask import Flask, request, abort
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

    print(docs)
    return docs

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    return "Welcome: " + user_id


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
