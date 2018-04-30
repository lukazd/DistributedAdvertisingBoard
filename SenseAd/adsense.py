import pandas as pd
import numpy as np
import pickle

from adsense_classes import Advertisement, Sensors, User
from google.cloud import firestore
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from surprise import SVD
from surprise import Dataset, Reader
from collections import defaultdict

db = firestore.Client()

def get_top_n(predictions, n=10):

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def build_recommendations():
    reader_params=dict(line_format='user item rating',
                        rating_scale=(1,3),
                        sep=',')
    reader = Reader(**reader_params)
    data = Dataset.load_from_file(file_path='./ratings.txt', reader=reader)

    trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)

    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    top_n = get_top_n(predictions, n=2)

    for uid, user_ratings in top_n.items():
        data = {
            u'recommendations': [iid for (iid, _) in user_ratings],
        }

        db.collection(u'personInfo').document(uid).update(data)

def download_ratings():
    global db
    ratings_file = open("ratings.txt","w")
    ratings = db.collection(u'ratings').get()
    for rating in ratings:
        rating_dict = rating.to_dict()
        ad_id = rating_dict["ad_id"]
        user_id = rating_dict["user_id"]
        rating = rating_dict["rating"]
        ratings_file.write(user_id + ',' + ad_id + ',' + str(rating) + '\n')
    ratings_file.close()

def filter_predictions():
    np.random.seed(0)
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

    train, test = df[df['is_train']==True], df[df['is_train']==False]
    print('Number of observations in the training data:', len(train))
    print('Number of observation in the test data:', len(test))
    features = df.columns[:4]

    y = pd.factorize(train['species'])[0]

    clf = RandomForestClassifier(n_jobs=2, random_state=0)

    clf.fit(train[features], y)
    print('test preditctions: ', clf.predict(test[features]))

    print('prediction probability', clf.predict_proba(test[features])[0:10])

def predict_categories(sex, age):
    sensor = db.collection(u'sensorData').document('1').get().to_dict()
    temperature = sensor["temperature"]
    pressure = sensor["pressure"]
    humidity = sensor["humidity"]
    traffic = sensor["traffic"]

    categories = ['carAds','foodAds', 'vacationAds', 'foodAds', 'videoGameAds', 'clothingAds','techAds']
    categories_to_keep = []
    df = pd.DataFrame(columns=['sex','age','temperature','pressure','humidity','traffic','category','like'])
    for i in categories:
        df.loc[i] = [sex, age, temperature, pressure, humidity, traffic, i,'0']
        categories_to_keep.append(i)

    df_var = pd.get_dummies(df).copy()

    clf = pickle.load(open('model.sav', 'rb'))
    return categories_to_keep

def train_model():
    df = pd.read_csv('train.txt')
    df["sex"] = df["sex"].astype("category")
    df["category"] = df["category"].astype("category")
    df["like"] = df["like"].astype("category")
    #print(df)


    features = df.columns[:7]

    df_var = pd.get_dummies(df[features]).copy()

    y = pd.factorize(df["like"])[0]

    clf = RandomForestClassifier(n_jobs=2)
    #clf = GaussianNB()

    clf.fit(df_var, y)
    filename = 'model.sav'
    pickle.dump(clf, open('model.sav', 'wb'))

