# Daniel Machlab for IoT group 5


class Advertisement:
    def __init__(self, ad_id, company, category, gender, agerange, weather, temperature):
        self.ad_id = ad_id
        self.company = company
        self.category = category
        self.gender = gender
        self.ageRange = agerange
        self.weatherConditions = weather
        self.temp = temperature

    # def load(self):
    #     ad_data = []
    #     with open("tcl/Advertisements.txt") as file_ads:
    #         line = file_ads.readline()
    #         while line:
    #             elmts = line.split(',')
    #             ad_data.append(self.__init__(elmts[0], elmts[1], elmts[2], elmts[3], elmts[4], elmts[5]))
    #             line = file_ads.readline()
    #     return ad_data


class Sensors:
    def __init__(self, temperature, humidity, traffic):
        self.temp = temperature
        self.hum = humidity
        self.traf = traffic

    # def load(self):
    #     sensor_data = []
    #     with open("tcl/Sensors.txt") as file_sensors:
    #         line = file_sensors.readline()
    #         while line:
    #             elmts = line.split(',')
    #             sensor_data.append(self.__init__(elmts[0], elmts[1], elmts[2]))
    #             line = file_sensors.readline()
    #     return sensor_data


class User:
    def __init__(self, gender, age, prev_companies, prev_activities):
        self.gender = gender
        self.age = age
        self.companies = prev_companies
        self.activities = prev_activities

    # def load(self):
    #     user_data = []
    #     with open("tcl/Users.txt") as file_users:
    #         line = file_users.readline()
    #         while line:
    #             elmts = line.split(',')
    #             user_data.append(self.__init__(elmts[0], elmts[1], elmts[2], elmts[3]))
    #             line = file_users.readline()
    #     return user_data









