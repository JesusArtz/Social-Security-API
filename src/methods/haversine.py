import numpy as np
import math
import random


r = 6371000


def haversine(lat1, lon1, lat2, lon2):

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return c * r


def randlatlon1():
    pi = math.pi
    cf = 180.0 / pi

    gx = random.gauss(0.0, 1.0)
    gy = random.gauss(0.0, 1.0)
    gz = random.gauss(0.0, 1.0)

    norm2 = gx*gx + gy*gy + gz*gz
    norm1 = 1.0 / math.sqrt(norm2)
    x = gx * norm1
    y = gy * norm1
    z = gz * norm1

    radLat = math.asin(z)
    radLon = math.atan2(y, x)

    return (round(cf*radLon, 5), round(cf*radLat, 5))

lista = []

for i in range(10000):
    lat1, lon1 = randlatlon1()
    lista.append((lat1, lon1))

# save the list in a file to use it in the next step with the format: (lat, lon)
with open('data.txt', 'w') as f:
    for item in lista:
        f.write("%s" % str(item))


from geopy.distance import geodesic

def coordinates_within_distance(coordinates, reference_coordinate, distance):
    within_distance = []
    for lat, lon in coordinates:
        if geodesic(reference_coordinate, (lat, lon)).meters <= distance:
            within_distance.append((lat, lon))
    return within_distance

with open('data.txt', 'r') as f:
    coordenadas = f.read().splitlines()

reference_coordinate = (41.730610, -72.935242)
distance = 500

coordenadas_cercanas = coordinates_within_distance(coordenadas, reference_coordinate, distance)
print(coordenadas_cercanas)
