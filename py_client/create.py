import requests

headers = {'Authorization': 'Bearer 55396c49fba2309fa4e85f04896f25fb9a6caed4'}
endpoint = "http://localhost:8000/api/products/"

data = {
    "title": "Rapsodo MLM1 Mobile Launch Monitor.",
    "content": "Mobile launch monitor by Rapsodo Inc.",
    "price": 39.99,
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())
