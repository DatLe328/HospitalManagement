from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'HJGFGHF^&%^&&*^&*YUGHJGHJF^%&YYHB'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/test?charset=utf8mb4" % quote('root')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app)
login = LoginManager(app)

import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration
cloudinary.config(
    cloud_name = "dokzvxp8m",
    api_key = "712437327494933",
    api_secret = "<mAhCr1YQc_NUGDuGHOoQ1Ohrk1M>", # Click 'View API Keys' above to copy your API secret
    secure=True
)
