import os
from flask import Flask, send_from_directory

from backend.routes.auth import auth
from backend.config.config import PORT, FRONTENED_PATH, FRONTENED_DEPENDENCIES, STATIC_FILES_PATH
from backend.errors.error_handler import handle_error_response

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
def serve_index():
    return send_from_directory(
        directory = STATIC_FILES_PATH,
        path = 'index.html'
    )

# Serve static files from the static folder
@app.route('/<path:fpath>')
def serve_static_file(fpath):
    return send_from_directory(
        directory = STATIC_FILES_PATH,
        path = fpath
    )

if __name__ == '__main__':
    app.run(port=PORT)
