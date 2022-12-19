from http import HTTPStatus
from flask import (
    request, g,
    json
)
from flask_restful import Resource
from bson import ObjectId
import bson.json_util as json_util

from .auth import login_required
from ..utils.db import get_db
from ..utils.handler import SPSError, ErrorType


class BlogList(Resource):

    method_decorators = [login_required]

    def get(self):
        """
        Get all blogs

        Endpoint to get all blogs
        ---
        tags:
            - blogs
        responses:
            200:
                description: A list of blogs
                body:
                    application/json:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    _id: string
                                    title: string
                                    body: string
            400:
                description: Bad request
        """
        db = get_db()
        blogs = db.blogs.find().sort('created', -1)
        blogs = json_util.dumps(blogs)
        return json.loads(blogs), HTTPStatus.OK

    def post(self):
        """
        Create a blog

        Endpoint to create a blog
        ---
        tags:
            - blogs
        responses:
            201:
                description: Created id of the blog
            400:
                description: Bad request
        """
        title = request.json['title']
        body = request.json['body']

        if not title:
            raise SPSError(*ErrorType.TITLE_REQUIRED.value)

        db = get_db()
        result_id = db.blogs.insert_one({
            'title': title,
            'body': body,
            'author': g.user['username'],
        }).inserted_id
        return {'id': result_id.__str__()}, HTTPStatus.CREATED


class BlogDetail(Resource):

    method_decorators = [login_required]

    def get_blog(self, id, check_author=True):
        blog = get_db().blogs.find_one({'_id': ObjectId(id)})
        if blog is None:
            raise SPSError(*ErrorType.BLOG_NOT_FOUND)
        if check_author and blog['author'] != g.user['username']:
            raise SPSError(*ErrorType.INVALID_CREDENTIALS.value)
        return blog

    def get(self, id):
        """
        Get a blog

        Endpoint to get a blog
        ---
        tags:
            - blogs
        responses:
            200:
                description: A blog
                body:
                    application/json:
                        schema:
                            type: object
                            properties:
                                _id: string
                                title: string
                                body: string
            400:
                description: Bad request
            404:
                description: Blog not found
        """
        blog = self.get_blog(id)
        blog = json_util.dumps(blog)
        return json.loads(blog), HTTPStatus.OK

    def put(self, id):
        """
        Update a blog

        Endpoint to update a blog
        ---
        tags:
            - blogs
        responses:
            200:
                description: A blog
                body:
                    application/json:
                        schema:
                            type: object
                            properties:
                                _id: string
                                title: string
                                body: string
            400:
                description: Bad request
            404:
                description: Blog not found
        """
        blog = self.get_blog(id)
        body = request.json['body'] or blog['body']
        title = request.json['title']
        if not title:
            raise SPSError(*ErrorType.TITLE_REQUIRED.value)

        db = get_db()
        db.blogs.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'title': title, 'body': body}}
        )
        updated_blog = self.get_blog(id)
        updated_blog = json_util.dumps(updated_blog)
        return json.loads(updated_blog), HTTPStatus.OK

    def delete(self, id):
        """
        Delete a blog

        Endpoint to delete a blog
        ---
        tags:
            - blogs
        responses:
            204:
                description: No content
            400:
                description: Bad request
            404:
                description: Blog not found
        """
        _ = self.get_blog(id)
        db = get_db()
        db.blogs.delete_one({'_id': ObjectId(id)})
        return HTTPStatus.NO_CONTENT
