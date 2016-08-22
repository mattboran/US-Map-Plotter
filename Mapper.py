from DataGatherer import *
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

locations = read_city_names('Cities.txt')
print(locations['city'])
#make_api_call('Los Angeles', 'California', 'murder rate')
i = 0
states = []
cities = []
for location in locations:
	states.append(location[1])
	cities.append(location[0])
	print('City: %s, state: %s' % (location[0], location[1]))
	
make_many_api_calls(cities, states, 'latitude', False)