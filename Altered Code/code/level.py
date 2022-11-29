# Imports the pygame module
import pygame 
# Imports everything from the file settings.py
from settings import *
# Imports class Tile from the file tile.py
from tile import Tile
# Imports class Player from the file player.py
from player import Player
# Imports debug from the file depug.py
from debug import debug
# Imports everything from the file support.py
from support import *
# Imports choice and randint from the module random
from random import choice, randint
# Imports class Weapon from the file weapon.py
from weapon import Weapon
# Imports class UI from the file ui.py
from ui import UI
# Imports class Enemy from the file enemy.py
from enemy import Enemy
# Imports class AnimationPlayer from file particles.py
from particles import AnimationPlayer

# Imports class MagicPlayer from file magic.py
from magic import MagicPlayer
# Imports class Upgrade from file upgrade.py
from upgrade import Upgrade

# Creates class Level (graphics and collision for the game map)
class Level:
	# Initiates the class (allows the class to contain arguments)
	def __init__(self):

		# get the display surface 
		# Creates the display (video)
		self.display_surface = pygame.display.get_surface()
		# Sets the default game to not be paused
		self.game_paused = False

		# sprite group setup
		# Viewpoint for sprites
		self.visible_sprites = YSortCameraGroup()
		# Image for sprites is from a group of images
		self.obstacle_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		# Image for sprites is from a group of images
		self.attack_sprites = pygame.sprite.Group()
		# Image for sprites is from a group of images
		self.attackable_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

		# User Interface (HUD)
		self.ui = UI()
		# The level can update as the game progresses
		self.upgrade = Upgrade(self.player)

		# Particles animation
		self.animation_player = AnimationPlayer()
		# Magic animation
		self.magic_player = MagicPlayer(self.animation_player)
		
	# Controls the map layout and graphics
	def create_map(self):
		# Map layout is defined with the following csv files
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
		}
		# Level graphics are defined by the following files
		graphics = {
			'grass': import_folder('../graphics/Grass'),
			'objects': import_folder('../graphics/objects')
		}

		# Whenever the game is loaded
		for style,layout in layouts.items():
			# Counts the current posiyion of the player
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					# For all tiles on the map that the player cannot walk on
					if col != '-1':
						# Horizontal position on the map
						x = col_index * TILESIZE
						# Vertical position on the map
						y = row_index * TILESIZE
						# Creates a boundary around the world to prevent the player from walking off the map
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						# The image for grass is selcted at random
						if style == 'grass':
							# Choses a random grass tile image for any tile set to be grass
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x,y),
								[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
								'grass',
								random_grass_image)
						
						# The image for an object depends on what object is there
						if style == 'object':
							# 
							surf = graphics['objects'][int(col)]
							# Position and image of the object
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
						
						# Whenever an entity is called (An entity is called when their ID is found in the csv files)
						if style == 'entities':
							# If the entity ID is 394 then the player is called
							if col == '394':
								# The player is defined using their location, their sprite, their attacks,and their magic
								# Also allows for collison between the player and obstacles
								self.player = Player(
									(x,y),
									[self.visible_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic)
							else:
								# If the entity ID is 390 then the bamboo monster is created
								if col == '390': monster_name = 'bamboo'
								# If the entity ID is 391 then the spirit monster is created
								elif col == '391': monster_name = 'spirit'
								# If the entity ID is 392 the raccon monster is created
								elif col == '392': monster_name ='raccoon'
								# Any other entity Id must be a squid monster
								else: monster_name = 'squid'
								# Once an enemy is attacked run the corresponding effects
								Enemy(
									# What monster did the player defeat?
									monster_name,
									# Where is the monster?
									(x,y),
									# Sprites for the player, monsters and obstacles
									[self.visible_sprites,self.attackable_sprites],
									# Obstacle sprites such as rocks
									self.obstacle_sprites,
									# How much damge did the player take?
									self.damage_player,
									# Death particles animation
									self.trigger_death_particles,
									# Add exp to player for deafeating monsters
									self.add_exp)
									
	# Controls the players attack
	def create_attack(self):
		# Player Attack is defined by player stats + attack sprites
		self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

	# Controls the players magic
	def create_magic(self,style,strength,cost):
		# When healing magic is used
		if style == 'heal':
			# Healing magic is defined with sprites, cost in energy and magic power
			self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

		# When flame magic is used
		if style == 'flame':
			# Flame magic is defined with sprites, cost in energy and magic power
			self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

	# Controls attacking
	def destroy_attack(self):
		# Kill the enemy
		if self.current_attack:
			self.current_attack.kill()
		# Otherwise not attacking
		self.current_attack = None

	# Creates function player_attack_logic with argument "Self"
	def player_attack_logic(self):
		# If the player uses an attack
		if self.attack_sprites:
			# If the player attack is attacking something
			for attack_sprite in self.attack_sprites:
				# If the sprite for an attack collides with the sprite for an enemy the player damages an enemy
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				# If the attack hits something
				if collision_sprites:
					# If the sprite the player attacks is an attackable sprite do damage
					for target_sprite in collision_sprites:
						# If the player attacks grass
						if target_sprite.sprite_type == 'grass':
							# The position attacked should be center of a single sprite (stops you from attacking sevral things at once)
							pos = target_sprite.rect.center
							# Controls where the attack hits
							offset = pygame.math.Vector2(0,75)
							# If the sprite is for grass
							for leaf in range(randint(3,6)):
								# The player animation attacks the defined position
								self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
							# If the player attack sprite collides with a grass sprite destroy the attacked sprite
							target_sprite.kill()
						# If the target is an enemy do damage rather than destroy the target
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	# Creates function damage_player that manages when the player can be damaged and by how much
	def damage_player(self,amount,attack_type):
		# The the player is vulnerable at all times other then immediately after being attacked
		if self.player.vulnerable:
			# The player loses an amount of health when attacked
			self.player.health -= amount
			# The player is made invincible for a moment
			self.player.vulnerable = False
			# How long the player is invincible for
			self.player.hurt_time = pygame.time.get_ticks()
			# Particle animations from player attacks
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	# Create function trigger_death_particles that controls the animation upon player death
	def trigger_death_particles(self,pos,particle_type):

		# Player death animation
		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	# Creates a function add_exp tha controls the amount of experience the player gathers
	def add_exp(self,amount):

		# Current amount of player exp + amount earned
		self.player.exp += amount

	# Controls the toggle for different UI options (Different weapons and magic types)
	def toggle_menu(self):

		# 101
		self.game_paused = not self.game_paused 

	# Create function run which controls whether the game display is running
	def run(self):
		# Draw the player sprite while the game is running
		self.visible_sprites.custom_draw(self.player)
		# The UI is running while the game is running
		self.ui.display(self.player)
		
		# Whenever the game is paused the display is updated
		if self.game_paused:
			self.upgrade.display()
		# Update sprites and locations whenever the game is running
		else:
			# Update the visible sprites such as player, obstacles and grass
			self.visible_sprites.update()
			# Update enemy sprite and values
			self.visible_sprites.enemy_update(self.player)
			# Runs the function controlling player attack
			self.player_attack_logic()
		
# Controls the ingame camera (Viewpoint / POW)
# Creates illusion of depth
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		# Sets up display surface
		self.display_surface = pygame.display.get_surface()
		# Alows the camera to follow the player
		# The player will allways be halfway across the screen from the left
		self.half_width = self.display_surface.get_size()[0] // 2
		# Allows the camera to follow the player
		# The player will always be halfway down the screen from the top
		self.half_height = self.display_surface.get_size()[1] // 2
		# Creates a vector that controls the camera location
		self.offset = pygame.math.Vector2()

		# creating the floor
		# Loads the floor image as the bottomost layer of graphics (evrything else is superimposed into it)
		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		# The topleft of the map is (0,0) which is the same as the top left of the pygame window
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	# Controls the camera
	def custom_draw(self,player):

		# The camera moves horizontaly with the player
		self.offset.x = player.rect.centerx - self.half_width
		# The camera moves vertically with the player
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		# Offsets the floor the same as the camera so that they are aligned
		floor_offset_pos = self.floor_rect.topleft - self.offset
		# Displays the floor surface
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# Orders the sprites in terms of y values 
		# Controls what sprite will overlap the other 
		# The sprite with the lower y value will other sprites with higher y value which adds depth
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			# How offset are the sprites?
			offset_pos = sprite.rect.topleft - self.offset
			# Display sprite image with offset
			self.display_surface.blit(sprite.image,offset_pos)

	# Controls enemy health and sprites
	def enemy_update(self,player):
		# If there is an enemy display their sprite
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		# Whenever the player encounters an enemy update sprites
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
