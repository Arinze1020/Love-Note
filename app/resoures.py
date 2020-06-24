from app import app, Post, PostSchema, db
from flask import request, jsonify
from flask_restful import Api, Resource 
#from app import datab
import random
from  sqlalchemy.sql.expression import func, select


from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

from flasgger import Swagger
from flasgger.utils import swag_from
from flask_restful_swagger import swagger

api = Api(app)

limiter = Limiter(app, key_func=get_remote_address)
limiter.init_app(app)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/doc')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

#Post an Api from all the categorys

class PostResource(Resource):
    def post(self):
        new_post = Post(
            category=request.json['category'],
            note=request.json['note']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

api.add_resource(PostResource, '/posts')


# Get all Api in the database 
class Get_all_Resource(Resource):
    decorators = [limiter.limit("100/day")]
    @swagger.model
    @swagger.operation(notes='your result')
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)
api.add_resource(Get_all_Resource, '/getall')


#select one random Api in the data base
class GetResource(Resource):
    decorators = [limiter.limit("100/day")]
    @swagger.model
    @swagger.operation(notes='your result')
    def get(self):
        posts = Post.query.order_by(func.random()).limit(1)
        return posts_schema.dump(posts)
api.add_resource(GetResource, '/get')

#select one random Api from all the categorys

class Get_id_Resource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

api.add_resource(Get_id_Resource, '/get/<int:post_id>')


#Delete Api using id

class DeleteResource(Resource):
    @swagger.model
    @swagger.operation(notes='your result')
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204
api.add_resource(DeleteResource, '/del/<int:post_id>')

#select one random Api from all the categorys
class Get_category_Resource(Resource):
    decorators = [limiter.limit("100/day")]
    @swagger.model
    @swagger.operation(notes='your result')
    def get(self,category):
        posts = Post.query.filter(Post.category.endswith(category)).order_by(func.random()).limit(1)
        return posts_schema.dump(posts)
api.add_resource(Get_category_Resource, '/get/category/<string:category>')

