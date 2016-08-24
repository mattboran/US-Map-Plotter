from DataGatherer import *
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def take_action():
	locations = read_city_names('Cities.txt')
	i = 0
	states = []
	cities = []
	numcities = 5
	for location in locations:
		if(i == numcities):
			break
		states.append(location[1])
		cities.append(location[0])
		print('City: %s, state: %s' % (location[0], location[1]))
		i+=1
	make_many_api_calls(cities, states, 'latitude', False)
	make_many_api_calls(cities, states, 'longitude', False)
	make_many_api_calls(cities, states, 'murder rate', False)
	
map = Basemap(llcrnrlon=-120, llcrnrlat = 20.3, urcrnrlon =-60, urcrnrlat =52.0, 
	resolution = 'l', projection = 'tmerc', lat_0 = 35.15, lon_0 = -90.5)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral', lake_color='aqua')
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)

x,y = map( -73.56, 40.39)

map.plot(x,y, marker='D', color='r')

plt.title('Property plotted on US Map')
plt.show()