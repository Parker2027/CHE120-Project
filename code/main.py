*import pygame, sys #this line imports the pygame file in order for the game's visuals and a sys file
from settings import * #this line seems to call up some code from a settings file elsewhere in this game's file
from level import Level #this line seems to call up a function Level from a level file elsewhere in this game's code

class Game: #this line establishes a new class called Game, where we can assume most of the work for running and starting the game can be found
	def __init__(self): #this function starts the code for starting the game

		# general setup #the original programmer lets us know that the general setup for the game exists in this section
		pygame.init() #this is the code that starts the actual game using the pygame file
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH)) #this line establishes the display screen for the game
		pygame.display.set_caption('Zelda') #this line produces a caption for the game that says 'Zelda'
		self.clock = pygame.time.Clock() #this line makes a clock that runs in game

		self.level = Level() #this line likely acts selects the level for the player to play in

		# sound #the original programmer lets us know that this section produces the sounds for the game
		main_sound = pygame.mixer.Sound('../audio/main.ogg') #this line codes for the main theme of the game
		main_sound.set_volume(0.5) #this line codes for the volume of the main theme for the game and sets it at 0.5
		main_sound.play(loops = -1) #this line plays the main theme of the game and loops it indefinitely
	
	def run(self): #this function runs the gsme
		while True: #this while loop uses the parameters true, meaning that the game is running and the player is on some sort of select screen
			for event in pygame.event.get(): #this for loop is for various events in event.get() function
				if event.type == pygame.QUIT: #this if statement is for the scenario that the player has decided to quit the program and exit the game
					pygame.quit() #this line quits the pygame file and cancels the running of code
					sys.exit() #this line exits the system and shuts down the program
				if event.type == pygame.KEYDOWN: #this if statement is for the event that the player scrolls down a list of options using the down arrow key
					if event.key == pygame.K_m: #this if statement seems to code for an event in the menu
						self.level.toggle_menu() #this code allows the player to scroll through a menu selection screen

			self.screen.fill(WATER_COLOR) #this line seems serve as a background colour for the display screen, which is apparently the colour of water
			self.level.run() #this line seems run the layout for the level that the user plays on
			pygame.display.update() #this line seems to update the display to show the change in level or background
			self.clock.tick(FPS) #this line seems to run the framerate of the entire game

if __name__ == '__main__': #this if statement makes sure that __name__ is equal to '__main__'
	game = Game() #this line sets a game variable equal to a Game() function
	game.run() #this line finally runs all of this code to let the game run
