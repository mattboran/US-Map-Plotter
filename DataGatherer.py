'''
Tudor Boran
August 17, 2016

This is a python script that queries the Wolfram Alpha API to populate a data set. To begin, we will be using crime statistics for some us cities

APP ID-
' TT8EJW-E7K35T3VUA '

http://api.wolframalpha.com/v2/query?appid=TT8EJW-E7K35T3VUA&input=murder%20rate%20in%20springfield%2C%20massachussets&format=plaintext

'''

import collections, requests, re
import unicodedata as unicode
import lxml.etree as etree #includes XPath

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
	
def make_api_call(city, state, query, over_write):
	#
	#	This function makes an API call to Wolfram Alpha using 'query' as the query, about 'city, state'
	#	query is a space-separated series of words i.e. 'murder rate' or 'tornado frequency' etc
	#	It returns a string output - in XML
	#
	#	http://api.wolframalpha.com/v2/query?appid=TT8EJW-E7K35T3VUA&input=murder%20rate%20in%20springfield%2C%20massachussets&format=plaintext
	#
	
	url = 'http://api.wolframalpha.com/v2/query?appid=TT8EJW-E7K35T3VUA&input='
	
	#first check cache if over_write is false, and if the object exists, break and return false
	if(not over_write):
		newquery = ''
		if(query == 'murder rate'):
			newquery = 'murders'
		else:
			newquery = query
		if(check_cache(city, newquery) != 'no_entry'):
			return False
	
	#assemble the query URL
	_query = query.split(' ')
	for word in _query:
		url += (word + '%20')
	
	_city = city.split(' ')
	for word in _city:
		url += (word+'%20')
	url = url[:-1]
	url += 'C%20'
	
	_state = state.split(' ')
	for word in _state:
		url += (word+'%20')
	url = url[:-3]
	url += '&format=plaintext'
	
	#print attempt to console
	print("Making api call for \'%s in %s, %s\' " % (query, city, state))
	print("The URL we're hitting is %s" % (url))
	#make request to server
	api_call = requests.get(url, stream=True)
	if(api_call.status_code != 200):
		print("API call failed, status code %s " % (str(api_call.status_code)))
		return False
	#else, API call went successfully and returned a result of 'content-type' text/xml in charset=utf-8
	else:	
		with open('temp.dat', 'wb') as fd:		#write results to temp.dat
			for chunk in api_call.iter_content(256):
				fd.write(chunk)

	if(query == 'murder rate'):
		query = 'murders'
	#first check if the city, alone is in the cache. if not, let's add it
	if(check_cache(city, 'no_query') == 'no_entry'):
		print('Adding city %s to cache' % (city))
		add_city_to_cache(city)
	#we've added the city or it was already there. is the state field populated?
	if(check_cache(city, 'state') == 'no_entry'):
		print('Adding state %s to cache' % (state))
		add_entry_to_city(city, 'state', state, True)
	#now add the property from the query we made as a series of if-then's
	if(query == 'murders'):
		add_entry_to_city(city, query, murder_rate_from_file('temp.dat'), True)
	elif(query == 'latitude'):
		add_entry_to_city(city, query, latitude_longitude_from_file('temp.dat', 'latitude'), True) 
	elif(query == 'longitude'):
		add_entry_to_city(city, query, latitude_longitude_from_file('temp.dat', 'longitude'), True) 
	
	print('Adding property %s to cache' % (query))
	
	return True
	
def make_many_api_calls(citylist, statelist, querylist, over_write):
	#
	#	This function,for each city and state in citylist and statelist, each query in querylist. Before making any single city,state query
	#	the cache should be checked. If the entry exists in cache, then the call should either be made or not made based on over_writelist
	#
	
	#error handling
	if(len(citylist) != len(statelist)):
		print('Citylist and statelist different lengths, please check format and try again.\n')
		return False
	
	for i in range(len(citylist)):
		if(make_api_call(citylist[i], statelist[i], querylist, over_write)):
			print('Successfully made API call.\n')
		else:
			print('Call failed.\n')
	
def  murder_rate_from_file(fname):
	#
	#	This function gets the murder rate per 100,000 people from a file, 'fname' that is in XML format; this is
	#	specific to the returns we get from querying Wolfram Alpha with 'murder rate in xxx, yyy' where xxx is city and yyy is state
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
	
