import requests

# api key for favqs
API_KEY = "9df9615581a3be73714e017f9b7f87b4"

# url for favq quotes api
API_URL = "https://favqs.com/api/quotes"

# headers for using api
headers = {
"Authorization": f"Bearer {API_KEY}"
}

response = requests.get(API_URL, headers=headers)
response_json = response.json()