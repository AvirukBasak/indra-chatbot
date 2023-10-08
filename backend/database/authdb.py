import uuid
import bcrypt
from flask import jsonify

from backend.config.config import HASH_SALT_LENGTH
from backend.database.init_mongodb import db
from backend.errors.error_handler import error_codes


def validate_request(data, required_fields):
    for field in required_fields:
        if field not in data:
            return jsonify({'code': error_codes[f'POST_MISSING_FIELD_{field.upper()}']}), 400
    return None


def create_or_update_user(email, passwd, btoken):
    ftoken = str(uuid.uuid4())
    if not btoken:
        btoken = str(uuid.uuid4())
        passwd_hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt(HASH_SALT_LENGTH))
        db.auth.insert_one({'email': email, 'passwd': passwd_hash, 'btoken': btoken, 'ftoken': [ ftoken ]})
    else:
        db.auth.update_one({'btoken': btoken}, {'$push': {'ftoken': ftoken}})
    return btoken, ftoken


def authenticate_user(email, passwd):
    auth_data = db.auth.find_one({'email': email})

    if not auth_data:
        btoken, ftoken = create_or_update_user(email, passwd, None)
        return btoken, ftoken

    passwd_matching = bcrypt.checkpw(passwd.encode('utf-8'), auth_data.get('passwd'))
    if not passwd_matching:
        return None, None

    btoken = auth_data.get('btoken')
    return create_or_update_user(email, passwd, btoken)


def handle_auth_request(data):
    email = data['email']
    passwd = data['passwd']

    btoken, ftoken = authenticate_user(email, passwd)

    if not btoken and not ftoken:
        return jsonify({'code': error_codes['AUTH_INCORRECT_PASSWD']}), 401

    return jsonify({'btoken': btoken, 'ftoken': ftoken}), 200


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
