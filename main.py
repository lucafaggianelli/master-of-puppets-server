#!/usr/bin/env python

import json
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "mop"
mongo = PyMongo(app, config_prefix='MONGO')


class Document(Resource):

  def get(self, id=None):
    if id is None:
      cursor = mongo.db.docs.find({}, {"update_time": 0}).limit(10)
      data = []
      for doc in cursor:
        print doc
        doc['url'] = url_for('document', id=doc.get('_id'))
        data.append(doc)

      return toJson(data)

    else:
      doc = mongo.db.docs.find_one_or_404({'_id': ObjectId(id)})
      return toJson(doc)

  def post(self, id=None):
    data = {'name': request.form['name']}
    print data
    result = mongo.db.docs.insert_one(data)

    return result.inserted_id


def toJson(data):
  return json.dumps(data, default=json_util.default)


api = Api(app)
api.add_resource(Document, '/api/docs/', endpoint='documents')
api.add_resource(Document, '/api/docs/<string:id>')


if __name__ == "__main__":
    app.run(debug=True)
