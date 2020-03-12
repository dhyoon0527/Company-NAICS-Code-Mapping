import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'company name':'david steel company'})

print(r.json())