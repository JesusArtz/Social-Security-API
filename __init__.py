import flask_cors
import jwt
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)
flask_cors.CORS(app)


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token', None)

        if token is None:
            return jsonify({'message': 'Token is missing!'}), 403

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        if not data:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated
