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
			# Imports flame graphics
			'flame': import_folder('../graphics/particles/flame/frames'),
			# Imports aura graphics
			'aura': import_folder('../graphics/particles/aura'),
			# Imports heal graphics
			'heal': import_folder('../graphics/particles/heal/frames'),
			
			# Imports the .png files for the graphics for the physical attacks
			# Imports claw graphics
			'claw': import_folder('../graphics/particles/claw'),
			# Imports slash graphics
			'slash': import_folder('../graphics/particles/slash'),
			# Imports sparkle graphics
			'sparkle': import_folder('../graphics/particles/sparkle'),
			# Imports leaf_attack graphics
			'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
			# Imports thunder graphics
			'thunder': import_folder('../graphics/particles/thunder'),

			# Imports the .png files for the graphics for enemy deaths
			# Imports squid death graphics
			'squid': import_folder('../graphics/particles/smoke_orange'),
			# Imports racoon death graphics
			'raccoon': import_folder('../graphics/particles/raccoon'),
			# Imports spirits death graphics
			'spirit': import_folder('../graphics/particles/nova'),
			# Imports bamboo death graphics
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
	
	# Creates a function that mirrors sprites
	def reflect_images(self,frames):
		# variable new_frames = empty list
		new_frames = []

		for frame in frames:
			# Flips the sprites on the x axis
	 		flipped_frame = pygame.transform.flip(frame,True,False)
			# Saves the mirrored sprites in the list new_frames
	 		new_frames.append(flipped_frame)
		return new_frames

	# Adds the particles from interaction with grass
	def create_grass_particles(self,pos,groups):
		# How fast is the animation playing
	 	animation_frames = choice(self.frames['leaf'])
		# Particle effect is added at the position of the grass and at the framerate
	 	ParticleEffect(pos,animation_frames,groups)
		
	# Adds the general animations
	def create_particles(self,animation_type,pos,groups):
		# The speed of the animation depends on which animation is chosen
		animation_frames = self.frames[animation_type]
		# The particle effect occurs at the location and speed specified
		ParticleEffect(pos,animation_frames,groups)

# Creates class ParticleEffect
class ParticleEffect(pygame.sprite.Sprite):
	# Initiates class ParticleEffects
	def __init__(self,pos,animation_frames,groups):
		# Initializes "groups"
		super().__init__(groups)
		# The sprite used is for the magic effect
		self.sprite_type = 'magic'
		# Initial player frame_index is 0
		self.frame_index = 0
		# defines animation_speed 
		self.animation_speed = 0.15
		# Player fps equal to animation fps
		self.frames = animation_frames
		# Player image fps equal to self.frame_index
		self.image = self.frames[self.frame_index]
		# Stores the position (center) of the player
		self.rect = self.image.get_rect(center = pos)
		
	# Controls animation (Change in sprites)
	def animate(self):
		# Choses a new image from the list of images
		self.frame_index += self.animation_speed
		# Destoy the sprite after it is used
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			# Otherwise the image displayed is the image selected 
			self.image = self.frames[int(self.frame_index)]

	# The animation will update with each tick that passes
	def update(self):
		# The player animation is updated
		self.animate()
