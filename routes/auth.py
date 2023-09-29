import uuid
import bcrypt
from flask import request, jsonify, Blueprint

from modules.config import HASH_SALT_LENGTH
from modules.database import db
from modules.error_handler import error_codes, error_response

auth = Blueprint('auth', __name__)


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


@auth.route('/auth', methods=['GET'])
def auth_get():
    return jsonify({ 'message': 'GET not supported by /auth' }), 404


@auth.route('/auth', methods=['POST'])
@error_response
def auth_post():
    data = request.get_json()
    if not data:
        return jsonify({'code': error_codes['POST_MISSING_BODY']}), 400

    op = data.get('op')
    if not op:
        return jsonify({'code': error_codes['POST_MISSING_FIELD_OP']}), 400

    if op == 'AUTH':
        required_fields = ['email', 'passwd']
        validation_result = validate_request(data, required_fields)
        if validation_result:
            return validation_result

        return handle_auth_request(data)

    elif op == 'VERIFY':
        required_fields = ['ftoken']
        validation_result = validate_request(data, required_fields)
        if validation_result:
            return validation_result

        return handle_verify_request(data)

    else:
        return jsonify({
            'code': error_codes['POST_INVALID_OP'],
            'message': 'invalid operation: should be \'AUTH\' or \'VERIFY\''
        }), 400
