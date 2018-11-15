import curses
import curses.textpad
import sys
import os
import glob
from os import listdir
from os.path import isfile, join
import CLI_Audio_Exception


class FrontEnd:
    nowPlaying = False  # now playing set to false so nothing plays initially
    folderPath = '/Users/isfar/Desktop/collabProj/cli-audio/media/'  # directory of media files
    mediaFiles = os.listdir(folderPath)  # searches in the given folder path for the media files

    def __init__(self, player):  # constructor method for the class
        self.player = player
        curses.wrapper(self.menu)

    def menu(self, args):  # method for creating menu
        self.stdscr = curses.initscr()  # curses is initialized. returns a window object representing the entire screen
        self.stdscr.border()  # draws a border around the edges of the window
        while True:

            try:
                height, width = self.stdscr.getmaxyx()  # returns a tuple (y,x) of the height and width of the window
                if height < 16 and width < 60:
                    raise CLI_Audio_Exception.CLI_Audio_Screen_Size_Exception

                else:
                    self.stdscr.clear()  # cause the window to be repainted upon next call to refresh()
                    self.stdscr.border()  # draws a border around the edges of this window
                    self.stdscr.addstr(0, 0, "cli-audio",
                                       curses.A_REVERSE)  # paint the string at (0,0) a reverse video status line is displayed
                    self.stdscr.addstr(5, 10, "c - Change current song")  # paints the string at (5,10) on the window
                    self.stdscr.addstr(6, 10, "p - Play/Pause")  # paints the string at (6,10) on the window
                    self.stdscr.addstr(7, 10, "l - Library")  # paints the string at (7,10) on the window
                    self.stdscr.addstr(9, 10, "ESC - Quit")  ##paints the string at (9,10) on the window
                    self.updateSong()  # updateSong() method is called
                    self.stdscr.refresh()  # updates the window

            except CLI_Audio_Exception.CLI_Audio_Screen_Size_Exception:
                print("The screen size is below the minimum allowable of 60 x 16.")

            while True:
                height, width = self.stdscr.getmaxyx()  # returns a tuple (y,x) of the height and width of the window
                c = self.stdscr.getch()  # getting a character from user
                if c == 27:  # if esc is clicked
                    self.quit()  # player stops
                elif c == ord('p'):  # if p is clicked
                    if self.nowPlaying == True:  # if nowPlaying() method returns true here
                        self.player.pause()  # player is paused
                elif c == ord('c'):  # if c is clicked by the user
                        # if height >= 10 and width >= 90:
                        self.changeSong()  # changeSong() method is called
                        self.updateSong()  # updateSong() methos is called
                        self.stdscr.touchwin()  # pretend the whole window has been changed, for purposes of drawing optimizations
                        self.stdscr.refresh()  # updates the window
                elif c == ord('l'):  # if l is clicked
                    self.displayDir()  # displayDir() method called
                resize = curses.is_term_resized(height, width)  # resizes the window to to the specified dimensions
                if resize is True:
                    break

    def updateSong(self):
        self.stdscr.addstr(15, 10, "                                        ")
        self.stdscr.addstr(15, 10,
                           "Now playing: " + self.player.getCurrentSong())  # if a song is updated the current song is displayed

    def changeSong(self):

        changeWindow = curses.newwin(5, 40, 5, 50)  # return a new window
        changeWindow.border()  # draws a border around the new window
        changeWindow.addstr(0, 0, "What is the file path?",
                            curses.A_REVERSE)  # displays the specified string on the new wiindow
        self.stdscr.refresh()  # updates the window
        curses.echo()  # enter echo mode.each character input is echoed to the screen as it is entered
        path = changeWindow.getstr(1, 1, 30)  # reads a string from the user
        curses.noecho()  # leave echo mode. echoeing of input character inoout is turned off.
        del changeWindow  # changed window removed
        self.stdscr.touchwin()  # pretend the whole window has been changed, for purposes of drawing optimizations
        self.stdscr.refresh()  # updates the window
        pathWithExt = (path.decode(encoding="utf-8")) + '.wav'  # path with .wav extension defined
        if (pathWithExt) in self.mediaFiles:  # if the song is present in the media files directory
            if self.nowPlaying == True:  # if a song is currently playing
                self.player.stop()  # stop the player
        #try:
            #self.player.play(path.decode(encoding="utf-8"))  # play the song that has been requested
           # self.nowPlaying = True  # player plays song
            #except
            else:
                songDntExistsWindow = curses.newwin(5, 40, 5, 50)  # another window defined
                songDntExistsWindow.border()  # draws a border around this window
                songDntExistsWindow.addstr(1, 1,"No such song in media folder")  # prints the specified string at (1,1) on this new window
            self.stdscr.refresh()  # updates the undow
            curses.echo()  # enter echo mode. each character input is echoed to the screen as it is entered
            input = songDntExistsWindow.getstr(3, 1, 30)  # reads user input
            curses.noecho()  # leave echo mode. echoeing of input character inoout is turned off.
            del songDntExistsWindow  # changed window removed
            self.stdscr.touchwin()  # pretend the whole window has been changed, for purposes of drawing optimizations
            self.stdscr.refresh()  # updates the window


def displayDir(self):
    libraryWindow = curses.newwin(len(self.mediaFiles) + 2, 40, 5, 50)  # window defined
    libraryWindow.border()  # draws border around window
    libraryWindow.addstr(0, 0, "Available songs:",
                         curses.A_REVERSE)  # paint the string at (0,0) a reverse video status line is displayed
    placement = 1
    for element in range(len(self.mediaFiles)):
        if self.mediaFiles[element] != 'README.md' and self.mediaFiles[element] != '.DS_Store':  # valid media file
            libraryWindow.addstr(placement, 1, self.mediaFiles[element][
                                               :-4])  # prints the specified string at the given position on window
            self.stdscr.refresh()  # updates the window
            print(self.mediaFiles[element])  # print media files
            placement += 1
    str = libraryWindow.getstr(element + 1, 1, 30)  # reads a string from the user
    del libraryWindow  # window removed
    self.stdscr.touchwin()  # pretend the whole window has been changed, for purposes of drawing optimizations
    self.stdscr.refresh()  # updates the window


def quit(self):
    if self.nowPlaying == True:  # is a song is currently playing
        self.player.stop()  # stop playing song
        exit()  # leave player
