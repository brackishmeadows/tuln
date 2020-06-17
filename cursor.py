# coding: utf-8
from unicurses import *
from util import *
import logging

class Cursor(object):
	def __init__ (self, stdscr, body, color, attr = A_NORMAL):
		yy,xx = stdscr.getmaxyx()
		self.max_x,self.max_y = xx-1,yy-1 #collision bounds
		self.center()
		self.body = body
		self.attr = attr
		self.color = color
		self.window=None
		self.panel=None
		self.draw()
	def draw(self):
		del self.window
		del self.panel
		self.window = newwin(1,1,self.y,self.x)
		self.panel = new_panel(self.window)
		self.set_color(self.color)
	def center(self):
		self.x = self.max_x/2
		self.y = self.max_y/2
		self.draw
	def set_body(self,char):
		logging.info('set body '+char)
		self.body = char
		self.draw()
	def set_color(self, color):
		if color==None: return
		self.color = color
		attr = self.attr
		if attr == None: attr = 0
		waddstr(self.window, self.body,
			color_pair(self.color)+attr)

	def update(self, key=None):  #interface, pass keys to it
		pass

class Gun(Cursor):
	def __init__ (self, stdscr, body, color=None, attr=None):
		logging.info('start gun')
		super(Gun,self).__init__(stdscr,body,color,attr)
		self.agent = None
		self.facing = 1
	def setAgent(self,agent,no_backsies=False):
		logging.info('add agent to gun')
		self.agent = agent
		if (not no_backsies): agent.setGun(self,True)
	def update(self,key=None):
		xx,yy = self.x, self.y
		if (key == 'z'):
			#pew
			pass
		try:
			if (self.agent != None):
				ax = self.agent.x
				ay = self.agent.y
				if (key == KEY_LEFT):
					self.facing = -1
					self.set_body('┑')
				elif (key == KEY_RIGHT):
					self.facing = 1
					self.set_body('┍')
				self.x =ax+self.facing
				self.y =ay
				moved = (self.x != xx or self.y != yy)
				if (moved):
					logging.info('gun moved')
					move_panel(self.panel, self.y, self.x)
					self.update() #with no key
		except:
			pass
			logging.warning('GUN:no agent')


class Rogue(Cursor):
	def __init__ (self, stdscr, body, color=None, attr=None):
		super(Rogue,self).__init__(stdscr,body,color,attr)
		self.gun = None
		logging.info('rogue start')
	def setGun(self,gun,no_backsies=False):
		logging.info('add gun to rogue')
		self.gun = gun
		if (not no_backsies): gun.setAgent(self,True)
	def update(self, key=None):
		self.move(key)
		try:
			if(self.gun is not None):
				self.gun.update(key)
		except:
			pass
			logging.warning("ROGUE: no gun")
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
			self.update() #with no key
