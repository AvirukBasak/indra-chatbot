import os
from flask import Flask, send_from_directory

from routes.auth import auth
from modules.config import PORT
from modules.error_handler import handle_error_response

app = Flask(__name__)

# Register error handling decorator
app.register_blueprint(auth)
app.register_error_handler(Exception, handle_error_response)

# Set the static folder and URL path for serving frontend assets
app.static_folder = "static"
app.static_url_path = "/static"

# Serve index.html as the default page from the static folder
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(port=PORT)
