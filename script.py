import sys, ctypes
import pytz
import time
from datetime import datetime
from ctypes import windll
import os
import pip
import importlib
import subprocess
# import install packages
import numpy as np
from numpy import frombuffer, uint8
import cv2
import win32gui, win32con, win32ui, win32api
import imutils
# import matplotlib.pyplot as plt
from PIL import Image
from pywinauto import Application
import pywinauto
import pyscreenshot
path = os.getcwd() # 'D:\\platform-tools\\moonlight\\Moonlight_PC'
os.chdir(path)

try:
    exec(open('setup.py',encoding="utf-8").read())
except:
    exec(open('setup.py').read())
try:
    exec(open('time.py',encoding="utf-8").read())
except:
    exec(open('time.py').read())
try:
    exec(open('function_PC.py',encoding="utf-8").read())
except:
    exec(open('function_PC.py').read())
    

if is_admin():
    # MAP['掛機'] = (0.822, 0.594, 0.759, 0.637, '流浪民溫泉帶', '尼普爾海姆遺址')
    Game = Game_obj()
    #Game.accounts = [2,3,4,1]
    #Game.lst_friends = [(),(1,2,3,11,12),(1,2,3,5,8),(1,2,11,12,13)]
    Game.accounts = [1]
    print('滑鼠位置:' + str(Game.getPosition()))
    Game.gameloop()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
