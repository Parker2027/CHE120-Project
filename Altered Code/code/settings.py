# game setup
#Width and Height of game display
WIDTH    = 1280	
HEIGTH   = 720
#Frames Per Second and Tile Size which stays static while the game is running
FPS      = 60
TILESIZE = 64
####################################################
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui 
#Setting the height of each resource bar
BAR_HEIGHT = 20
#Width of the Health Bar
HEALTH_BAR_WIDTH = 200
#Width of the energy resource bar
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
#What font the UI is written in as well as its size
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
#Colours of several assets being set for the level display
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
#Colours used for the resource bars
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
#Colours used when the upgrade menu is opened
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons 
#All five weapons assigned cooldown values which determines how fast the player can attack
#damage value assigned to each weapon to determine how much health is lost by enemies when hit by the weapon
#size values which determine the size of the unique sprite assigned to each weapon with a .png
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}

# magic
#Assigning values to the magic system of the game
#Flame "spell" has a strength which determines its damage value and a graphic size determining the size of the .png sprite used
#Heal "spell" is assigned a strength value, determining how much health is gained when used, and a graphic value to determine the size of the .png sprite used
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'../graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'../graphics/particles/heal/heal.png'}}

# enemy
#Assigning each enemy a health value which determines how much damage can be inflicted on them
#Experience determines how much experience resource is gained by the player when the enemy dies
#Damage determines how much health is lost by the player when the enemy attacks them
#Each attack is given a different "type", giving them a unique sound when the attack is instigated
#Speed determines how fast the enemies can move across tiles
#The attack radius determines where the damage of the attack is valid
#The notice radius is what distance the enemy will begin chasing the player
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
