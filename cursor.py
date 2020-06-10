from unicurses import *
from util import *
class RogueCursor:
	def center(self):
		self.x = self.max_x/2
		self.y = self.max_y/2

	def __init__ (self, stdscr, body, color = None, attr = None):
		yy,xx = stdscr.getmaxyx()
		self.max_x,self.max_y = xx-1,yy-1
		self.center()
		self.body = body
		del stdscr
		self.window = newwin(1,1,self.y,self.x)
		waddstr (self.window,self.body)
		self.panel = new_panel(self.window)
		self.attr = attr
		if (color != None):
			self.set_color(color)
		self.update();
	def set_color(self, color):
		self.color = color
		waddstr(self.window, self.body,
			color_pair(self.color)+self.attr)
		self.update()
	def update(self, key=None):
		self.move(key)
	def move(self, key=None, vel=1):
		xx,yy = self.x, self.y
		if (key == KEY_UP
		and self.y - vel > 0):
			self.y -= vel
		elif(key == KEY_DOWN
		and self.y + vel < self.max_y):
			self.y += vel
		elif (key == KEY_LEFT
		and self.x - vel  > 0):
			self.x -= vel
		elif (key == KEY_RIGHT
		and self.x + vel < self.max_x):
			self.x += vel
		moved = (self.x != xx or self.y != yy)
		if (moved):
			move_panel(self.panel, self.y, self.x)
			self.update()
