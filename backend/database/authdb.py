import uuid
import bcrypt
from flask import jsonify

from config.config import HASH_SALT_LENGTH
from database.init_mongodb import db
from errors.error_handler import error_codes


def validate_request(data, required_fields):
    for field in required_fields:
        if field not in data:
            return jsonify({'code': error_codes[f'POST_MISSING_FIELD_{field.upper()}']}), 400
    return None


def authenticate_user(email, passwd):
    auth_data = db.auth.find_one({'email': email})
    if not auth_data:
        return None, None

    passwd_matching = bcrypt.checkpw(passwd.encode('utf-8'),
                                     str(auth_data.get('passwd', b'')).encode('utf-8'))
    if not passwd_matching:
        return None, None

    return auth_data.get('btoken', str(uuid.uuid4())), auth_data


def create_or_update_user(email, passwd, auth_data, btoken):
    if not auth_data:
        passwd_hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt(HASH_SALT_LENGTH))
        db.auth.insert_one({'email': email, 'passwd': passwd_hash, 'btoken': btoken, 'ftoken': []})
    else:
        db.auth.update_one({'btoken': btoken}, {'$push': {'ftoken': str(uuid.uuid4())}})


def handle_auth_request(data):
    email = data['email']
    passwd = data['passwd']
    
    btoken, auth_data = authenticate_user(email, passwd)
    if not btoken:
        return jsonify({'code': error_codes['AUTH_INCORRECT_PASSWD']}), 401

    create_or_update_user(email, passwd, auth_data, btoken)
    return jsonify({'btoken': btoken, 'ftoken': str(uuid.uuid4())}), 200


def handle_verify_request(data):
    ftoken = data['ftoken']

    auth_data = db.auth.find_one(
        {'ftoken': {'$elemMatch': {'$eq': ftoken}}},
        {'email': 1, 'btoken': 1}
    )
    if not auth_data or not auth_data.get('btoken'):
        return jsonify({'email': None, 'btoken': None}), 401

    return jsonify({
        'email': auth_data['email'],
        'btoken': auth_data['btoken']
    }), 200
