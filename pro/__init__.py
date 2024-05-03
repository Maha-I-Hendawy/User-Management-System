from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SECRET_KEY'] = '59f672b6fbe60ee8016f46e335f4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydbdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

app.app_context().push()




from . import routes