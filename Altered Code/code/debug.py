import pygame 
#this line of code exists to import the pygame file
pygame.init() 
#this line of code seems to initiate the contents of the pygame file
font = pygame.font.Font(None,30) 
# this line of code exists to spit out a font for the game, which seems to be size 30 and potentially a title screen for the game

def debug(info,y = 10, x = 10): 
	#this line is the set up for a debugging function, using the input variables info, y = 10, and x = 10
	display_surface = pygame.display.get_surface() 
	# this line might serve as the background screen for the game, or at least for the start screen of the game
	debug_surf = font.render(str(info),True,'White') 
	#this line seems to be for producing white text font for the contents of the info variable
	debug_rect = debug_surf.get_rect(topleft = (x,y)) 
	#this line produces a rectangle with the dimensions of x = 10 and y = 10; strong chance the text font is contained within this rectangle
	pygame.draw.rect(display_surface,'Black',debug_rect) 
	#this another rectangle, this time in black that serves as a display screen for the game
	display_surface.blit(debug_surf,debug_rect) 
	#this seems like a function within the function that runs the code for producing text and the white rectangle
