import json
import urllib.request

url = 'http://localhost:5000/api/text/default'
data = {'text': 'This is a text input.'}
header = {'Content-Type': 'application/json'}

req = urllib.request.Request(url, json.dumps(data).encode(), header)
f = urllib.request.urlopen(req)
response = f.read()
f.close()

print(response)