#!/usr/bin/env python
# coding: utf-8

UNDEFINED = object()

from unicurses import *
from random import randint
from cursor import *
from menu import *
import subprocess as bash
import logging
showmenu = None
logger = None

def spam(str, max_x=10, max_y=10, count=2):
  offset_x = len(str) + 2
  for _ in range(count):
    move (randint(1,max_y-3),
    randint(2,max_x-offset_x)) #(y,x)
    addstr (str)

def title():
  mvaddstr (0,2," TULN ")

def makemenu(width,ypos,xpos,msg,options,color):
  menu= newwin(len(options)+3,width, ypos, xpos)
  wcolon(menu,color)
  box(menu)
  mvwaddstr(menu,0,1,msg)
  offset=0
  for choice in options:
    mvwaddstr(menu, 1+offset, 4, choice);
    offset += 1
    menu_panel = new_panel(menu)
    bottom_panel(menu_panel)
  return [menu,menu_panel]

def startLog():
    global logger
    logger= logging.getLogger(__file__)
    handler = logging.FileHandler(__file__+".log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info("begin logging")
    

def win(): #the window
  showmenu = True;
  #various curses invokes
  stdscr = initscr()
  start_color()
  noecho()
  curs_set(False)
  keypad(stdscr, True)
  stdscr.nodelay(1) #kill cooked mode
  red,blue,green,purple,orange,white=set_colors()
  #set_colors() from util.py
  cursor = Rogue(stdscr,'+', green, A_REVERSE)
  #RogueCursor from cursor.py
  gun = Gun(stdscr,'┍',white)
  cursor.setGun(gun)
  max_y, max_x = getmaxyx(stdscr);
  if (showmenu):
    menu, menu_panel = makemenu( max_x - 11,
      max_y - 8, 5,
      "you are travelling to distant TULN...",
      ["continue", "scry", "exit"],
      green
    )

  buff = "" #key buffer
  buff_showlast = max_x - 6
  title()
  while True:
    colon(orange)
    if (randint(0,1000) < 1):
      spam(" . . * . * . ", max_x, max_y)
      update_panels()
      doupdate()
      c = getch()
      cursor.update(c)
      if (c == -1 ): #no key
        continue
      elif (c == 27 ): #esc
        break #terminate the loop and the window
      elif (c == 9 ): #toggle
        if (showmenu):
          showmenu = False
          hide_panel(menu_panel)
        else:
          showmenu = True
          show_panel(menu_panel)
      elif (c == KEY_BACKSPACE ): #erase
        buff = buff[:-1]
        tail = buff[-buff_showlast:]
        mvaddstr (max_y-2,2,(max_x-4) * " " )
        mvaddstr (max_y-2,4,tail)
      elif ( 31 < c < 255 ): #buffer
        buff += chr(c)
        tail = buff[-buff_showlast:]
        mvaddstr (max_y-2,2, chr(c),
        color_pair(red))
        addstr(" %s" % (tail))
      else: c = ord('0') #i forget why

def main():
  startLog()
  win()
  endwin()
  bash.call(["clear"])
  return 0

if (__name__ == "__main__"):
  main()
