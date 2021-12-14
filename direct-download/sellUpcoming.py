#
import requests
from bs4 import BeautifulSoup 
import json
import pandas as pd

reqUrl = "http://localhost:8050/render.html?url=http://www.fangdi.com.cn/service/freshHouse/getSellUpcoming.action&timeout=10&wait=0.5"

headersList = {
 "Accept": "application/json",
 "User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion",
 "Content-Type": "application/json",
 "Referer" : "http://www.fangdi.com.cn"
}

payload = ""

response = requests.request("GET", reqUrl, data=payload, headers=headersList)

# print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
body = soup.body.text
data = json.loads(body)
json_name = 'sellUpcoming.json'
csv_name = 'sellUpcoming.csv'

with open(json_name, 'w', encoding='utf8') as f:
  json.dump(data['listSellUpcoming'], f, ensure_ascii=False)

df = pd.read_json(json_name)
df.to_csv(csv_name, index=None)