#imports the pygame module and the sys module
import pygame, sys
#imports everything about game window settings from settings1.py into main1.py
from settings import *
#imports sprites and displays from level.py into main.py
from level import Level

#creates the class "Game"
class Game:
	#adds value "Self" to class "Game"
	def __init__(self):
		
		#initiates pygame
		# general setup
		pygame.init()
		#creates the game window and defines the size
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		#changes the name of the game window
		pygame.display.set_caption('CHE120 Project')
		#creates a clock for the game
		self.clock = pygame.time.Clock()
		
		#
		self.level = Level()
	
	#defines a function that determines if the game should be running
	def run(self):
		#sets parameters for when the game should be running
		while True:
			#
			for event in pygame.event.get():
				#if the game is exited do the actions listed below
				if event.type == pygame.QUIT:
					#quit module pygame if game is exited
					pygame.quit()
					#quit sys module if game is exited
					sys.exit()

			#makes the background of the game window black
			self.screen.fill('black')
			#
			self.level.run()
			#updates the game window
			pygame.display.update()
			#sets the FPS of the game
			self.clock.tick(FPS)

#if the 
if __name__ == '__main__':
	game = Game()
	game.run()
