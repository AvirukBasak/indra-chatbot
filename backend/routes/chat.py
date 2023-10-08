from flask import request, jsonify, Blueprint
from backend.errors.error_handler import error_codes, error_response
import backend.database.docsdb as docsdb

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=['GET'])
def chat_get():
    return jsonify({ 'message': 'GET not supported by /chat' }), 404


# @chat.route('/chat', methods=['POST'])
# @error_response
# Create a chat api endpoint w/ following API schema
# req: {
#     'ftoken': 'auth-ftoken', (optional if none, assume anonymous and dont store any data)
#     'user_msg': 'user message',
#     '
# }