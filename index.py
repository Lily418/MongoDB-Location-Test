import json

from flask              import Flask, request, Response
from flask.ext.pymongo  import PyMongo
from werkzeug.routing   import BaseConverter
from bson.objectid      import ObjectId
from pymongo            import GEO2D

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
  query = {}
  users = []

  longitude = request.args.get("long")
  latitude = request.args.get("lat")
  limit = request.args.get("limit")
  limit = int(limit) if limit else 0

  if (longitude and latitude):
    query["loc"] = {
      "$near": [latitude, longitude]
    }

  for user in mongo.db.users.find(query, limit=limit):
    user['_id'] = str(user['_id'])
    users.append(user)
  return json.dumps(users)

@app.route('/users', methods=['POST'])
def users_post():
  print(request.data)
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

@app.route('/createindex')
def create_index():
	mongo.db.users.create_index([("loc", GEO2D)])


if __name__ == "__main__":
	app.run(debug=True, port=5000)
