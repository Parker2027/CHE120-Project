#imports the pygame module
import pygame 
#imports everything about game window settings from settings1.py into level1.py
from settings import *
#imports Tile from tile1.py into level1.py
from tile import Tile
#imports Player from player1.py
from player import Player


class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		#sprites that at vis
		self.visible_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
				if col == 'p':
					Player((x,y),[self.visible_sprites])

	def run(self):
		# update and draw the game
		self.visible_sprites.draw(self.display_surface)
