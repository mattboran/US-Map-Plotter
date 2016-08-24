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
	
#Assemble data:
str_y_lon = property_from_cache('longitude')
str_x_lat = property_from_cache('latitude')
y_lon = [float(p) for p in str_y_lon]
x_lat = [float(p) for p in str_x_lat]
#need to get whatever property we're plotting and normalize it w/ min-max
query = 'murders'
str_props = property_from_cache(query)
properties = [float(p) for p in str_props]

#Here we convert to 'np' format for matplotlib through numpy
lat_min = min(x_lat)
lat_max = max(x_lat)
lon_min = min(y_lon)
lon_max = max(y_lon)
prop_min = min(properties)
prop_max = max(properties)

spatial_resolution = 0.52

x = np.array(x_lat)
y = np.array(y_lon)
z = np.array(properties)
xinum = (lat_max - lat_min)/spatial_resolution	
yinum = (lon_max - lon_min)/spatial_resolution
xi = np.linespace(lat_min, lat_max + spatial_resolution, xinum)
yi = np.linespace(lon_min, lon_max + spatial_resolution, xinum)

xi,yi = np.meshgrid(xi, yi)
zi = griddata(x, y, z, xi, yi)

map = Basemap(llcrnrlon=-120, llcrnrlat = 20.3, urcrnrlon =-60, urcrnrlat =52.0, 
resolution = 'l', projection = 'tmerc', lat_0 = 35.15, lon_0 = -90.5)

map.drawmapboundary(fill_color='aqua')
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)

map.fillcontinents(color='coral', lake_color='aqua')

map.drawmeridians(np.arange(0,360,15))
map.drawparallels(np.arange(-90,90,15))

lat, lon = map.makegrid(zi.shape[1], zi.shape[0])
x,y = map( lat, lon)
map.contourf(x, y, zi)

#map.plot(x,y, marker='C', color='r')

plt.title('Property plotted on US Map')
plt.show()