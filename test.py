import requests

# Adjust if your server is on a different port
url = "http://127.0.0.1:5000/predict"

# Example zodiac signs to test
payload = {
    "sign1": "pisces",
    "sign2": "Leo"
}

# Make the POST request
response = requests.post(url, json=payload)

# Display the results
if response.ok:
    data = response.json()
    print("✅ Prediction Result:")
    print(f"- Sign 1: {data.get('sign1')}")
    print(f"- Sign 2: {data.get('sign2')}")
    print(f"- Compatibility Score: {round(data.get('compatibility_score', 0) * 100, 2)}%")

    
    if "descriptions" in data:
        print("\nDescriptions:")
        for rel_type, desc in data["descriptions"].items():
            print(f"{rel_type}: {desc}")
else:
    print("❌ Error:")
    print(response.status_code, response.text)


