import requests, urllib

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4"

user_agent = urllib.quote_plus(user_agent)

r = requests.get('https://useragentapi.com/api/v3/json/8c21e71c/'+user_agent)

print r.json()
