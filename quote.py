import requests

url = "https://zenquotes.io/api/today"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

today_quote = response.text