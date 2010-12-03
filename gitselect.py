#!/usr/bin/python

import subprocess
import sys
import curses
import curses.textpad

def select (screen, files):
    ysize, xsize = screen.getmaxyx()
    ypad = len (files)
    if ypad<ysize-1:
        ypad = ysize-1
    candidates = curses.newpad (ypad, xsize)
    y = 0
    for f in files:
        candidates.addnstr (y, 0, f, xsize)
        y = y + 1
    pattern = curses.newwin (1, xsize, ysize-1, 0)
    text = curses.textpad.Textbox (pattern)
    screen.refresh()
    pattern.refresh()
    candidates.refresh (0, 0, 0, 0, ysize-2, xsize-1)
    while True:
        c = screen.getch()
        if c==27: # ESC
            break
        text.do_command (c)
        pattern.refresh()
        candidates.refresh (0, 0, 0, 0, ysize-2, xsize-1)

if __name__ == "__main__":
    p = subprocess.Popen ("git ls-files", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True)
    out, err = p.communicate()
    if len (err)!=0:
        print err
        sys.exit (1)
    files = out.splitlines()
    curses.wrapper (select, files)
