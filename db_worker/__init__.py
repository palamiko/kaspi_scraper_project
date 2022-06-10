from flask import Flask

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')

from db_worker.dto import db_models
from db_worker.api.v1 import route
