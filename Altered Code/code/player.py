#This was commented by Luc Bourassa, ID 21027232

#For all comments to this module, the word player refers to the user providing input, while the word character refers
#to the in game rendition of the model that carries out these commands.

#This module is for all things regarding the character including player input, basic animations, abilities, and stats.
#Starts by bringing in other functions and variables from the settings, support, and entity modules
#These are for use in this module and most regard variables surrounding the character model and its potential states.

import pygame 
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
# A class for functions regarding everything the character can do
#This involves attacking, moving, standing still, using magic, and taking damage

	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
	#This function is used to initialize every aspect of the character regarding its different possible states at the start of the game
	#There are 12 states in total: 4 for attacking (1 in each direction), 4 for moving (1 in each direction) and 4 for standing still(1 in each direction
	#All of these parts deal with these states in one way or another, and allow the player to continually provide input for the character with response
	
		super().__init__(groups)  #Function from the tile module regarding movement interactions with objects and layers of the map
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()   #Generates the sprite for the character image from its file in storage
		self.rect = self.image.get_rect(topleft = pos)  #Sets the starting position of the character image and its boundaries with respect to the map
		self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])  #Sets the hitbox for the character image

		# graphics setup
		self.import_player_assets()
		self.status = 'down'   #Default for starting the game is character facing down

		# movement 
		self.attacking = False       #Default state of the character is not attacking
		self.attack_cooldown = 400   #Default attack cooldown, changes for each weapon
		self.attack_time = None      #No timer since the character does not start in the attack state, this will change for each cooldown
		self.obstacle_sprites = obstacle_sprites  #Generates the places where the character cannot move on the map (detailed in settings, but also a part of the map file)

		# weapons for regular attack
		self.create_attack = create_attack      #When attacking creates a weapon sprite and hitbox
		self.destroy_attack = destroy_attack    #After the attack cooldown ends, destroys the weapon sprite and hitbox
		self.weapon_index = 0      #Current weapon number, contains corresponding data, starts at the sword weapon but can be changed by input
		self.weapon = list(weapon_data.keys())[self.weapon_index]   #Used for the switching of weapons as well, sets the data of current weapon
		self.can_switch_weapon = True        #By default the player is able to switch the characters weapon
		self.weapon_switch_time = None       #Time taken to switch to another weapon, set as none since the character already has a cooldown after switching to limit speed of input
		self.switch_duration_cooldown = 200  #Default weapon switch cooldown, does not change

		# magic 
		self.create_magic = create_magic   #Generates a sprite of the magic used, which disappears after a cooldown
		self.magic_index = 0     #Starts with the flame spell equipped
		self.magic = list(magic_data.keys())[self.magic_index]  #Used to find data for the starting spell, located in settings
		self.can_switch_magic = True     #Character is able to switch magic by default
		self.magic_switch_time = None    #Time taken to switch between magic, does not change

		# stats, can be changed through an upgrade menu
		self.stats = {'health': 10000000,'energy':60,'attack': 10,'magic': 4,'speed': 5}   #Dictionary containing starting stats for the character
		self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}  #Dictionary containing maximum stats for character
		self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}  #Upgrade cost dictionary, changes with each upgrade
		### Changed so that you start with 100 percent of your health ###
		self.health = self.stats['health'] * 1 #Health stat changes with respect to dictionary
		self.energy = self.stats['energy'] * 0.8 #Energy stat changes with stats dictionary
		### The player now starts with no exp ###
		self.exp = 0
		self.speed = self.stats['speed']  #Speed stat changes with dictionary, as it is updated by upgrades

		# damage timer, acts as an indirect limit to the amount of damage the character can take for a given time
		self.vulnerable = True   #By default, character is able to take damage
		self.hurt_time = None    #Time taken to decrease health when character takes damage
		self.invulnerability_duration = 500   #Time that separates the frequency at which character health can drop

		# imports a sound for attacking, and sets it to a healthy volume 
		self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
		self.weapon_attack_sound.set_volume(0.4)

	def import_player_assets(self):
	#This function provides animation output for each possible state that the character is in
	
		character_path = '../graphics/player/'  #Path to the character folder containing all sprites used in animations for the character
		
		#Dictionary to define each state of the character and its corresponding name for the animation of that state
		#As stated earlier there are 12 states, 3 in terms of different inputs, with 4 for each different input in each direction(up, down, left, right)
		#These dictionary terms correspond to the names of files containing their sprites
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
	#This function regards all possible types of attacking, meaning it allows for attack input, and the type of attack to be switched by another input
	#These attacks all use different sprites, the data for which is stored in another module. 
	#However, the character attack animation is the same, to reduce the number of states the character sprite needs
	
	#It should be noted that while it is possible for the character to be in multiple states at once.
	#this fuction, and the weapon segment from the first function prevent that to reduce the amount and complexity of sprites needed
	
		if not self.attacking:
		#This is a clause that prevents movement and attack at the same time
		#if this triggers, the character is not in an attacking state, and can move freely and change weapons
		#When player attacks, this if statement is untrue, so attacking restricts all input
			
			keys = pygame.key.get_pressed()    #Allows keyboard input to be provided outside of an attacking state.
			#The function this variable depends on is mapped by the standard keyboard layout, and the key pressed is mapped by a dictionary in a separate module
			#All input for non idling animations is through this variable, which is done to allow predictability in the inputs
			#and reduce the sheer number of possibilities for the character to be in (less bugs hopefully)

			# movement input, statements update the vertical and horizontal movements separately
			#so that the character is able to move diagonally (Both vertically and horizontally at the same time
			
			### Changed the movement keys from the arrow keys to w, s, a and d ###
			if keys[pygame.K_w]:  #Input up key from the player
				self.direction.y = -1   #Updates the coordinate of the player to move up, is negative because the player starts the game facing down, which is the positive direction
				self.status = 'up'    #Sets status of the player to be up, changing the sprite used
			elif keys[pygame.K_s]: #Input down key from player
				self.direction.y = 1  #Moves the player down by 1 unit in the map, defined in settings module
				self.status = 'down'  #Sets the state of the character, all animations from attacking idling and moving occur in the down direction
			else:
				self.direction.y = 0  #For when no vertical input is given but movement is still happening

			if keys[pygame.K_d]: #Input right key from player to move right
				self.direction.x = 1  #Right is arbitrarily set as the positive direction on the horizontal axis, moves character right
				self.status = 'right' #Sets status to use right facing sprite animations
			elif keys[pygame.K_a]:
				self.direction.x = -1  #Moves left on the horizontal axis
				self.status = 'left' #Sets status to use left facing sprite animations
			else:
				self.direction.x = 0  #For when character is not given input to move horizontally

			# attack input, this is for regular attacks with weapons and can be done infinitely (no restrictive stat, as with magic)
			#This makes the initial if statement untrue, and closes off all input for a short time (During cooldown)
			if keys[pygame.K_SPACE]:
				self.attacking = True #Attack state triggers, shutting off all potential input through this function for a short time
				self.attack_time = pygame.time.get_ticks()   #Cooldown (Time in attack state), varies based on weapon type
				self.create_attack()    #Also based on weapon type, this creates a sprite of the weapon used while attacking
				self.weapon_attack_sound.play()   #Attacking with a weapon has its own sound

			# magic input, for attacks regarding magic, which can be used a finite number of times based on the characters energy stat
			#Data for these variables are from another module
			#This makes the initial if statement untrue, and closes off all input for a short time (During cooldown)
			### Changed the key for magic from left control to return ###
			if keys[pygame.K_RETURN]:
				self.attacking = True  #Attack state triggers, shutting off all potential input through this function for a short time
				self.attack_time = pygame.time.get_ticks()      #Cooldown for magic attacks, based on type of magic
				style = list(magic_data.keys())[self.magic_index]    #Used to show a certain sprite based on the type of magic
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic'] #Damage done is increased through in game stats
				cost = list(magic_data.values())[self.magic_index]['cost']    #Magic costs an amount of energy, based on the type of magic
				self.create_magic(style,strength,cost)        #Creates a sprite, reduces energy, and damages enemies based on values found above

			### Changed the swap weapon key from q to left shift ###
			if keys[pygame.K_LSHIFT] and self.can_switch_weapon:  #Allows change of weapon if the character has not recently switched its weapon
			
				#Provides cooldown time for switching weapons, where players can still provide other input, but not switch weapons again
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				
				#Rotates between weapons by counting the weapon number (0 to 4, adding 1 each time weapon is switched)
				#Then resetting the count back to 0 when the count exceeds 4 (The amount of weapons existing in the game)
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
					
				#Data for the new weapon in use after any change has been made. Weapon data is stored in a list and is indexed accordingly
				#This results in a different sprite with different stats (Cooldown, hitbox, damage, etc)
				self.weapon = list(weapon_data.keys())[self.weapon_index]

			### Changed the swap magic key from e to right shift ###
			if keys[pygame.K_RSHIFT] and self.can_switch_magic:
			#Allows the player to switch between magic types (2 total) when they hit the appropriate button (e) and the cooldown for switching is reached
			
			#Works the exact same as weapon switching, where the player can still provide input, but not change magic for a short time
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				
				if self.magic_index < len(list(magic_data.keys())) - 1:  
				#Also works the same, but there are 2 types of magic, so this switches between the if and else clauses each time magic is switched
					self.magic_index += 1
				else:
					self.magic_index = 0

				#Updates self.magic to use different data from the magic data in the settings module
				self.magic = list(magic_data.keys())[self.magic_index]

	def get_status(self):
	#This function finds the non directional state of the character and updates the characters status to read its state

		# checks and assigns idle status to self.status if the character is not moving or attacking
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
				
		#Checks and assigns attacking status to character if it is in the attack state
		if self.attacking:
			#The character is made unable to move if attacking
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
			#updates the state of the character based on its current state, to avoid repetition of states in the self status string
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else: #Removes attack from status string for when the character stops attacking
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','') #Replaces attack with an empty string

	def cooldowns(self):
	#This function acts as a clock that cooldowns are based on, using parts of another module
		current_time = pygame.time.get_ticks()
		
		#Cooldown for attack input
		if self.attacking:
			#Compares the attack time to the time taken for an attack cooldown based on specific weapon data
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				#If the time spent in the attacking state is greater than or equal to the cooldown of the attack, the character is no longer attacking
				self.attacking = False
				self.destroy_attack() #Destroys the sprite of the weapon used to attack
				
		#Cooldown for weapon switching, if the input to switch weapons was given
		if not self.can_switch_weapon:
			#If the time spent after switching the weapon is greater than or equal to the cooldown for weapon switching, the player is able to switch weapons again
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True
				
		#Cooldown for switching magic if the input to switch magic is given
		if not self.can_switch_magic:
			#If the time taken after switching weapons is greater than or equal to the cooldown for weapon switching, the player is able to switch again
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				#Cooldown is the same as for switching weapons
				self.can_switch_magic = True
		#Cooldown for grace period after taking damage
		if not self.vulnerable:
			#If the time taken after being damaged is greater than or equal to the grace period of invulnerability, the character can be damaged again
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True

	def animate(self):
		#Runs an animation function to output a sprite for every state the character is in
		animation = self.animations[self.status]

		#loop over the frame index to run the animation repeatedly so that movement and constantly changing states are maintained smoothly
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		#setting the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		#flicker effect that triggers right after the character takes damage 
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):
		#Returns the damage done by a weapon using indexes of stats for the character and weapon in a dictionary under the setttings module
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']
		return base_damage + weapon_damage  #Sum of the damage done by the weapon and the attack stat of the character

	def get_full_magic_damage(self):
		#Returns the damage output of spells using indexes of dictionaries found under the settings module and character stats
		base_damage = self.stats['magic']
		spell_damage = magic_data[self.magic]['strength']
		return base_damage + spell_damage #Sum of the damage done by an individual spell and the magic damage potential by character stats

	def get_value_by_index(self,index):
		#This function returns a value in a list of character stats by indexing for the desired output
		return list(self.stats.values())[index]

	def get_cost_by_index(self,index):
		#This function returns a value for cost (of using magic) in a list by indexing for the desired output 
		return list(self.upgrade_cost.values())[index]

	def energy_recovery(self):
		#This function enables recovery of energy for casting spells in the game when the characters energy is not full
		if self.energy < self.stats['energy']:
			self.energy += 0.01 * self.stats['magic'] #Recharges energy by adding a small amount that is a multiple of the players magic stat every time the function is run
		else:
			self.energy = self.stats['energy']

	def update(self):
		#This function updates the state of the player and updates all related data needed to work with new states
		#This gets an input from the player. Self input is done first since it is the only variable revolving around the player that is changed the most
		self.input()
		#This is run after getting the input to carry out parts of the input such as attacks and weapon or magic switching, and to maintain accuracy of the cooldowns immediately after the input is given
		self.cooldowns()
		#The characters state is updated to match that provided of the input given
		self.get_status()
		#Once the state has been updated, the character is animated to match it with a given sprite
		self.animate()
		#All inputs without cooldown timers, such as moving, are then carried out. These have less priority since they do not need to be timed and stop by choice of the player
		self.move(self.stats['speed'])
		#Lowest priority to updating stats of player. Triggers energy rejuvenation, which does not depend on the input of the player and is refreshed every time the character is updated
		self.energy_recovery()

		### Changed so that if player health ever reached zero the game will quit and you will need to try again ###
		if self.health <= 0:
			quit()