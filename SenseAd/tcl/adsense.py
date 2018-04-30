from tcl.adsense_classes import Advertisement, Sensors, User

ad_data = []
with open("Advertisements.txt") as file_ads:
    line = file_ads.readline()
    while line:
        elmts = line.split(',')
        ad = Advertisement(elmts[0], elmts[1], elmts[2], elmts[3], elmts[4], elmts[5])
        ad_data.append(ad)
        line = file_ads.readline()

sensor_data = []
with open("Sensors.txt") as file_sensors:
    line = file_sensors.readline()
    while line:
        elmts = line.split(',')
        sensor = Sensors(elmts[0], elmts[1], elmts[2])
        sensor_data.append(sensor)
        line = file_sensors.readline()

user_data = []
with open("Users.txt") as file_users:
    line = file_users.readline()
    while line:
        elmts = line.split(',')
        user = User(elmts[0], elmts[1], elmts[2], elmts[3])
        user_data.append(user)
        line = file_users.readline()

test_user = user_data[0]
test_sensor = sensor_data[0]
for ad in ad_data:
    count = 0
    if ad.company.strip() == test_user.companies.strip():
        count += 1
    if ad.category.strip() == test_user.activities.strip():
        count += 1
    if ad.gender.strip() == test_user.gender.strip():
        count += 1
    if ad.ageRange.strip() == test_user.age.strip():
        count += 1
    if ad.temp.strip() == test_sensor.temp.strip():
        count += 1
    print(ad.company, count, sep=' ')