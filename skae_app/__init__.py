from flask import Flask
import secrets
from skae_app.hello.views import skaes

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.register_blueprint(skaes)