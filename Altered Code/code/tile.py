#Commented by Luc Bourassa, ID 21027232
#This file is for a module that creates a class of objects called tile. 

import pygame 
from settings import *

#Creates a class for the different layers of images being initialized on the map. The base layer of the map is called the floor, and the layer of images above is called the object layer
class Tile(pygame.sprite.Sprite):
	#A function that labels and separates the objects of the tile class
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		#Initializes the attributes of each object in the tile class
		super().__init__(groups)
		#Finds and sets a sprite type to the object in the class
		self.sprite_type = sprite_type
		#Uses the hitbox offset dictionary in the settings module to find a corresponding value for each type of object in the class
		y_offset = HITBOX_OFFSET[sprite_type]
		#Locates an image sprite for every object in the tile class based on its layer
		self.image = surface
		#If statement to separate out objects of a sprite type other than that of the floor, so that they are generated after the floor, on top of the floor
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
		#Sets hitboxes used for collision detection of the floor layer, which is spots where the character cannot move such as cliffs and sides of bridges.
		else:
			self.rect = self.image.get_rect(topleft = pos)
		#Sets hitboxes for collision detection of all objects in the tile class
		self.hitbox = self.rect.inflate(0,y_offset)
