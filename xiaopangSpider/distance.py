#%%
import pandas as pd
from urllib.parse import urlparse, parse_qs
import requests
mimi = '121.508884,31.242874'
peng = '121.581063,31.184638'

df=pd.read_csv('houselist1.csv', delimiter=',', encoding='gb18030')

#%%
def decode_map(url):
  fragment = parse_qs(urlparse(url).fragment)
  coordinates=f"{fragment['lng'][0]},{fragment['lat'][0]}"
  return coordinates
df['coordinates'] = df.apply(lambda x: decode_map(x['mapLink']), axis=1)


#%%

def get_distance(origin, destination):
  apikey='5d2702adb45071fcd711e23c47063eb9'
  apiurl='https://restapi.amap.com/v5/direction/driving'
  
  data = {
    'key': apikey,
    'origin': origin,
    'destination': destination
  }
  r = requests.post(apiurl, params=data)
  result = r.json()
  if result['infocode'] == '10000':
    # OK
    route = result['route']
    taxi_cost = route['taxi_cost']
    distance = int(route['paths'][0]['distance'])/1000
    # print(f"Taxi cost: {taxi_cost} Distance: {distance}")
    return distance, taxi_cost
  else:
    return 0, 0


#%%
df['peng'] = df.apply(lambda x: get_distance(x['coordinates'], peng), axis=1)
# df[['peng', 'distance']] = get_distance(df['coordinates'], peng)
df['mimi']= df.apply(lambda x: get_distance(x['coordinates'], mimi), axis=1)


# %%

for index, row in df.iterrows():
  coordinates = row['coordinates']
  df[['peng_distance', 'peng_taxi']]= get_distance(coordinates, peng)
  #row[['mimi_distance', 'mimi_taxi']]= get_distance(coordinates, mimi)

# %%
df
# %%
