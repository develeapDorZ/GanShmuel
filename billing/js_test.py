import json

data = None
with open("json-mock-weights.json") as f:
    data = json.load(f)

#print(data)

#print(data[0]['id'])

for entry in data:
    print(entry['id'])