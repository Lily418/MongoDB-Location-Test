from flask import Flask, request
import json
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
mongo = PyMongo(app)

#curl -H "Content-Type: application/json" --data '{"user":"Joel"}' http://127.0.0.1:5000/user/
@app.route('/user/', methods=['GET', 'POST'])
def user():
	if request.method == "POST":
		data = json.loads(request.data)
	        id = mongo.db.users.insert(data)	
		return json.dumps({"id": str(id)}) 	
	elif request.method == "GET":
		users = []
		for user in mongo.db.users.find():
			user['_id'] = str(user['_id'])
			users.append(user)

		return json.dumps(users)

@app.route('/user/<id>', methods=['POST', 'GET'])
def userid(id):
	if request.method == "POST":
		mongo.db.users.update({'_id': ObjectId(id)}, {"$set": json.loads(request.data)})
		return ""
	elif request.method == "GET":
		record = mongo.db.users.find_one({"_id" : ObjectId(id)})
		record["_id"] = str(record["_id"])
		return json.dumps(record)
	 

@app.route('/location/<id>', methods=['POST', 'GET'])
def location(id):
	if request.method == "POST":
		data = json.loads(request.data)
		mongo.db.users.update({"_id": ObjectId(id)}, {"$set" : {"lang" : data['lang'], "long" : data['long']}})
		return ""
	elif request.method == "GET"
		pass




if __name__ == "__main__":
	app.run(debug=True, port=5000)
