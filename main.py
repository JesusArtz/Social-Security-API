from crypt import methods
from distutils.log import error
from locale import currency
from methods.genUUID import GenerateUUID
from flask import Flask, jsonify, request
import flask_cors
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
import models as md
from convertBase64 import processImage, processPostImage
import stripe
import datetime
import requests

app = Flask(__name__)
flask_cors.CORS(app)

stripe.api_key = "sk_test_51LLGC6L6X1F1cMlGS8lon3H0IrNl8QMpHdxF5o7ADhehnv5xI6F5fdwTvfPKuAKbpusEUumurNwNAoeVzcaeAWtJ00RHJ1hwbY"


"""

REGISTER ROUTE

Gets three elements of the json, username, email and password,
then compares if the username or email exists, if not proceed
to create the account.

Response codes:

User already exist - 409

Error during session creation - 430

"""


@app.route('/api/v1/users/register', methods=['POST'])
def Register():

    data = request.get_json()

    username = data['username']
    description = data['description']
    image = data['image']
    email = data['email']
    password = data['password']
    latitude = data['latitude']
    longitude = data['longitude']
    
    try:
        convertImage = processImage(image)
        
    except:
        
        convertImage = 'xd'


    existentEmail = md.getExistEmail(email)
    existentUsername = md.getExistUsername(username)

    if existentEmail or existentUsername:

        hPass = genph(password)
        
        requestData = requests.get(f'https://nominatim.openstreetmap.org/reverse.php?lat={latitude}&lon={longitude}&zoom=16&format=jsonv2')
    
        jsonGeo = requestData.json()
    
        zipCode = jsonGeo['address']['postcode']

        md.registerUser(email, username, description, convertImage, hPass, zipCode)

        getHashedPass = md.getHash(email)

        respLogin = md.loginUser(email, getHashedPass[0])

        getToken = f"{GenerateUUID()}"

        md.generateSession(respLogin['id'], getToken)     

        return jsonify({
                "id": respLogin['id'],
                "username": respLogin['username'],
                "email": respLogin['email'],
                "token": f"{getToken}",
                "is_staff": respLogin['is_staff'],
                "is_donator": respLogin['is_donator'],
                "zip_code":respLogin['zip_code'],
                "profile": {
                    'description': respLogin['description'],
                    'image': respLogin['image']
                }
            })

    return jsonify({'response': 409})


"""

LOGIN ROUTE

It obtains two elements of the json, email and password, later
they are compared, and if they exist, a profile associated with
the user is searched to later send it together with the session.

Response codes:

No data in json fields - 403

Error during session creation - 430

Incorrect email or password - 417

"""


@app.route('/api/v1/users/login', methods=['POST'])
def Login():

    data = request.get_json()

    email = data['email']
    password = data['password']

    if email and password:

        getHashedPass = md.getHash(email)

        if getHashedPass[0]:

            unHashPass = checkph(getHashedPass[0], password)

            if unHashPass:

                respLogin = md.loginUser(email, getHashedPass[0])

                getToken = f"{GenerateUUID()}"
                
                md.generateSession(respLogin['id'], getToken)

                return jsonify({
                            "id": respLogin['id'],
                            "username": respLogin['username'],
                            "email": respLogin['email'],
                            "token": f"{getToken}",
                            "is_staff": respLogin['is_staff'],
                            "is_donator": respLogin['is_donator'],
                            "zip_code":respLogin['zip_code'],
                            "profile": {
                                'description': respLogin['description'],
                                'image': respLogin['image']
                            }
                        })
            return jsonify({'response': 417})

        return jsonify({'response': 417})

    return jsonify({'response': 403})


"""

LOGOUT ROUTE

Gets a json with a field called token in which 
the user's session token is received, then the 
session is deleted.

RESPONSE CODES:

Correctly logout - 200

Error on logout - 500


"""


@app.route('/api/v1/users/logout', methods=['POST'])
def Logout():

    data = request.get_json()


    id = data['token']

    respLogout = md.deleteSession(id)

    if respLogout:

        return jsonify({'response': 200})

    return jsonify({'response': 500})


# @app.route('/api/v1/users/createProfile', methods=['POST'])
# def CreateProfile():

#     if request.method == 'POST':

#         data = request.get_json()

#         if data:

#             id = data['id']
#             name = data['name']
#             description = data['description']
#             imageToConvert = data['image']

#             if name and description and imageToConvert and id:

#                 convertImage = processImage(imageToConvert)

#                 print(convertImage)

#                 if convertImage:

#                     resp = md.createProfile(
#                         id, name, description, convertImage)

#                     if resp:

#                         profileData = md.getProfile(id)
#                         respLogin = md.getUserById(id)
#                         getToken = md.getSessionById(id)

#                         return jsonify({
#                             "id": respLogin[0],
#                             "username": respLogin[1],
#                             "email": respLogin[2],
#                             "token": f"{getToken[0]}",
#                             "is_active": respLogin[3],
#                             "is_staff": respLogin[4],
#                             "profile": {
#                                 'id': profileData[0],
#                                 'name': profileData[1],
#                                 'description': profileData[2],
#                                 'image': profileData[3]
#                             }})