def latitude_longitude_from_file(fname, lat_or_long):
	#
	#	This function gets the latitude or longitude of a city from the return from Wolfram Alpha
	#	This function requires you to have the correct file in place with correct lat/long data.
	#	That is, it makes the assumption you know what's in the file
	#
	parser = etree.XMLParser(remove_blank_text=True)
	with open(fname, 'r') as f:
		tree = etree.parse(f, parser)
	root = tree.getroot()
	location = ''
	i = 0
	for element in root.iter("plaintext"):
		i += 1
		if(i == 2):
			loc = element.text.replace('\xc2', '')
			loc = loc.split(" ")
			position1 = loc[0].find('°')
			position2 = loc[1].find('\'')
			location += loc[0][0:position1]
			location += '.'
			location += loc[1][0:position2]
	
	print('%s = %s' % (lat_or_long, location))
	non_decimal = re.compile(r'[^\d.]+')
	non_decimal.sub('', location)
	return location
	
def check_cache(cityname, query):
	#
	#	This function checks cache.xml for an entry 'city' in 'cities', then goes to 'data' in 'city' and checks if there's an entry for 'query'
	#	 if it doesn't find it, it returns 'no_entry'. Query can be 'no_query' to just check cache for the city
	#
	tree = etree.parse('cache.xml')
	root = tree.getroot()
	for city in root.iter("city"):
		one_city = False								#one_city is used to flag when we find current name == cityname		
		for element in city:
			if(element.tag == 'name'):
				if(element.text == cityname):
					one_city = True
					if(query=='no_query'):
						return element.text
			if(element.tag == query) and (one_city):	#one_city is only true for a single 'city' parent element; the city we search for 
				return element.text
				
	return 'no_entry'
	
def add_city_to_cache(city):
	#
	#	This function reads cache.xml and writes a new entry <city name='city'> </city>
	#
	
	#in order to prettify the output, we need to do the following with the XML parser
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse('cache.xml', parser)
	root = tree.getroot()
	for city_elements in root.iter('name'):
		if (city_elements.text == city):
			print("%s is already in the cache as a city entry!" % (city))
			return False
			
	num_cities = len(root.findall('city'))
	
	e_city = etree.Element('city')
	e_name = etree.Element('name')
	e_name.text = city
	e_city.append(e_name)
	
	root.insert(num_cities, e_city)
	tree.write('cache.xml', pretty_print=True)
	
	return True

def add_entry_to_city(city, property, value, over_write):
	#
	#	This method adds a property (attribute) and value (text) as sub-element to the city element specified. We assume there are not any duplicate
	#	city names. At this point. This will be ameliorated at a later point, so we can have similar-named cities from different states
	#	
	#	over_write may be either 'True' or 'False'; if False, property is not overwritten if it already exists
	#
	#	This may be slow
	#
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse('cache.xml', parser)
	root = tree.getroot()
	e_prop = etree.Element(property)
	e_prop.text = value
	#first check to see if the city is in the list
	#we will use the XPath object 'finder' to utilize XPath for this purpose
	finder = tree.xpath('//data/city/name/text()')
	has_element = False
	
	if city not in finder:
		print("City %s not found in cache file." % (city))
		return False
	else:
		i = 0
		for cityname in finder:
			if cityname==city:
				break
			else:
				i += 1
	#get the parent 'city' block as city_root
	city_root = finder[i].getparent().getparent()
	#cycle through its children, re-assigning value if over_write = True
	for element in city_root: 
		if(element.tag == property):
			has_element = True
			if(not over_write):
				return False
			else:
				element.text = value
				break
		
	if(not has_element):
		city_root.append(e_prop)
	
	tree.write('cache.xml', pretty_print=True)
	return True



'''
for i in range(len(cities)):
	if(check_cache(cities[i], 'no_query') == 'no_entry'):
		print('Adding city %s to cache' % (cities[i]))
		#add_city_to_cache(city)
	#we've added the city or it was already there. is the state field populated?
	if(check_cache(cities[i], 'state') == 'no_entry'):
		print('Adding state %s to cache under entry for city %s' % (states[i], cities[i]))
		#add_entry_to_city(city, 'state', state, True)
	#now add the property from the query we made as a series of if-then's
	if(check_cache(cities[i], 'murders') == 'no_entry'):
		print('Adding property %s to cache' % ('murder'))
	#	add_entry_to_city(city, query, murder_rate_from_file('temp.dat'), True)
'''