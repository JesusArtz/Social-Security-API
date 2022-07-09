from crypt import methods
from methods.genUUID import GenerateUUID
from flask import Flask, request
import flask_cors
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph

app = Flask(__name__)
flask_cors.CORS(app)
app.secret_key(GenerateUUID())


@app.route('/api/v1/users/register', methods=['POST'])
def Register():
    
    if request.method == 'POST':
        
        data = request.get_json()
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        if password and email and username:
            
            

