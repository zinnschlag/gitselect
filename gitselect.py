#!/usr/bin/python

import subprocess
import sys
import curses
import curses.textpad
import string

class Files:

    def __init__ (self, files, screen):
        self.files = files
        self.screen = screen
        self.ysize, self.xsize = screen.getmaxyx()
        ypad = len (files) +1 # XXX
        if ypad<self.ysize-1:
            ypad = self.ysize-1
        self.candidates = curses.newpad (ypad, self.xsize)
        self.candidates.bkgdset (' ', curses.color_pair (2))
        self.index = 0
        self.size = len (self.files)
        self.pattern = None
        self._update()

    def filter_ (self, pattern):
        files = [f for f in self.files if pattern in f]
        self._update (pattern)
        self.pattern = pattern

    def _update (self, pattern=None):
        if pattern is None:
            files = self.files
        else:
            files = [f for f in self.files if pattern in f]
        self.size = len (files)
        self.candidates.clear()
        y = 0
        for f in files:
            string = f.ljust (self.xsize)
            color_index = 2
            if y==self.index:
                color_index = 1
            self.candidates.addnstr (y, 0, string, self.xsize, curses.color_pair (color_index))
            y = y + 1
        self.candidates.refresh (0, 0, 0, 0, self.ysize-2, self.xsize-1)

    def up (self):
        if self.index>0:
            self.index = self.index - 1
            self._update (self.pattern)

    def down (self):
        if self.index<self.size-1:
            self.index = self.index + 1
            self._update (self.pattern)

    def get (self):
        if self.pattern is None:
            files = self.files
        else:
            files = [f for f in self.files if self.pattern in f]
        if self.index>=len (files):
            return None
        return files[self.index]


def select (screen, files):
    curses.init_pair (1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair (2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    screen.refresh()
    ysize, xsize = screen.getmaxyx()
    candidates = Files (files, screen)
    pattern = curses.newwin (1, xsize, ysize-1, 0)
    text = curses.textpad.Textbox (pattern)
    pattern.refresh()
    while True:
        c = screen.getch()
        if c==27: # ESC
            return None
        if c==curses.KEY_UP:
            candidates.up()
        if c==curses.KEY_DOWN:
            candidates.down()
        if c==10: # return
            return candidates.get()
        text.do_command (c)
        candidates.filter_ (string.strip (text.gather()))
        pattern.refresh()

if __name__ == "__main__":
    p = subprocess.Popen ("git ls-files", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True)
    out, err = p.communicate()
    if len (err)!=0:
        print err
        sys.exit (1)
    files = out.splitlines()
    print curses.wrapper (select, files)