#                 return jsonify({'response': 'an error as ocurred'})

#             return jsonify({'response': 'null data'})

#         return jsonify({'response': 'null data'})


# @app.route('/api/v1/users/getProfile', methods=['POST'])
# def GetProfile():

#     if request.method == 'POST':

#         data = request.get_json()

#         if data:

#             token = data['token']

#             if token:

#                 response = md.getIdFromToken(token)

#                 if response:

#                     profileData = md.getProfile(response[0])

#                     if profileData:

#                         return jsonify({
#                             'profile_id': profileData[0],
#                             'name': profileData[1],
#                             'description': profileData[2],
#                             'image': profileData[3]
#                         })

#                     return jsonify({'response': 'Profile doesnt exist'})

#                 return jsonify({'response': 'Invalid session'})

#             return jsonify({'response': 'Null token'})

#         return jsonify({'response': 'No data'})


@app.route('/api/v1/users/newPost', methods=['POST'])
def NewPost():

    data = request.get_json()

    id = data['id']
    name = data['name']
    content = data['content']
    imageToConvert = data['image']
    image = data['profileImage']
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(date)

    if imageToConvert:
        convertedImage = processPostImage(imageToConvert)

        resp = md.createPost(id, name, content, convertedImage, image, date)

        if resp:

            return jsonify({'response': 'ok'})

    resp = md.createPost(id, name, content, 'none', image, date)

    return jsonify({'response': 'ok'})


@app.route('/api/v1/users/getPosts', methods=['GET'])
def GetPosts():

    resp = md.getPosts()

    return jsonify(resp)


@app.route('/api/v1/payment/submitPaymentInfo', methods=['POST'])
def confirmPaymentIntent():

    try:

        data = request.get_json()

        charge = stripe.Charge.create(
            amount=data['amount'],
            currency='usd',
            description=data['description'],
            source='tok_visa',
            idempotency_key=data['id']
        )

        if charge['paid']:

            updated = md.setDonator(data['username'])

            if updated:

                return jsonify(charge)

    except stripe.error.StripeError as e:

        print(e)
        return 'error'


@app.route('/api/v1/users/getProfileById', methods=['POST'])
def getProfileById():

    data = request.get_json()

    id = data['id']

    print(id)

    resp = md.getProfile(id)

    return jsonify({
        "id": resp[0],
        "username": resp[1],
        "description": resp[2],
        "image": resp[3],
        "is_donator": resp[4]
    })


@app.route('/api/v1/users/getPostsById', methods=['POST'])
def getPostsById():

    data = request.get_json()

    id = data['id']

    resp = md.getPostsById(id)

    return jsonify(resp)

@app.route('/api/v1/users/getPostsFollow', methods=['POST'])
def getPostsFollow():
    
    data = request.get_json()
    
    id = data['id']
    
    resp = md.getFollowsId(id)    

    arr = f'{id} '

    for i in resp:
    
        arr = arr + f"{i[0]} "
    
    dataFollow = arr.replace(' ', ',').rstrip(',') 
    
    posts = md.getPostsFollowing(dataFollow)    
    
    return jsonify(posts)

@app.route('/api/v1/users/follow', methods=['POST'])
def follow():

    data = request.get_json()

    followerId = data['follower']
    followedId = data['followed']

    resp = md.setFollow(followerId, followedId)

    if resp:

        return jsonify({'response': 'ok'})

    return '', 500


@app.route('/api/v1/users/getFollow', methods=['POST'])
def getFollowing():

    data = request.get_json()

    id = data['followerid']
    followedId = data['followedid']
    
    resp = md.getFollow(id, followedId)
    
    if resp:
        
        return jsonify({'response':'ok'}),200
    
    return 400
    
    

@app.route('/api/v1/users/search', methods=['POST'])
def search():
    
    data = request.get_json()
    
    search = data['search']
    
    a = md.busqueda(search)
    
    return jsonify(a)

@app.route('/api/v1/users/getAllUsers', methods=['GET'])
def getAllUsers():
    
    resp = md.getAllUsers()
    
    return resp


@app.route('/api/v1/emergency', methods=['POST'])
def emergencyPost():
    
    data = request.get_json()
    
    id = data['id']
    name = data['username']
    image = data['image']
    message = data['message']
    latitude = data['latitude']
    longitude = data['longitude']
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    requestData = requests.get(f'https://nominatim.openstreetmap.org/reverse.php?lat={latitude}&lon={longitude}&zoom=16&format=jsonv2')
    
    jsonGeo = requestData.json()
    
    zipCode = jsonGeo['address']['postcode']
    
    md.emergency(id, name, message, image, latitude, longitude, date, zipCode)
    
    return jsonify({'a':'a'})

@app.route('/api/v1/getEmergencys', methods=['POST'])
def getEmergency():
    
    data = request.get_json()
    
    zipCode = data['zip_code']
    
    respObj = md.getEmergencys(zipCode)
    
    return jsonify(respObj)

app.run(port=5000, debug=True)
