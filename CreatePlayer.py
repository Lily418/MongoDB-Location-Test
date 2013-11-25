import urllib2
import json


user = {"user" : "Joel",
        "loc"  : [38.804329, 89.296875]}

req = urllib2.Request(url  = "http://zombies-game.herokuapp.com/users",
                      data = json.dumps(user))

req.add_header('Content-Type', 'application/json')

f = urllib2.urlopen(req)

print f.read() 

