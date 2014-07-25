#!/usr/bin/python
import csv
import math

countryDict = {}
countryDistance = []

def read_file(filename):
    with open(filename, 'rb') as f:
        countries = csv.reader(f, delimiter=',', quotechar='|')
        next(countries, None) #skip header
        for alpha, lat, lon, fname in countries:
            if (len(lat) > 0 and len(lon) > 0):
                countryDict[fname] = Country(fname, float(lat), float(lon))

class Distance():
    def __init__(self, countryA, countryB, distance_km):
        self.countryA = countryA
        self.countryB = countryB
        self.distance_km = distance_km

    def __str__(self):
        return ", ".join([self.countryA.fname, self.countryB.fname, str(self.distance_km)])

class Country():
    def __init__(self, fname, lat, lon):
        self.fname = fname
        self.latitude = lat
        self.longitude = lon

    #haversine
    def distanceTo(self, otherCountry):
        earth_radius = 6371 #kilometers
        theta1 = math.radians(self.latitude)
        theta2 = math.radians(otherCountry.latitude)
        delta_lat = math.radians(otherCountry.latitude - self.latitude)
        delta_lon = math.radians(otherCountry.longitude - self.longitude)

        a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + \
            math.cos(theta1) * math.cos(theta2) * \
            math.sin(delta_lon/2) * math.sin(delta_lon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return earth_radius * c;
        

if __name__ == '__main__':
    read_file("google-country.csv")

    for countryA in countryDict.values():
        for countryB in countryDict.values():
            distance = Distance(countryA, countryB, countryA.distanceTo(countryB))
            #countryDistance.append(distance)
            print distance
    
    

