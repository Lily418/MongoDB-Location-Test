import json

from flask              import Flask, request, Response
from flask.ext.pymongo  import PyMongo
from werkzeug.routing   import BaseConverter
from bson.objectid      import ObjectId

class ObjectIdConverter(BaseConverter):
  def to_python(self, value):
    return ObjectId(value)


def user_location(id):
  return {"Location": "/users/" + str(id)}

app = Flask(__name__)
app.url_map.converters['objectid'] = ObjectIdConverter
mongo = PyMongo(app)

#curl -H "Content-Type: application/json" --data '{"user":"Joel"}' http://127.0.0.1:5000/users/
@app.route('/users', methods=['GET'])
def users_get():
  users = []
  for user in mongo.db.users.find():
    user['_id'] = str(user['_id'])
    users.append(user)
  return json.dumps(users)

@app.route('/users', methods=['POST'])
def users_post():
  id = mongo.db.users.insert(json.loads(request.data))
  return Response(status=201, headers=user_location(id))

@app.route('/users/<objectid:id>', methods=['GET'])
def user_get(id):
  record = mongo.db.users.find_one(id)
  record["_id"] = str(record["_id"])
  return Response(status=200,
                  response=json.dumps(record),
                  headers=user_location(id)
                 )

@app.route('/users/<objectid:id>', methods=['POST'])
def user_post(id):
  mongo.db.users.update({'_id': id}, {"$set": json.loads(request.data)})
  return ""

if __name__ == "__main__":
	app.run(debug=True, port=5000)
