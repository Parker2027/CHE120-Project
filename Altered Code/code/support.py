# This was commented by Parker Bray-Jones (21017290)
# Imports a csv reader from the python module csv
from csv import reader
# Imports walk from the os module (allows python to browse files)
from os import walk
# Imports the pygame module
import pygame

# Creates a function responsible for opening and reading csv files
def import_csv_layout(path):
	# Terrain map is a list containing the position and type of all tiles
	terrain_map = []
	# Opens the specified file and names it 
	with open(path) as level_map:
		# The csv reader interpretes the csv file as a python list
		layout = reader(level_map,delimiter = ',')
		# The function gathers all the rows in the list "layout"
		for row in layout:
			# The empty list from the beginning is appended to contain this list of rows
			terrain_map.append(list(row))
		return terrain_map

# Creates a function that imports all images from a folder
def import_folder(path):
	# Creates a list containing information about images on the map surface
	surface_list = []

	# Looks for .img files in the specified path
	for _,__,img_files in walk(path):
		# For all images in the specified path
		for image in img_files:
			# Concatonate the path name with the folder name to create a reference for the folder
			full_path = path + '/' + image
			# The chosen images are added to the surface of the map
			image_surf = pygame.image.load(full_path).convert_alpha()
			# This data is added to a list that the code can interperate
			surface_list.append(image_surf)

	return surface_list
