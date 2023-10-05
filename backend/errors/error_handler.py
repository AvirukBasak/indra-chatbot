import traceback
from functools import wraps
from flask import jsonify

error_codes = {
    'POST_MISSING_BODY': 'post:missing_body',
    'POST_MISSING_FIELD_OP': 'post:missing_field_op',
    'POST_INVALID_OP': 'post:invalid_op',
    'AUTH_MISSING_FIELD_EMAIL': 'auth:missing_field_email',
    'AUTH_MISSING_FIELD_PASSWD': 'auth:missing_field_passwd',
    'AUTH_INCORRECT_PASSWD': 'auth:incorrect_passwd',
    'VERIFY_MISSING_FIELD_FTOKEN': 'verify:missing_field_ftoken',
    'MONGODB_QUERY_ERROR': 'mongodb:query_error',
}


def handle_error_response(e):
    return jsonify({ 'message': str(e) }), e.code if hasattr(e, 'code') else 500


def error_response(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return jsonify({}), 500
    return decorator
