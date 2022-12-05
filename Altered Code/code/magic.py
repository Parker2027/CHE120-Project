# This was commented by Wafeeq Alam (21026755)
import pygame
from settings import *
from random import randint

class MagicPlayer:
	def __init__(self,animation_player):
		self.animation_player = animation_player
		self.sounds = {
		'heal': pygame.mixer.Sound('../audio/heal.wav'),
		'flame':pygame.mixer.Sound('../audio/Fire.wav')
		}
#This is our heal spell function
#When the spell is cast, it will first check if the player has equal to or greater energy to the cost of the heal spell
#If the cost is met, the heal sound bite will play and the player health will raise by the strength value of the heal spell
#The cost of the spell will be deducted from the player energy resource
#However if the players health becomes greater than or equal to the maximum health they currently have, the player health will become equal to their maximum current health, this is to prevent overhealing
#The healing animation then applies the aura and heal sprites on top of the player character
	def heal(self,player,strength,cost,groups):
		if player.energy >= cost:
			self.sounds['heal'].play()
			player.health += strength
			player.energy -= cost
			if player.health >= player.stats['health']:
				player.health = player.stats['health']
			self.animation_player.create_particles('aura',player.rect.center,groups)
			self.animation_player.create_particles('heal',player.rect.center,groups)
#This is our flame spell function
#When the spell is cast, it will first check if the player has equal to or greater energy to the cost of the flame spell
#If the cost is met, the sound bite for the heal spell will play
	def flame(self,player,cost,groups):
		if player.energy >= cost:
			player.energy -= cost
			self.sounds['flame'].play()
#This area will determine what direction the spell will be cast depending on the directional orientation of the player character
#Each two dimensional vector will determine where the spell is cast, right, up, and left
#The base direction of the player if no direction is determined is down
			if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
			elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
			elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
			else: direction = pygame.math.Vector2(0,1)
#This will determine the size of effect where the damage of the flame spell is applied
#Depending on the directional orientation of the character, the flame will have a different animation applied to the area designated
			for i in range(1,6):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('flame',(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
					y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
					self.animation_player.create_particles('flame',(x,y),groups)
