'''
Tudor Boran
August 17, 2016

This is a python script that queries the Wolfram Alpha API to populate a data set. To begin, we will be using crime statistics for some us cities

APP ID-
' TT8EJW-E7K35T3VUA '

'''

import collections
import xml.etree.cElementTree as etree
import requests 

def read_city_names(fname):
	#
	#	This function reads the names of cities from 'fname'.
	#	Cities should be in format City, State\n
	#
	location = collections.namedtuple('Location', ['city','state'])
	places = []
	with open(fname, 'r') as infile:
		for line in infile:
			text = line.split(', ')
			text[1] = text[1][0:-1]						#strip the newline character
			places.append(location(text[0], text[1]))
	return places
	
def make_api_call(question):
	#
	#	This function makes an API call to Wolfram Alpha using 'question' as the query
	#	It returns a string output - in XML
	#
	return True

def  murder_rate_from_file(fname):
	#	This function gets the murder rate per 100,000 people from a file, 'fname' that is in XML format
	#
	i = 0
	with open(fname, 'r') as f:
		tree = etree.parse(f)
	root = tree.getroot()
	for element in root.iter("plaintext"):
		i += 1
		if(i == 2):
			rate = element.text.split()
			return rate[0]
	return 0

def check_cache(cityname, query):
	#
	#	This function checks cache.xml for an entry 'city' in 'cities', then goes to 'data' in 'city' and checks if there's an entry for 'query'
	#	 if it doesn't find it, it returns 'no_entry'
	#
	tree = etree.parse('cache.xml')
	root = tree.getroot()
	for city in root.iter("city"):
		one_city = False								#one_city is used to flag when we find current name == cityname		
		for element in city:
			if(element.tag == 'name'):
				if(element.text == cityname):
					print(element.text)
					one_city = True
			if(element.tag == query) and (one_city):	#one_city is only true for a single 'city' parent element; the city we search for 
				return element.text
	return 'no_entry'
	
def add_city_to_cache(city):
	#
	#	This function reads cache.xml and writes a new entry <city name='city'> </city>
	#
	doc = etree.parse('cache.xml')
	root = doc.getroot()
	num_cities = len(root.findall('city'))
	e_city = Element('city')
	e_name = Element('name')
	e_name.text = city
	e_city.append(e_name)
	root.insert(num_cities, e_city)
	doc.write('cache.xml', xml_declaration=True)
	
	
locations = read_city_names('Cities.txt')
for place in locations:
	print('City: ', place[0], ', ', place[1])

print(murder_rate_from_file('NYCExample.xml'))
print("Checking cache for New York City, murder: ")
print(check_cache('Chicago', 'murders'))
add_city_to_cache('Gadsden')