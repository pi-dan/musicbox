#!/usr/bin/env python
#encoding: UTF-8

'''
网易云音乐 Entry
'''

from menu import Menu
import curses

def start():
    curses.setupterm()
    lines=curses.tigetnum('lines')
    cols=curses.tigetnum('cols')
    if int(lines)<22:
        print '  窗口太小，请调整窗口高度' 
    elif int(cols)<60:
        print '  窗口太小，请调整窗口宽度'
    else:
        Menu().start()

if __name__ == '__main__':
    start()
