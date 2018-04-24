from adsense_classes import Advertisement, Sensors, User
from google.cloud import firestore
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from surprise import SVD
from surprise import Dataset
import pandas as pd
import numpy as np

np.random.seed(0)

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
print(df.head())
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
print("----after species addition-----")
print(df.head())

def get_top_n(predictions, uuid, n=10):
    top_n = defaultdict(list)
    for iid, true_r, est, _ in predictions:
        top_n[uuid].append((iid,est))

    for user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n 

data = Dataset.load_builtin('ml-100k')

algo = SVD()

trainset = data.build_full_trainset()

algo.fit(trainset)

pred = algo.predict(2,2,4,True)

print(pred)

db = firestore.Client()

users_ref = db.collection(u'carAds')
docs = users_ref.get()

#for doc in docs:
    #print(u'{} => {}'.format(doc.id, doc.to_dict()))

# ad_data = []
# with open("Advertisements.txt") as file_ads:
#     line = file_ads.readline()
#     while line:
#         elmts = line.split(',')
#         ad = Advertisement(elmts[0], elmts[1], elmts[2], elmts[3], elmts[4], elmts[5], elmts[6])
#         ad_data.append(ad)
#         line = file_ads.readline()
#
# sensor_data = []
# with open("Sensors.txt") as file_sensors:
#     line = file_sensors.readline()
#     while line:
#         elmts = line.split(',')
#         sensor = Sensors(elmts[0], elmts[1], elmts[2])
#         sensor_data.append(sensor)
#         line = file_sensors.readline()
#
# user_data = []
# with open("Users.txt") as file_users:
#     line = file_users.readline()
#     while line:
#         elmts = line.split(',')
#         user = User(elmts[0], elmts[1], elmts[2], elmts[3])
#         user_data.append(user)
#         line = file_users.readline()
#
# test_user = user_data[0]
# test_sensor = sensor_data[0]
# ad_results = {}
# for ad in ad_data:
#     count = 0
#     if ad.company.strip() == test_user.companies.strip():
#         count += 1
#     if ad.category.strip() == test_user.activities.strip():
#         count += 1
#     if ad.gender.strip() == test_user.gender.strip():
#         count += 1
#     if ad.ageRange.strip() == test_user.age.strip():
#         count += 1
#     if ad.temp.strip() == test_sensor.temp.strip():
#         count += 1
#     ad_results.update({ad.ad_id : count})
#
#     print(ad.ad_id, count, sep=' ')
#     print(ad_results)
#
# sorted_ad_results = sorted(ad_results.items(), key=operator.itemgetter(1))
# print(sorted_ad_results)
