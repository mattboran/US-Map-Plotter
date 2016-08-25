from DataGatherer import *
from mpl_toolkits.basemap import Basemap

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def collect_properties():
	locations = read_city_names('Cities.txt')
	i = 0
	states = []
	cities = []
	numcities = 50
	for location in locations:
		if(i == numcities):
			break
		states.append(location[1])
		cities.append(location[0])
		print('City: %s, state: %s' % (location[0], location[1]))
		i+=1
	#make_many_api_calls(cities, states, 'latitude', True)
	#make_many_api_calls(cities, states, 'longitude', True)
	make_many_api_calls(cities, states, 'murder rate', False)
	
#Assemble data:
str_y_lon = property_from_cache('longitude')
str_x_lat = property_from_cache('latitude')
y_lon = [float(p) for p in str_y_lon]
x_lat = [float(p) for p in str_x_lat]
#reverse latitude values
y_lon = [-p for p in y_lon]

#need to get whatever property we're plotting and normalize it w/ min-max
query = 'murders'
str_props = property_from_cache(query)
properties = [float(p) for p in str_props]

prop_min = min(properties)
prop_max = max(properties)

#min-max normalized property values
prop_minmax = [(p - prop_min)/(prop_max - prop_min) for p in properties]
marker_sizes = [int(p * 16)+4 for p in prop_minmax]

map = Basemap(llcrnrlon=-120, llcrnrlat = 20.3, urcrnrlon =-60, urcrnrlat =52.0, 
resolution = 'l', projection = 'tmerc', lat_0 = 35.15, lon_0 = -90.5)

map.drawmapboundary(fill_color='aqua')
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)

map.fillcontinents(color='coral', lake_color='aqua')

x, y = map(y_lon, x_lat)

for i in range(len(x)):
	map.plot(x[i], y[i],  'bo', markersize = marker_sizes[i])

#map.scatter(x, y, 3, marker='o',color='b')

cols = ['r' for p in prop_minmax]

plt.title('Property plotted on US Map')
plt.show()