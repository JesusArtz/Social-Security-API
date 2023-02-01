import flask
import flask_cors
from flask import request, jsonify
from functools import wraps
import jwt

app = flask.Flask(__name__)
flask_cors.CORS(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        if not data:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated