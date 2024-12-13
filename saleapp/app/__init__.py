from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)

app.secret_key='DFJWRT39[E]F/GDMGRGJFDKLS;LFMJLEMVS'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4

db = SQLAlchemy(app)


cloudinary.config(cloud_name='tthau',
                  api_key='372274126191375',
                  api_secret='Abk-RA6C6MUKDV34nOuFDhpLFjs')


login = LoginManager(app)