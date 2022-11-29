# Imports the pygame module
import pygame
# Imports "import_folder" from support.py
from support import import_folder
# Imports the function choice() from the random module
from random import choice

# Creates the class AnimationPlayer
class AnimationPlayer:
	# Initiates class AnimationPlayer
	def __init__(self):
		# assigns frames to class AnimationPlayer
		self.frames = {
			# Imports the .png files for the graphics for the magic effects
			# Imports flame
			'flame': import_folder('../graphics/particles/flame/frames'),
			# Imports aura
			'aura': import_folder('../graphics/particles/aura'),
			# Imports heal
			'heal': import_folder('../graphics/particles/heal/frames'),
			
			# Imports the .png files for the graphics for the physical attacks
			# Imports claw
			'claw': import_folder('../graphics/particles/claw'),
			# Imports slash
			'slash': import_folder('../graphics/particles/slash'),
			# Imports sparkle
			'sparkle': import_folder('../graphics/particles/sparkle'),
			# Imports leaf_attack
			'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
			# Imports thunder
			'thunder': import_folder('../graphics/particles/thunder'),

			# Imports the .png files for the graphics for enemy deaths
			# Imports squid death
			'squid': import_folder('../graphics/particles/smoke_orange'),
			# Imports racoon death
			'raccoon': import_folder('../graphics/particles/raccoon'),
			# Imports spirits death
			'spirit': import_folder('../graphics/particles/nova'),
			# Imports bamboo death
			'bamboo': import_folder('../graphics/particles/bamboo'),
			
			# Imports the .png files for the graphics for the different leafs 
			'leaf': (
				import_folder('../graphics/particles/leaf1'),
				import_folder('../graphics/particles/leaf2'),
				import_folder('../graphics/particles/leaf3'),
				import_folder('../graphics/particles/leaf4'),
				import_folder('../graphics/particles/leaf5'),
				import_folder('../graphics/particles/leaf6'),
				# Mirrors all the imported leaf graphics
				self.reflect_images(import_folder('../graphics/particles/leaf1')),
				self.reflect_images(import_folder('../graphics/particles/leaf2')),
				self.reflect_images(import_folder('../graphics/particles/leaf3')),
				self.reflect_images(import_folder('../graphics/particles/leaf4')),
				self.reflect_images(import_folder('../graphics/particles/leaf5')),
				self.reflect_images(import_folder('../graphics/particles/leaf6'))
				)
			}
	
	# Creates function reflect_images with arguments "self" and "frames"
	def reflect_images(self,frames):
		# variable new_frames = empty list
		new_frames = []

		# 
		for frame in frames:
			# 
	 		flipped_frame = pygame.transform.flip(frame,True,False)
			#
	 		new_frames.append(flipped_frame)
		return new_frames

	# Creates function create_grass_particles with arguments "self", "pos" and "groups"
	def create_grass_particles(self,pos,groups):
		# 
	 	animation_frames = choice(self.frames['leaf'])
		#
	 	ParticleEffect(pos,animation_frames,groups)
		
	# 
	def create_particles(self,animation_type,pos,groups):
		#
		animation_frames = self.frames[animation_type]
		#
		ParticleEffect(pos,animation_frames,groups)

# Creates class ParticleEffect
class ParticleEffect(pygame.sprite.Sprite):
	# Initiates class ParticleEffects
	def __init__(self,pos,animation_frames,groups):
		# Initiales "groups"
		super().__init__(groups)
		# The sprite used is for the magic effect
		self.sprite_type = 'magic'
		# Initial player frame_index is 0
		self.frame_index = 0
		# defines animation_speed 
		self.animation_speed = 0.15
		# Player fps equal to animation fps
		self.frames = animation_frames
		# PLayer image fps equal to self.frame_index
		self.image = self.frames[self.frame_index]
		# Stores the position (center) of the player
		self.rect = self.image.get_rect(center = pos)
		
	# Creates function animate with argument "Self"
	def animate(self):
		# defines variable self.frame_index
		self.frame_index += self.animation_speed
		# If ever self.frames grows larger than self.frames_index the player is killed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			# set player image to number of player fps
			self.image = self.frames[int(self.frame_index)]

	# Creates function update with argument "Self"
	def update(self):
		# The player animation is updated
		self.animate()
