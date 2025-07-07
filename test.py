import requests


URL = "http://127.0.0.1:5000/lucky_colors"

payload = {
    "user_id": "68658d3cd3ecdca4fe06e62d"
}

response = requests.post(URL, json=payload)

print("Status Code:", response.status_code)
print("Raw Response Text:")
print(response.text)

