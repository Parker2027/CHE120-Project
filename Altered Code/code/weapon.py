# This was commented by Nate Barret (21027169)
# this line imports code from the pygame file
import pygame 

# this line establishes a new class Weapon with parameters of pygame, sprite, and Sprite
class Weapon(pygame.sprite.Sprite):
	# this function initiates the behaviour of the weapon with regards to the variables self, player, and groups
	def __init__(self,player,groups):
		# this line of code sets up the groups variable with parameters used by other variables using the super(). function
		super().__init__(groups)
		# this line of code establishes a type of sprite for weapons
		self.sprite_type = 'weapon'
		# this line of code sets the direction of the player and shares it with the weapon
		direction = player.status.split('_')[0]

		# the original programmer lets us know that this block of code establishes the graphics for the weapons
		# graphic
		# this line of code sets a variable full_path to opening the graphics folder and taking the weapon sprite, applying it to the player
		full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
		# this line of code loads the image of the weapon sprite onto the player's sprite, and letting them move together
		self.image = pygame.image.load(full_path).convert_alpha()
		
		# the original programmer lets us know that this section establishes the placement for the weapon
		# placement
		# this if statement is for the situation where the player is facing the right direction
		if direction == 'right':
			# this line of code establishes a small rectangular hitbox for the weapon with dimensions of 0 X 16
			self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
		# this elif statement is for the situation where the player is facing the left direction
		elif direction == 'left': 
			# this line of code establishes a small rectangular hitbox for the weapon with dimensions of 0 X 16
			self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
		# this elif statement is for the situation where the player is facing the downward direction
		elif direction == 'down':
			# this line of code establishes a small rectangular hitbox for the weapon with dimensions of -10 X 0
			self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
		# this else statement is for the situation where the player is facing the upward direction
		else:
			# this line of code establishes a small rectangular hitbox for the weapon with dimensions of -10 X 0
			self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
