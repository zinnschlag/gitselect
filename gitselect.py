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
        ypad = len (files)
        if ypad<self.ysize-1:
            ypad = self.ysize-1
        self.candidates = curses.newpad (ypad, self.xsize)
        y = 0
        for f in files:
            self.candidates.addnstr (y, 0, f, self.xsize)
            y = y + 1
        self.candidates.refresh (0, 0, 0, 0, self.ysize-2, self.xsize-1)

    def filter_ (self, pattern):
        files = [f for f in self.files if pattern in f]
        self.candidates.clear()
        y = 0
        for f in files:
            self.candidates.addnstr (y, 0, f, self.xsize)
            y = y + 1
        self.candidates.refresh (0, 0, 0, 0, self.ysize-2, self.xsize-1)

def select (screen, files):
    screen.refresh()
    ysize, xsize = screen.getmaxyx()
    candidates = Files (files, screen)
    pattern = curses.newwin (1, xsize, ysize-1, 0)
    text = curses.textpad.Textbox (pattern)
    pattern.refresh()
    while True:
        c = screen.getch()
        if c==27: # ESC
            break
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
    curses.wrapper (select, files)
