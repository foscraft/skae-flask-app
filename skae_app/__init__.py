from flask import Flask

from skae_app.hello.views import skaes

app = Flask(__name__)
app.register_blueprint(skaes)