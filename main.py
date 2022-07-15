from crypt import methods
from distutils.log import error
import json
from locale import currency
from methods.genUUID import GenerateUUID
from flask import Flask, jsonify, request
import flask_cors
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
import models as md
from convertBase64 import processImage, processPostImage
import stripe

app = Flask(__name__)
flask_cors.CORS(app)

stripe.api_key = "sk_test_51LLGC6L6X1F1cMlGS8lon3H0IrNl8QMpHdxF5o7ADhehnv5xI6F5fdwTvfPKuAKbpusEUumurNwNAoeVzcaeAWtJ00RHJ1hwbY"

@app.route('/api/v1/users/register', methods=['POST'])
def Register():

    if request.method == 'POST':

        data = request.get_json()

        username = data['username']
        email = data['email']
        password = data['password']

        if password and email and username:

            existentEmail = md.getExistEmail(email)
            existentUsername = md.getExistUsername(username)

            if existentEmail or existentUsername:

                hPass = genph(password)

                responseModel = md.registerUser(email, username, hPass)

                if responseModel:

                    getHashedPass = md.getHash(email)

                    unHashPass = checkph(getHashedPass[0], password)

                    if unHashPass:

                        respLogin = md.loginUser(email, getHashedPass[0])

                        if respLogin:

                            getToken = f"{GenerateUUID()}"

                            respSession = md.generateSession(
                                respLogin['id'], getToken)

                            if respSession:

                                return jsonify({
                                    "id": respLogin['id'],
                                    "username": respLogin['username'],
                                    "email": respLogin['email'],
                                    "token": f"{getToken}",
                                    "is_active": respLogin['is_active'],
                                    "is_staff": respLogin['is_staff'],
                                    "profile": {
                                        'id': 0,
                                        'name': 'none',
                                        'description': 'none',
                                        'image': 'none'
                                    }
                                })

                            return jsonify({'response': 'an error as ocurred during creation of session'})

                        return jsonify({'response': 'an error as ocurred'})

                return jsonify({'response': 'an error as ocurred on register'})

            return jsonify({'response': 'Email or username already exist'})

        return jsonify({'response': 'No data'})

    return jsonify({'response': 'Method not allowed'})


@app.route('/api/v1/users/login', methods=['POST'])
def Login():

    if request.method == 'POST':

        data = request.get_json()

        if data:

            email = data['email']
            password = data['password']

            if email and password:

                getHashedPass = md.getHash(email)

                if getHashedPass[0]:

                    unHashPass = checkph(getHashedPass[0], password)

                    print(unHashPass)

                    if unHashPass:

                        respLogin = md.loginUser(email, getHashedPass[0])

                        if respLogin:

                            getToken = f"{GenerateUUID()}"

                            respSession = md.generateSession(
                                respLogin['id'], getToken)

                            if respSession:

                                profileData = md.getProfile(respLogin['id'])

                                if profileData:

                                    return jsonify({
                                        "id": respLogin['id'],
                                        "username": respLogin['username'],
                                        "email": respLogin['email'],
                                        "token": f"{getToken}",
                                        "is_active": respLogin['is_active'],
                                        "is_staff": respLogin['is_staff'],
                                        "profile": {
                                            'id': profileData[0],
                                            'name': profileData[1],
                                            'description': profileData[2],
                                            'image': profileData[3]
                                        }
                                    })

                                return jsonify({
                                    "id": respLogin['id'],
                                    "username": respLogin['username'],
                                    "email": respLogin['email'],
                                    "token": f"{getToken}",
                                    "is_active": respLogin['is_active'],
                                    "is_staff": respLogin['is_staff'],
                                    "profile": {
                                        'id': 0,
                                        'name': 'none',
                                        'description': 'none',
                                        'image': 'none'
                                    }
                                })

                            return jsonify({'response': 'Incorrect Password 2'})

                        return jsonify({'response': 'Incorrect Password 1'})

                    return jsonify({'response': 'Incorrect Password'})

                return jsonify({'response': 'Incorrect Email'})

            return jsonify({'response': 'Null data'})

        return jsonify({'response': 'No data'})


@app.route('/api/v1/users/logout', methods=['POST'])
def Logout():

    if request.method == 'POST':

        data = request.get_json()

        if data:

            id = data['token']

            if id:

                respLogout = md.deleteSession(id)

                if respLogout:

                    return jsonify({'response': 'ok'})

            return jsonify({'response': 'Id is null'})

        return jsonify({'response': 'No data'})

    return jsonify({'response': 'Incorrect Method'})


@app.route('/api/v1/users/createProfile', methods=['POST'])
def CreateProfile():

    if request.method == 'POST':

        data = request.get_json()

        if data:

            id = data['id']
            name = data['name']
            description = data['description']
            imageToConvert = data['image']

            if name and description and imageToConvert and id:

                convertImage = processImage(imageToConvert)

                print(convertImage)

                if convertImage:

                    resp = md.createProfile(
                        id, name, description, convertImage)

                    if resp:

                        profileData = md.getProfile(id)
                        respLogin = md.getUserById(id)
                        getToken = md.getSessionById(id)

                        return jsonify({
                            "id": respLogin[0],
                            "username": respLogin[1],
                            "email": respLogin[2],
                            "token": f"{getToken[0]}",
                            "is_active": respLogin[3],
                            "is_staff": respLogin[4],
                            "profile": {
                                'id': profileData[0],
                                'name': profileData[1],
                                'description': profileData[2],
                                'image': profileData[3]
                            }})

                return jsonify({'response': 'an error as ocurred'})

            return jsonify({'response': 'null data'})

        return jsonify({'response': 'null data'})


@app.route('/api/v1/users/getProfile', methods=['POST'])
def GetProfile():

    if request.method == 'POST':

        data = request.get_json()

        if data:

            token = data['token']

            if token:

                response = md.getIdFromToken(token)

                if response:

                    profileData = md.getProfile(response[0])

                    if profileData:

                        return jsonify({
                            'profile_id': profileData[0],
                            'name': profileData[1],
                            'description': profileData[2],
                            'image': profileData[3]
                        })

                    return jsonify({'response': 'Profile doesnt exist'})

                return jsonify({'response': 'Invalid session'})

            return jsonify({'response': 'Null token'})

        return jsonify({'response': 'No data'})


@app.route('/api/v1/users/newPost', methods=['POST'])
def NewPost():

    data = request.get_json()

    id = data['id']
    username = data['username']
    name = data['name']
    content = data['content']
    imageToConvert = data['image']
    profileImage = data['profileImage']

    if imageToConvert:
        convertedImage = processPostImage(imageToConvert)
        image = md.getImageFromId(id)

        resp = md.createPost(id, username, name, content,
                             convertedImage, image)

        if resp:

            return jsonify({'response': 'ok'})

    resp = md.createPost(id, username, name, content, 'none', profileImage)

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
        "id":resp[0],
        "username":resp[1],
        "description":resp[2],
        "image":resp[3]
    })
    
    
@app.route('/api/v1/users/getPostsById', methods=['POST'])
def getPostsById():
    
    data = request.get_json()
    
    id = data['id']
    
    resp = md.getPostsById(id)
    
    return jsonify(resp)


app.run(port=5000, debug=True)
