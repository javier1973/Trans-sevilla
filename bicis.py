from requests import requests
r = requests.get(" http ://open.mapquestapi.com/xapi/api/0.6/node [amenity=bicycle_rental ][ bbox = -6.0838,37.3074,-5.8249 ,37.4653]")

print r.text