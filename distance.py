#!/usr/bin/python
import csv
import math
import sys, argparse

def main(argv, filename):
    parser = argparse.ArgumentParser(description="Calculate distances between two countries")
    parser.add_argument('-o', action="store", dest="output_type", type=str, \
            help="Set format of output.", default="standard")

    args = parser.parse_args()

    read_file(filename)
    
    if args.output_type == "matrix":
        print_matrix()
    else:
        print_standard()
        

def read_file(filename):
    with open(filename, 'rb') as f:
        countries = csv.reader(f, delimiter=',', quotechar='|')
        next(countries, None) #skip header
        for alpha, lat, lon, fname in countries:
            if (len(lat) > 0 and len(lon) > 0):
                countryDict[fname] = Country(fname, alpha, float(lat), float(lon))

def print_standard():
    for countryA in countryDict.values():
        for countryB in countryDict.values():
            print Distance(countryA, countryB, countryA.distanceTo(countryB))


def print_matrix():
    countries_unsorted = [x for x in countryDict.values()]
    countries = sorted(countries_unsorted, key=lambda x: x.iso_code)

    print ",",
    for country in countries:
        print country.iso_code + ", ",
    print ""        
       
    for country in countries:
        row = [country.iso_code]
        for other_country in countries:
            row.append(str(country.distanceTo(other_country)))
        print ', '.join(row) 


class Distance():
    def __init__(self, countryA, countryB, distance_km):
        self.countryA = countryA
        self.countryB = countryB
        self.distance_km = distance_km

    def __str__(self):
        return ", ".join([self.countryA.fname, self.countryB.fname, str(self.distance_km)])

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
    countryDict = {}

    main(sys.argv, "google-country.csv")

