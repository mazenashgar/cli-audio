import curses
import curses.textpad

import sys
import os
import glob
from os import listdir
from os.path import isfile, join

class FrontEnd:

    nowPlaying = False
    mediaFiles = os.listdir("media")

    def __init__(self, player):
        self.player = player
        curses.wrapper(self.menu)

    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        while True:
            height, width = self.stdscr.getmaxyx()
            if height >= 16 and width >= 60:
              self.stdscr.clear()
              self.stdscr.border()
              self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
              self.stdscr.addstr(5,10, "c - Change current song")
              self.stdscr.addstr(6,10, "p - Play/Pause")
              self.stdscr.addstr(7,10, "l - Library")
              self.stdscr.addstr(9,10, "ESC - Quit")
              #self.updateSong()
              self.stdscr.refresh()
            while True:
              height, width = self.stdscr.getmaxyx()
              c = self.stdscr.getch()
              if c == 27:
                  self.quit()
              elif c == ord('p'):
                  if self.nowPlaying == True:
                       self.player.pause()
              elif c == ord('c'):
                  #if height >= 10 and width >= 90:
                      self.changeSong()
                      self.updateSong()
                      self.stdscr.touchwin()
                      self.stdscr.refresh()
              elif c == ord('l'):
                  self.displayDir()
              resize = curses.is_term_resized(height,width)
              if resize is True:
                 break
              self.updateSong()
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        
             changeWindow = curses.newwin(5, 40, 5, 50)
             changeWindow.border()
             changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
             self.stdscr.refresh()
             curses.echo()
             path = changeWindow.getstr(1,1, 30)
             curses.noecho()
             del changeWindow
             self.stdscr.touchwin()
             self.stdscr.refresh()
             pathWithExt = (path.decode(encoding="utf-8")) + '.wav'
             if (pathWithExt) in self.mediaFiles:
                  if self.nowPlaying == True:
                      self.player.stop()
                  self.player.play(path.decode(encoding="utf-8"))
                  self.nowPlaying = True
             else:
                 songDntExistsWindow = curses.newwin(5, 40, 5, 50)
                 songDntExistsWindow.border()
                 songDntExistsWindow.addstr(1,1, "No such song in media folder")
                 self.stdscr.refresh()
                 curses.echo()
                 input = songDntExistsWindow.getstr(3,1, 30)
                 curses.noecho()
                 del songDntExistsWindow
                 self.stdscr.touchwin()
                 self.stdscr.refresh()
        
    def displayDir(self):
        libraryWindow = curses.newwin(len(self.mediaFiles)+2, 40, 5, 50)
        libraryWindow.border()
        libraryWindow.addstr(0,0, "Available songs:", curses.A_REVERSE)
        placement = 1
        for element in range(len(self.mediaFiles)):
            if self.mediaFiles[element] != 'README.md' and self.mediaFiles[element] != '.DS_Store':
                 libraryWindow.addstr(placement, 1, self.mediaFiles[element][:-4])
                 self.stdscr.refresh()
                 placement += 1
        curses.echo()
        str = libraryWindow.getstr(element+1,1,30)
        del libraryWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

    def quit(self):
        if self.nowPlaying == True:
        	self.player.stop()
        exit()
