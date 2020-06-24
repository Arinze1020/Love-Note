from flask import Flask

app = Flask(__name__)

#from app import datab


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///love.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

ma = Marshmallow(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50),nullable=False)
    note = db.Column(db.String(10000),unique=True,nullable=False)

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "note")

#post_schema = PostSchema()
#posts_schema = PostSchema(many=True)

from app import resoures






