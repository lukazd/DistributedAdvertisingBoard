import cognitive_face as CF
apikey = open("apiKey", "r").read()

KEY = apikey  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)
# If you need to, you can change your base API url with:
#CF.BaseUrl.set('https://westcentralus.api.cognitive.microsoft.com/face/v1.0/')

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)
# f = open('pic.jpg', "rb")
# body = f.read()
# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
# faces = CF.face.detect(img_url)
#faces = CF.face.detect('pic.jpg', attributes="age,gender,emotion")

#person_group = CF.person_group.create("group1")

#print(person_group)
#CF.person_group.get_status("group1")
#ryanPerson = CF.person.create("group1", "Ryan")
#print ryanPerson['personId']
#print(faces)



def addToGroup1(name, pic):
    pid = CF.person.create("group1", name)['personId']
    print pid
    print CF.person.add_face(pic, "group1", pid)

def findFace(groupName, pic):
    fid = CF.face.detect(pic)[0]['faceId']
    print fid
    print CF.face.identify([fid], "group1")


addToGroup1("Jisoon", 'j1.jpg')
CF.person_group.train("group1")

findFace("group1", 'j2.jpg')