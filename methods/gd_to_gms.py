import googlemaps
import requests
import pymysql


response = requests.get(f'https://nominatim.openstreetmap.org/reverse.php?lat=20.7322075&lon=-100.71946&zoom=16&format=jsonv2')


a = response.json()

print(a['address']['postcode'])
