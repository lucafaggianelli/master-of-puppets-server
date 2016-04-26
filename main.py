#!/usr/bin/env python

import os
import sys
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods


app = Flask(__name__)

app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = 27017,
    MONGODB_DB = 'sibilla',
)

db = MongoEngine(app)
api = MongoRest(app, url_prefix='/api')
app.url_map.strict_slashes = False

class Document(db.Document):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField()
    categories = db.ListField(db.StringField())
    tags = db.ListField(db.StringField())
    files = db.ListField()
    drive = db.StringField()

class DocumentResource(Resource):
    document = Document

    filters = {
        'name': [ops.Exact, ops.Startswith, ops.Contains],
        'description': [ops.Exact, ops.Startswith, ops.Contains],
        'categories': [ops.Exact],
        'tags': [ops.Exact],
    }

@api.register(name='documents', url='/docs/')
class DocumentView(ResourceView):
    resource = DocumentResource
    methods = [methods.Create, methods.Update,
            methods.Fetch, methods.List, methods.Delete]


if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 2:
        port = int(sys.argv[1])

    app.run(host='0.0.0.0', port=port)
