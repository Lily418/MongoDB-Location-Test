import urllib2
import json



req = urllib2.Request(url  = "http://127.0.0.1:5000/users?lat=52.905479&long=0.527344&limit=2")

req.add_header('Content-Type', 'application/json')

f = urllib2.urlopen(req)

print f.read()


