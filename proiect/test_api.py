import requests
import json

url = "http://127.0.0.1:8000/employee/"

payload = json.dumps({
  "name": "test1",
  "alias": "aliastest1"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
