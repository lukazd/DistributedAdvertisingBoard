from adsense_classes import Advertisement, Sensors, User
from google.cloud import firestore
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from surprise import SVD
from surprise import Dataset
import pandas as pd
import numpy as np



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


##sklearn example below
np.random.seed(0)
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
print(df.head())
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
print("----after species addition-----")
print(df.head())


db = firestore.Client()

users_ref = db.collection(u'carAds')
docs = users_ref.get()

df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

print(df.head())

#creates two new dataframes, one with the training rows, one witht the test rows
train, test = df[df['is_train']==True], df[df['is_train']==False]
print('Number of observations in the training data:', len(train))
print('Number of observation in the test data:', len(test))
features = df.columns[:4]
print(features)

#convert the species name into digit - 0,1, or 2
#for sensead, we will have categories instead of species
y = pd.factorize(train['species'])[0]
print('y: ', y)

#create RandomForestClassifier, clf = Classifier
clf = RandomForestClassifier(n_jobs=2, random_state=0)

#train the classifier to take the training features and learn how they
#relater to the trainging y (the species)
clf.fit(train[features], y)
print('clf: ',clf)

#applies classifier train above to the test data, this test accuracy of model
#array shoes what species the model predicts each plant is based on
#the four data points, septal length/width and petal legth/width
print('test preditctions: ', clf.predict(test[features]))

#Shows the predicted probability of the first 10 observations
print('prediction probability', clf.predict_proba(test[features])[0:10])

#EVALUATION OF CLASSIFIER
#create english names for the plants for each predicted plant class
preds = iris.target_names[clf.predict(test[features])]

#print PREDICTED species for the first five observations
print(preds[0:5])

#View the ACTUAL species for the first 5 observations
print(test['species'].head())

#create a confusion matrix to test the rest of the data
#Columns are the species we predicted for the test data
#Rows are the actual species for the test data
print(pd.crosstab(test['species'], preds, rownames=['Actual Species'], colnames=['Predicted Species']))

#View a list of the features and their importance scores
print(list(zip(train[features], clf.feature_importances_)))






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
