import requests

url = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"

querystring = {"sign":"aquarius","day":"today"}

payload = {}
headers = {
	"x-rapidapi-key": "4a2872055fmsh4ec7d0c02ff86bcp1bad27jsnf26e1b5be680",
	"x-rapidapi-host": "sameer-kumar-aztro-v1.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, params=querystring)

print(response.json())