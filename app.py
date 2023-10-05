import os
from flask import Flask, send_from_directory

from routes.auth import auth
from modules.config import PORT, FRONTENED_PATH, FRONTENED_DEPENDENCIES, STATIC_FILES_PATH
from modules.error_handler import handle_error_response

# build and install frontend dependencies

if not os.path.isdir(FRONTENED_DEPENDENCIES):
    os.system(f'cd {FRONTENED_PATH} && npm install')

if not os.path.isdir(STATIC_FILES_PATH):
    os.system(f'cd {FRONTENED_PATH} && npm run build')


app = Flask(__name__)

# Register error handling decorator
app.register_blueprint(auth)
app.register_error_handler(Exception, handle_error_response)

# Set the static folder and URL path for serving frontend assets
app.static_folder = STATIC_FILES_PATH
app.static_url_path = f'/{STATIC_FILES_PATH}'

# Serve index.html as the default page from the static folder
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=PORT)
