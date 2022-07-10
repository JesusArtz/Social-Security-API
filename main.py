from crypt import methods
import json
from methods.genUUID import GenerateUUID
from flask import Flask, jsonify, request
import flask_cors
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
import models as md

app = Flask(__name__)
flask_cors.CORS(app)



@app.route('/api/v1/users/register', methods=['POST'])
def Register():
    
    if request.method == 'POST':
        
        data = request.get_json()
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        if password and email and username:
            
            hPass = genph(password)
            
            responseModel = md.registerUser(email, username, hPass)
            
            if responseModel:
                
                getHashedPass = md.getHash(email)
                
                unHashPass = checkph(getHashedPass[0], password)
                
                if unHashPass:
                    
                    respLogin = md.loginUser(email, getHashedPass[0])
                    
                    if respLogin:
                        
                        return jsonify(respLogin)
                    
                return jsonify({'response':'an error as ocurred 1'})
            
            return jsonify({'response':'an error as ocurred 2'})
        
        return jsonify({'response':'an error as ocurred 3'})
    
                      
@app.route('/api/v1/users/login', methods=['POST'])  
def Login():
    
    if request.method == 'POST':
        
        data = request.get_json()
        
        if data:
            
            email = data['email']
            password = data['password']
            
            if email and password:
                
                getHashedPass = md.getHash(email)
                
                if getHashedPass:
                
                    unHashPass = checkph(getHashedPass[0], password)
                    
                    if unHashPass:
                        
                        respLogin = md.loginUser(email, getHashedPass[0])
                        
                        if respLogin:
                            
                            getToken = f"{GenerateUUID()}"
                            
                            respSession = md.generateSession(respLogin['id'], getToken)
                            
                            if respSession:
                                
                                return jsonify({
                                    "id":respLogin['id'],
                                    "username":respLogin['username'],
                                    "email":respLogin['email'],
                                    "token":f"{getToken}"
                                })
                
                    return jsonify({'response':'Incorrect Password'})                                    
                
                return jsonify({'response':'Incorrect Email'})  
                
            return jsonify({'response':'Null data'})  
        
        return jsonify({'response':'No data'})  

@app.route('/api/v1/users/logout', methods=['POST'])
def Logout():
    
    if request.method == 'POST':
        
        data = request.get_json()
        
        if data:
            
            id = data['id']
            
            if id:
                
                respLogout = md.deleteSession(id)
                
                if respLogout:
                    
                    return jsonify({})


app.run(port=5000, debug=True)