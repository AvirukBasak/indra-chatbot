from flask import request, jsonify, Blueprint
from errors.error_handler import error_codes, error_response
import database.authdb as authdb


auth = Blueprint('auth', __name__)


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
        validation_result = authdb.validate_request(data, required_fields)
        if validation_result:
            return validation_result

        return authdb.handle_auth_request(data)

    elif op == 'VERIFY':
        required_fields = ['ftoken']
        validation_result = authdb.validate_request(data, required_fields)
        if validation_result:
            return validation_result

        return authdb.handle_verify_request(data)

    else:
        return jsonify({
            'code': error_codes['POST_INVALID_OP'],
            'message': 'invalid operation: should be \'AUTH\' or \'VERIFY\''
        }), 400
