import geopandas as gpd
import re

MAP_FILES = (
             './assets/maps_shp/country.shp', 
             './assets/maps_shp/voivodeships.shp', 
             './assets/maps_shp/counties.shp'
            )

# deriving file names from MAP_FILES array
FILE_NAMES = [re.split('/', map_file) for map_file in MAP_FILES]
FILE_NAMES = ([splitted_list[-1][:-4] for splitted_list in FILE_NAMES])
FILE_LIST = []

print(FILE_NAMES)

# reformatting .shp map files into .geojson map files
def reformatter(shp_map_list):
    for num, map in enumerate(shp_map_list):
        
        shp_map_file = gpd.read_file(map)
        shp_map_file.to_file(f'./assets/maps_geojson/{FILE_NAMES[num]}.geojson', driver = 'GeoJSON')
               
reformatter(MAP_FILES)