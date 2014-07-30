#!/usr/bin/python
import csv
import math

countryDict = {}

def read_file(filename):
    with open(filename, 'rb') as f:
        countries = csv.reader(f, delimiter=',', quotechar='|')
        next(countries, None) #skip header
        for alpha, lat, lon, fname in countries:
            if (len(lat) > 0 and len(lon) > 0):
                countryDict[fname] = Country(fname, alpha, float(lat), float(lon))

def write_matrix(filename):
    countries_unsorted = [x for x in countryDict.values()]
    countries = sorted(countries_unsorted, key=lambda x: x.iso_code)

    first_line = ['']
    for country in countries:
        first_line.append(country.iso_code)
       
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',', quotechar='|')
        writer.writerow(first_line)
        for country in countries:
            row = [country.iso_code]
            for other_country in countries:
                row.append(country.distanceTo(other_country))
            writer.writerow(row)

class Distance():
    def __init__(self, countryA, countryB, distance_km):
        self.countryA = countryA
        self.countryB = countryB
        self.distance_km = distance_km

    def __str__(self):
        return ", ".join([self.countryA.iso_code, self.countryB.iso_code, str(self.distance_km)])

class Country():
    def __init__(self, fname, iso_code, lat, lon):
        self.fname = fname
        self.iso_code = iso_code
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
    write_matrix("distance-matrix.csv")

    """
    for country in countryDict.values():
        print country.iso_code,
        
    for countryA in countryDict.values():
        for countryB in countryDict.values():
            print Distance(countryA, countryB, countryA.distanceTo(countryB))
    """
    
    

