# this line imports the pygame file in order for the game's visuals and a sys file
import pygame, sys 
# this line seems to call up some code from a settings file elsewhere in this game's file
from settings import * 
# this line seems to call up a class Level from a level file elsewhere in this game's code
from level import Level 

# this line establishes a new class called Game, where we can assume most of the work for running and starting the game can be found
class Game: 
	# this function starts the code for starting the game
	def __init__(self): 

		# general setup 
		# this is the code that starts the actual game using the pygame file
		pygame.init() 
		
		# this line establishes the display screen for the game
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH)) 
		#this line produces a caption for the game that says 'Zelda'
		pygame.display.set_caption('Zelda') 
		#this line makes a clock that runs in game
		self.clock = pygame.time.Clock() 
		# Creates the game level (graphics and positions)
		self.level = Level() 
		

		# sound 
		#this line codes for the main theme of the game
		main_sound = pygame.mixer.Sound('../audio/main.ogg') 
		#this line codes for the volume of the main theme for the game and sets it at 0.5
		main_sound.set_volume(0.5) 
		#this line plays the main theme of the game and loops it indefinitely
		main_sound.play(loops = -1) 
		
	#this function runs the game
	def run(self): 
		#this while loop uses the parameters true, meaning that the game is running and the player is on some sort of select screen
		while True: 
			#this for loop is for various events in event.get() function
			for event in pygame.event.get(): 
				#this if statement is for the scenario that the player has decided to quit the program and exit the game
				if event.type == pygame.QUIT: 
					#this line quits the pygame file and cancels the running of code
					pygame.quit() 
					#this line exits the system and shuts down the program
					sys.exit() 
					
				#this if statement is for the event that the player scrolls down a list of options using the down arrow key
				if event.type == pygame.KEYDOWN: 
					#this if statement seems to code for an event in the menu
					if event.key == pygame.K_m: 
						#this code allows the player to scroll through a menu selection screen
						self.level.toggle_menu() 
						
			# this line seems serve as a background colour for the display screen, which is apparently the colour of water
			self.screen.fill(WATER_COLOR) 
			#this line seems run the layout for the level that the user plays on
			self.level.run() 
			#this line seems to update the display to show the change in level or background
			pygame.display.update() 
			#this line seems to run the framerate of the entire game
			self.clock.tick(FPS) 
			
#this if statement makes sure that __name__ is equal to '__main__'
if __name__ == '__main__': 
	#this line sets a game variable equal to a Game() function
	game = Game() 
	#this line finally runs all of this code to let the game run
	game.run() 
