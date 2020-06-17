from unicurses import *
numcolors = 0 #used to create ids

# ill put here aliases to make various curses things
# more tasty to use... but its mostly setting up colors
# i dont want to remember that colors are
# attributes, i want to put colon(color) to switch to
# that color.

def make_color(fg,bg):
	global numcolors
	numcolors = id = numcolors+1
	init_pair(id,fg,bg)
	return id

def colon(color):
	attron(color_pair(color)) #any->color
def coloff(color):
	attroff(color_pair(color)) #any->default
def wcolon(window,color):
	wattron(window,color_pair(color))
def wcoloff(window,color):
	wattroff(window,color_pair(color))

def set_colors(custom=True):
	if (custom): #overriding the terminal presets for the colors listed here
		init_color(COLOR_RED, 1000,0,200)
		init_color(COLOR_BLUE, 300,100,1000)
		init_color(COLOR_GREEN, 600,800,0)
		init_color(COLOR_MAGENTA, 600,100,600)
		init_color(COLOR_YELLOW, 1000,500,0)
		init_color(COLOR_WHITE, 900,1000,600)
	#make color pairs - for this game i anticipate only these on black
	#or these on black, reversed
	red = make_color(COLOR_RED,COLOR_BLACK)
	blue = make_color(COLOR_BLUE,COLOR_BLACK)
	green = make_color(COLOR_GREEN,COLOR_BLACK)
	purple= make_color(COLOR_MAGENTA,COLOR_BLACK)
	orange = make_color(COLOR_YELLOW,COLOR_BLACK)
	white = make_color(COLOR_WHITE, COLOR_BLACK)

	return [red,blue,green,purple,orange,white]
