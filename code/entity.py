import pygame 
# this line imports the pygame file for the entire game file to run
from math import sin 
#this line imports the sin function from the math class

class Entity(pygame.sprite.Sprite): 
	#this line defines a class for an entity in the game, which seems to be called a Sprite
	def __init__(self,groups): 
		#this function initiates the code for the variables self (which is for entities like enemies) and groups
		super().__init__(groups) 
		#this line calls up code that is shared between multiple objects
		self.frame_index = 0 
		#this line sets the frame data for the entity at 0
		self.animation_speed = 0.15 
		#this line sets the speed of the entity's animation at 0.15
		self.direction = pygame.math.Vector2() 
		#this line establishes a vector for the entity's direction

	def move(self,speed): 
		#this function describes the movement of the entity with regards to its direction and speed
		if self.direction.magnitude() != 0: 
			#this if statement takes the magnitude of the entity's direction and makes sure that it doesn't equal 0
			self.direction = self.direction.normalize() 
			#this line normalizes the direction vector of the entity, making the code easier to run

		self.hitbox.x += self.direction.x * speed 
		#this line makes sure that the hitbox of the entity travels with the x direction of the entity incrementally
		self.collision('horizontal') 
		#this line makes the entity collide with borders in the x direction
		self.hitbox.y += self.direction.y * speed 
		#this line makes sure that the hitbox of the entity travels with the y direction of the entity incrementally
		self.collision('vertical') 
		#this line makes the entity collide with borders in the y direction
		self.rect.center = self.hitbox.center 
		# this line makes sure that the center of the rectangle that forms the entity's hitbox is the entity's center

	def collision(self,direction): 
		#this function determines what happens whay happens when the entity collides into another objecgt
		if direction == 'horizontal': 
			#this if statement sets up the paramter that the direction the entity is travelling is horizontal (along x-axis)
			for sprite in self.obstacle_sprites: 
				#this for loop uses the parameters that a sprite for the obstacle the entity is colliding into exists in a separate function,  meaning that this line of code will loop repeatedly as long as the sprite exists
				if sprite.hitbox.colliderect(self.hitbox): 
					#this if statement seems to code for the scenario where the entity's hitbox comes into contact with a "hitbox" for the obstacle
					if self.direction.x > 0: 
						# moving right  
						#the original programmer gives some very helpful insight here, which lets us know that this if statement is for the scenario where the entity is moving towards the right
						self.hitbox.right = sprite.hitbox.left 
						#this line seems to make the sprite of the entity move in the opposite direction of the hitbox when it is moving to the right and hits an obstacle
					if self.direction.x < 0: 
						# moving left 
						#once again, the original programmer leaves a helpful insight letting us know that this if statement is for the situation where the entity moves towards the left
						self.hitbox.left = sprite.hitbox.right 
						#this line seems to make the entity sprite move in the opposite direction of the hitbox when it is moving to the left and hits an obstacle 

		if direction == 'vertical': 
			#this if statement is for the situation where the entity is moving in a vertical direction (up or down along y-axis)
			for sprite in self.obstacle_sprites: 
				#this for loop is for repeating the code for when the sprite collides with an obstacle
				if sprite.hitbox.colliderect(self.hitbox): 
					#this if statement is for the scenario where the entity has made contact with the obstacle
					if self.direction.y > 0: 
						# moving down  
						#this if statement is for the scenario where the entity is moving in the downward direction, as stated by the original programmer
						self.hitbox.bottom = sprite.hitbox.top 
						#this line seems to make the entity sprite move in the opposite direction of the hitbox when it moves in the downward direction
					if self.direction.y < 0: 
						# moving up 
						#this if statement is for the situation where the entity is moving in the upward direction, as stated by the original programmer
						self.hitbox.top = sprite.hitbox.bottom 
						#this line seems to make the entity dprite move in the opposite direction of the hitbox, when it moves in the uoward direction

	def wave_value(self): 
		#this function seems to produce a wave for the entity
		value = sin(pygame.time.get_ticks()) 
		#this line seems to create a sine function using a counter
		if value >= 0: 
			#this if statement takes the value variable and checks to see whether or not it is greater or equal to 0
			return 255 
			#this line returns the value 225 to the wave function
		else: 
			#this else statement is for the scenario where the value is less than 0
			return 0 
			#this line returns the value 0 to the wave function
