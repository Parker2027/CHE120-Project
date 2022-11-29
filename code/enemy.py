import pygame 
#this line is imports a pygame file
from settings import * 
#this seems to be another imported file called "settings", based on the way it's formatted I assume it comes from some other place in the game file
from entity import Entity 
#another imported file called "entity", likely from some other place in the game file
from support import * 
#another imported file called 'support', likely from some other place in the game's code

class Enemy(Entity): 
	#this is a line of code that sets up a whole new class specific to this code, the "enemy" class; all of the assets for enemies for the user to fight likely come from here
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp): 
		#this is a function for the class, which has lots of variables for the enemy's name, position, number of enemies, how it damages the player, and how it dies
			
		#the original programmer includes their own notes in this file
		# general setup #original programmer lets us know that this is how each enemy is set up
		
		super().__init__(groups) 
		# the super() function is used to make a variable share properties with another variable; given that information, we see that the __init__(groups) initiates the code for the enemies
		self.sprite_type = 'enemy' 
		#this line seems to be the actual line that creates the enemies

		# graphics setup 
		#original programmer lets us know that this is how each enemy's sprite is set up
		self.import_graphics(monster_name) 
		#this line imports the sprites for each enemy using the mmonster_name variable
		self.status = 'idle' 
		#this line shows us the state of the enemy sprite, which in this case is idle (stationary, not active until engaged by user)
		# Next line causes out of index error
		# Original programmer let's us know what the following line does, which is creating an out of index error
		self.image = self.animations[self.status][self.frame_index] 
		#this line changes the sprite's animation while in the idle position

		# movement 
		#original programmer lets us know that this is how each enemy moves
		self.rect = self.image.get_rect(topleft = pos) 
		#this line creates a rectangle for each enemy, which likely produces a hitbox based on what the line below states
		self.hitbox = self.rect.inflate(0,-10) 
		#this line creates the hitbox for the enemy using the rectangle from the previous line; when the user attacks the enemy, hits landed on the the hitbox will reflect as damage upon the enemy
		self.obstacle_sprites = obstacle_sprites 
		#this line controls how the enemy interacts with the environment and with the user; the enemy acts as an obstacle that the user cannot pass walk through without removing it or avoiding it; similarly, the enemy cannot move through an obstacle without removing it or avoiding

		# stats 
		#original programmer lets us know that this is where the stats for each monster is found
		self.monster_name = monster_name 
		#this line sets each enemy's name to distinguish the different types of enemy
		monster_info = monster_data[self.monster_name] 
		#this line exists to attach the name of each enemy to its specific data for its stats and characteristics
		self.health = monster_info['health'] 
		#this line establishes how much health the enemy will have (eg. a health of 50 or 100)
		self.exp = monster_info['exp'] 
		#this line establishes how much experience ("exp") the enemy will yield for the player once it is defeated
		self.speed = monster_info['speed'] 
		#this line establishes how quickly or slowly the enemy will move
		self.attack_damage = monster_info['damage'] 
		#this line establishes how much damage the enemy can deal to the player
		self.resistance = monster_info['resistance'] 
		#this line establishes what resistances the enemy will have towards different attack types (eg. a water enemy may be immune to water attacks, but may take damage from lightning attacks)
		self.attack_radius = monster_info['attack_radius'] 
		#this line establishes the radius of an enemy's attack (determines how far an enemy has to be from the player before it can deal damage to them)
		self.notice_radius = monster_info['notice_radius'] 
		#this line establishes when the enemy will notice a player (determines the radius for which an enemy can notice tha player, switching it from a passive, stationary demeanor to a more hostile, aggressive one)
		self.attack_type = monster_info['attack_type'] 
		#this line establishes the type of attack the enemy will perform (whether it is a fire attack or a melee attak or an explosion attack, etc)

		# player interaction 
		#original programmer lets us know that this is where the interactions between the enemy and the player are determined
		self.can_attack = True 
		#this line allows the enemy to attack the player; if can attack = False, the enemy would not be able to attack
		self.attack_time = None 
		#this line probably ensure that the enemy cannot perform consecutive attacks against the player
		self.attack_cooldown = 400 
		#this line is cooldown time for the attack; it makes sure that the enemy cannot perform consecutive attacks against the player until the cooldown time runs out
		self.damage_player = damage_player 
		#this line allows any damage the enemy has dealt to the player to be reflected in player's health
		self.trigger_death_particles = trigger_death_particles 
		#this line triggers a particle effect to appear once the enemy has been defeated by the player
		self.add_exp = add_exp 
		# this line add the exp to the player after the enemy has been slain

		# invincibility timer 
		#original programmer lets us know that this section codes for a timer for the enemy
		self.vulnerable = True 
		# this line establishes that each enemy is vulnerable to an attack by the player
		self.hit_time = None 
		# this line might make make an attack instantaneous, preventing any lag during a fight with the enemy
		self.invincibility_duration = 300 
		#this line establishes some invicibility frames for the enemy, ensuring that the player cannot deal consecutive attacks against the enemy and incresing the difficulty of the fight; once the invicibility timer reaches 0, the invincibility period ends and the enemy is vulnerable once again

		# sounds 
		#original programmer lets us know that this section codes for the audios used by the enemies in the game
		self.death_sound = pygame.mixer.Sound('../audio/death.wav') 
		#this line codes for the audio used by the enemy when it is slain by the player
		self.hit_sound = pygame.mixer.Sound('../audio/hit.wav') 
		# this line codes for the audio used by the enemy when it is hit
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound']) 
		# this line codes for the audio used by the enemy when it is attacking
		self.death_sound.set_volume(0.6) 
		#this line sets the volume of the death sound to 0.6
		self.hit_sound.set_volume(0.6) 
		#this line sets the volume of the hit sound to 0.6
		self.attack_sound.set_volume(0.6) 
		#this line sets the volume of the attack sound to 0.6

	def import_graphics(self,name): 
		# this section is a function that runs animations for the enemy
		self.animations = {'idle':[],'move':[],'attack':[]} 
		#this line seems to create a list containing all of those objects
		main_path = f'../graphics/monsters/{name}/' 
		#this line seems to establish a list of strings for the monster's animations and graphics
		for animation in self.animations.keys(): 
			#this is a for loop for the animation of the enemies to be repeated as long as the animation exists in it's proper folder
			self.animations[animation] = import_folder(main_path + animation) 
			#this line lets the code acess a folder and play the appropriate animation for each specific monster during the aprropriate situation

	def get_player_distance_direction(self,player):		 #this section is a function that seems to calculate the distance between the enemy and the player, and the direction of the player with regards to the enemy
		enemy_vec = pygame.math.Vector2(self.rect.center) # this line creates a vector from the enemy to the center of the game's map
		player_vec = pygame.math.Vector2(player.rect.center) # this line creates a vector from the player to the center of the game's map
		distance = (player_vec - enemy_vec).magnitude() #this line defines a variable distance as the enemy's vector subtracted from the enemy's vector and converted to magnitude

		if distance > 0:			 #this line establishes an if statement where the parameters are that distance must be greater than 0
			direction = (player_vec - enemy_vec).normalize()		 # this line seems to establish a new variable direction by finding the difference between the player's vector and the enemy's vector, and normalizing it
		else:			 #else statement for scenarios where distance = 0 (should not be possible for distance to be less than 0)
			direction = pygame.math.Vector2()		 #this establishes a new vector which I assume is betweenthe player and the enemy

		return (distance,direction)		 #this line just gives the calculated value for distance and direction

	def get_status(self, player): #this line establishes a new function using the self and player as input variables, which gets the status between the two entities
		distance = self.get_player_distance_direction(player)[0] #this retrieves the values for distance and direction from the above function

		if distance <= self.attack_radius and self.can_attack: #this line establishes an if statement that checks if the distance between the player and the enemy is within the enemy's attack radius, and whether the enemy is able to attack
			if self.status != 'attack': # this line establishes another if statement within an if statement for if the enemy is unable to attack
				self.frame_index = 0 # this line is for the the enemy's frame data; with a frame_index = 0, we're being told that the enemy is no longer moving and is stationary
			self.status = 'attack' #this line seems to help ensure that the enemy is in attack mode and ready to fight the player when engaged
		elif distance <= self.notice_radius: #this elif checks if the distance between the player and the enemy is within the enemy's notice range 
			self.status = 'move' # this line makes the enemy move towards the player while it is in the notice range
		else: # this else statement is a code in case the player is not within the enemy's notice radius
			self.status = 'idle' #this line ensures that the enemy is idle and performing it's idle animations when not engaged in combat

	def actions(self,player): # this function establishes a basis for the interactions betweem the enemy and the player when the player is attacking the enemy
		if self.status == 'attack': #this if statement is for the enemy while it is in attack mode
			self.attack_time = pygame.time.get_ticks() #this establishes a variable for enemies that can serve as a timer
			self.damage_player(self.attack_damage,self.attack_type) #this line calls up the attack type and attack damage variables to determine how much damage the player will be dealt
			self.attack_sound.play() #this line plays the attack sound as the enemy attacks the player
		elif self.status == 'move': #this elif statement is for the situation where the enemy is in moveing mode
			self.direction = self.get_player_distance_direction(player)[1] #this line seems to be moving the enemy toward the player
		else: #this else statement should be for situation where the enemy is not in the attack or move position (enemy is idle)
			self.direction = pygame.math.Vector2() # this line is establishing a new vector, which is likely between the enemy and the player

	def animate(self): # this function is for animating the enemy
		animation = self.animations[self.status] #this line calls up the animation of the enemy based on whether or not it is in attack, move, or idle position
		
		self.frame_index += self.animation_speed #this line increases the frame data of the enemy's animation incrementally
		if self.frame_index >= len(animation): #this if statement runs if the frame_index is greater than the length of the enemy's animation
			if self.status == 'attack': # this if statement within the previous if statement is for the enemy in attack mode
				self.can_attack = False #this line has diabled the enemy's ability to attack
			self.frame_index = 0 #this line resets the frame data to 0

		self.image = animation[int(self.frame_index)] #this variable produces an animation from the frame_index value turned to an integer
		self.rect = self.image.get_rect(center = self.hitbox.center) #this line seems to set the center of the rectangle that serves as the enemy's hitbox to be moved to the center of the enemy's sprite

		if not self.vulnerable: #this if statement is for the situation where the enemy has its invincibility frames and is invulnerable to attacks
			alpha = self.wave_value() #this line seems to be referring to an audio file that is being set to the variabel alpha
			self.image.set_alpha(alpha) #this is setting an image to the same variable alpha
		else: #this else statement is for the situation where the enemy does not have invincibility
			self.image.set_alpha(255) #this is setting an image to the same variable aplha

	def cooldowns(self): # this function acts to control the cooldown time for the enemy
		current_time = pygame.time.get_ticks() #this line sets a timer for the variable current_time
		if not self.can_attack: # this if statement for the situation where the enemy cannot attack the enemy
			if current_time - self.attack_time >= self.attack_cooldown: #this if statement within the if statement is for the scenario where subtracting the attack time from the current time is greater than or equal to the cooldown time
				self.can_attack = True # this line restores the enemy's ability to attack the player

		if not self.vulnerable: #this if statement is for the siutation where the enemy has its invincibility status and not vulnerable to attack
			if current_time - self.hit_time >= self.invincibility_duration: #this if statement within an if statement is for the scenario where subtracting the hit time from the current time is greater or equal the inv
				self.vulnerable = True #this line restores the vulnerability to the enemy

	def get_damage(self,player,attack_type): #this function calculates the damage inflicted upon the enemy when the player attacks it
		if self.vulnerable: #this if statement is for the scenario where the enemy is vulnerable to attacks from the player
			self.hit_sound.play() #this line plays the hit sound effect whenever one of the player's attacks land on the enemy's hitbox
			self.direction = self.get_player_distance_direction(player)[1] #this line exists to get the direction and distance from the player to the enemy, perhaps to calculate some form of knockback or recoil as a result from the enemy taking damage
			if attack_type == 'weapon': #ths if statement is for the situation where the enemy is struck by the player's weapon (eg. sword, arrow, etc)
				self.health -= player.get_full_weapon_damage() #this line updates the enemy's health to reflect the damage it sustained from the player's weapon
			else: #this else statement is for situations where the enemy is struck by attacks that are not dealt by a weapon
				self.health -= player.get_full_magic_damage() #this line updates the enemy's health to reflect the damage it sustained from the player's magical attacks
			self.hit_time = pygame.time.get_ticks() #this line establishes a timer for the hit time, which would be the time between a player's attacks
			self.vulnerable = False #this line returns the enemy's invincibility status briefly

	def check_death(self): #this function allows for the enemy to die once the monster's health is equal to 0
		if self.health <= 0: #this if statement establishes what happens when the enemy's health drop below 0
			self.kill() #this line seems to shut down the code for the individual enemy completely after it has been slain
			self.trigger_death_particles(self.rect.center,self.monster_name) #this line triggers the death particles effect from the center of the enemy's hitbox rectangle
			self.add_exp(self.exp) #this line allows valuable exp to be dropped after the enemy's death
			self.death_sound.play() #this line plays the death sound for the enemy

	def hit_reaction(self): #this function codes for the reaction the enemy will have after being hit
		if not self.vulnerable: #this if statement is for the scenario where the enemy is invincible to attacks
			self.direction *= -self.resistance #this line seems to code for potential knockback or recoil from a player's attacks on an enemy

	def update(self): #this function updates the status of the enemy and allows the other functions to run
		self.hit_reaction() #this line runs the above hit_reaction function
		self.move(self.speed) #this line allows the enemy to move at a rate of self.speed
		self.animate() #this line runs the animate function
		self.cooldowns() # this line runs the cooldowns function
		self.check_death() # this line runs the check_death function

	def enemy_update(self,player): #this function updates the enemy based on the status of itself and the player
		self.get_status(player) #this line runs the get_status function using the player as an input variable
		self.actions(player) #this line runs the actions function using th player as an input variable
