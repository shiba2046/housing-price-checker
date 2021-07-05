#%%
import pandas as pd
from urllib.parse import urlparse, parse_qs
import requests
mimi = '121.508884,31.242874'
peng = '121.581063,31.184638'

df=pd.read_csv('houselist.csv', delimiter=',', encoding='gb18030')

#%%
def decode_map(url):
  fragment = parse_qs(urlparse(url).fragment)
  coordinates=f"{fragment['lng'][0]},{fragment['lat'][0]}"
  return coordinates
df['coordinates'] = df.apply(lambda x: decode_map(x['mapLink']), axis=1)


#%%

def get_distance(origin, destination, test=True):
  apikey='5d2702adb45071fcd711e23c47063eb9'
  apiurl='https://restapi.amap.com/v5/direction/driving'
  
  data = {
    'key': apikey,
    'origin': origin,
    'destination': destination
  }
  if origin == '0,0':
    print("Error coords, exit")
    return
  if test:
    print(f"Testing for {origin} - {destination}")
    return f"Test Distance {origin} - {destination}", f"Test Taxi {origin} - {destination}"
  else:
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
      return result['infocode'], result


#%%
# df['peng'] = df.apply(lambda x: get_distance(x['coordinates'], peng), axis=1)
# df[['peng', 'distance']] = get_distance(df['coordinates'], peng)
df['mimi']= df.apply(lambda x: get_distance(x['coordinates'], mimi), axis=1)


# %%
area = [
  '嘉定区',
  '奉贤区',
  '宝山区',
  '崇明县',
  '徐汇区',
  '普陀区',
  '杨浦区',
  '松江区',
  '浦东新区',
  '虹口区',
  '金山区',
  '长宁区',
  '闵行区',
  '青浦区',
  '静安区',
  '黄浦区'
  ] 
area_list = [
  '嘉定区',
  '宝山区',
  '徐汇区',
  '普陀区',
  '杨浦区',
  '浦东新区',
  '虹口区',
  '长宁区',
  '闵行区',
  '静安区',
  '黄浦区'
]

df_distance = df.loc[(df['area'].isin(area_list)) & (df['coordinates'] != '0,0'), ['coordinates']]
# df_distance
#%%
df['mimi_taxi'] = df_distance.apply(lambda x: get_distance(x['coordinates'], mimi), axis=1)



# %%

for index, row in df_distance.iterrows():
  print(index, row)
  coordinates = row['coordinates']
  df.loc[index, ['peng_distance_km', 'peng_taxi_cost']]= get_distance(coordinates, peng, False)
  df.loc[index, ['mimi_distance_km', 'mimi_taxi_cost']]= get_distance(coordinates, mimi, False)

# %%
df.to_csv('distance.csv', encoding='gb18030')
# %%
