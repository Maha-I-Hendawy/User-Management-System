from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydbdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

app.app_context().push()




from . import routes