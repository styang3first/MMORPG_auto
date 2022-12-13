# encoding:utf-8
import tkinter as tk
from tkinter import *
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
path = os.getcwd() # 'D:\\platform-tools\\moonlight\\Moonlight_PC'
os.chdir(path)

win = tk.Tk()
# 標題
win.title("月光雕刻施輔助腳本")
rr, cc=0, 0
# 大小, 顏色, 透明度, 置頂
win.geometry("600x735+100+100")
#win.minsize(width=400, heigh=200)
#win.maxsize(width=400, heigh=200)
win.resizable(False, False)

### default values
try:
    exec(open('setup.py',encoding="utf-8").read())
except:
    exec(open('setup.py').read())

f_xx, f_yy = 10, 10
### 基本資訊
f_ww, f_hh = 580, 100
Basic_lf = tk.LabelFrame(text="遊戲視窗設定", height=10)
Basic_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)

xx, yy = 10, 10
len1, len2 = 4, 12 # text length, value length
lb = tk.Label(Basic_lf, text='視窗標題')
lb.place(x=xx, y=yy)
xx = xx + 14*len1
character_id_en = tk.Entry(Basic_lf)
character_id_en.insert(0, character_id) # default value
character_id_en.place(x=xx, y=yy, width = max(20, 10*len2) )
xx = xx + max(20, 10*len2)

len1, len2 = 6, 1 # text length, value length
lb = tk.Label(Basic_lf, text='復活次數上限')
lb.place(x=xx, y=yy)
xx += 14*len1
num_resurrect_en = tk.Entry(Basic_lf)
num_resurrect_en.insert(0, num_resurrect)
num_resurrect_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 6, 3 # text length, value length
lb = tk.Label(Basic_lf, text='復活間隔(秒)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_resurrect_en = tk.Entry(Basic_lf)
gap_resurrect_en.insert(0, gap_resurrect)
gap_resurrect_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


xx = xx + 30
xx_temp1 = xx
len1, len2 = 8, 1 # text length, value length
team_accept_cb = BooleanVar()
team_accept_chk = tk.Checkbutton(Basic_lf, text='自動確認加入隊伍', variable=team_accept_cb, onvalue=True, offvalue=False)
if team_accept:
    team_accept_chk.select()
team_accept_chk.place(x=xx+5, y=yy-2)
xx += 14*len1


xx, yy = 10, yy+30
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Basic_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_basic_en = tk.Entry(Basic_lf)
equip_basic_en.insert(0, equip_basic)
equip_basic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Basic_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_basic_en = tk.Entry(Basic_lf)
statue_basic_en.insert(0, statue_basic)
statue_basic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Basic_lf, text='寵物編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_basic_en = tk.Entry(Basic_lf)
friend_basic_en.insert(0, friend_basic)
friend_basic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

yy = yy - 3
len1, len2 = 6, 1 # text length, value length
water_basic_cb = BooleanVar()
water_basic_chk = tk.Checkbutton(Basic_lf, text='30% HP藥水', variable= water_basic_cb, onvalue=True, offvalue=False)
if water_basic:
    water_basic_chk.select()
water_basic_chk.place(x=xx, y=yy)
xx += 14*len1


xx = xx + 5
len1, len2 = 8, 1 # text length, value length
check_boss_cb = BooleanVar()
check_boss_chk = tk.Checkbutton(Basic_lf, text='截圖王的動靜', variable=check_boss_cb, onvalue=True, offvalue=False)
if check_boss:
    check_boss_chk.select()
check_boss_chk.place(x=xx+5, y=yy)
xx += 14*len1

xx = xx_temp1
len1, len2 = 8, 1 # text length, value length
team_add_cb = BooleanVar()
team_add_chk = tk.Checkbutton(Basic_lf, text='自動邀請密語人', variable=team_add_cb, onvalue=True, offvalue=False)
if team_add:
    team_add_chk.select()
team_add_chk.place(x=xx+5, y=yy)
xx += 14*len1

### 食物, 按鍵, 間隔
f_xx, f_yy = 10, f_yy+f_hh
f_ww, f_hh = 230, 70
Food_lf = tk.LabelFrame(text="食物設定")
Food_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_food_cb = BooleanVar()
enable_food_chk = tk.Checkbutton(text='開啟功能', variable= enable_food_cb, onvalue=True, offvalue=False)
if enable_food:
    enable_food_chk.select()
enable_food_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy


xx, yy = 10, 10
len1, len2 = 4, 3 # text length, value length
lb = tk.Label(Food_lf, text='食物按鈕')
lb.place(x=xx, y=yy)
xx += 14*len1
key_food_en = tk.Entry(Food_lf)
key_food_en.insert(0, key_food)
key_food_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 6, 3 # text length, value length
lb = tk.Label(Food_lf, text='食物間隔(分鐘)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_food_en = tk.Entry(Food_lf)
gap_food_en.insert(0, gap_food)
gap_food_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

### 交易所: 間隔
f_ww, f_hh = 170, 70
Auction_lf = tk.LabelFrame(text="交易所設定")
Auction_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_auction_cb = BooleanVar()
enable_auction_chk = tk.Checkbutton(text='開啟功能', variable= enable_auction_cb, onvalue=True, offvalue=False)
if enable_auction:
    enable_auction_chk.select()
enable_auction_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy


xx, yy = 10, 10
len1, len2 = 8, 3 # text length, value length
lb = tk.Label(Auction_lf, text='交易所間隔(分鐘)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_auction_en = tk.Entry(Auction_lf)
gap_auction_en.insert(0, gap_auction)
gap_auction_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


### 每日副本: 小時, 分鐘
f_ww, f_hh = 180, 70
Daily_lf = tk.LabelFrame(text="每日副本設定")
Daily_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_daily_cb = BooleanVar()
enable_daily_chk = tk.Checkbutton(text='開啟功能', variable= enable_daily_cb, onvalue=True, offvalue=False)
if enable_daily:
    enable_daily_chk.select()
enable_daily_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(Daily_lf, text='進場時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_daily_en = tk.Entry(Daily_lf)
hour_daily_en.insert(0, hour_daily)
hour_daily_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(Daily_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_daily_en = tk.Entry(Daily_lf)
min_daily_en.insert(0, min_daily)
min_daily_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

### 公會狩獵設定: 小時, 分鐘, 位置, 離開模式
### 預計新增: 裝備雕像
f_xx = 10
f_ww, f_hh = 550, 100
Guild_lf = tk.LabelFrame(text="公會狩獵設定")
Guild_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_hunt_cb = BooleanVar()
enable_hunt_chk = tk.Checkbutton(text='開啟功能', variable= enable_hunt_cb, onvalue=True, offvalue=False)
if enable_hunt:
    enable_hunt_chk.select()
enable_hunt_chk.place(x=f_xx + 14*6, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(Guild_lf, text='進場時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_guild_en = tk.Entry(Guild_lf)
hour_guild_en.insert(0, hour_guild)
hour_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(Guild_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_guild_en = tk.Entry(Guild_lf)
min_guild_en.insert(0, min_guild)
min_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx += 10
len1, len2 = 6, 5 # text length, value length
lb = tk.Label(Guild_lf, text='狩獵位置: X軸')
lb.place(x=xx, y=yy)
xx += 14*len1
x_guild_en = tk.Entry(Guild_lf)
x_guild_en.insert(0, x_guild)
x_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 5 # text length, value length
lb = tk.Label(Guild_lf, text='Y軸')
lb.place(x=xx, y=yy)
xx += 14*len1
y_guild_en = tk.Entry(Guild_lf)
y_guild_en.insert(0, y_guild)
y_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx, yy = 10, yy+30 # 換行
len1, len2 = 8, 1 # text length, value length
enter_pvp_cb = BooleanVar()
enter_pvp_chk = tk.Checkbutton(Guild_lf, text='進場開啟PVP', variable=enter_pvp_cb, onvalue=True, offvalue=False)
if enter_pvp:
    enter_pvp_chk.select()
enter_pvp_chk.place(x=xx, y=yy)
xx += 14*len1


len1, len2 = 8, 1 # text length, value length
leave_guild_cb = BooleanVar()
leave_guild_chk = tk.Checkbutton(Guild_lf, text='自動離開公會', variable=leave_guild_cb, onvalue=True, offvalue=False)
if leave_guild:
    leave_guild_chk.select()
leave_guild_chk.place(x=xx, y=yy)
xx += 14*len1


len1, len2 = 8, 1 # text length, value length
leave_pvp_cb = BooleanVar()
leave_pvp_chk = tk.Checkbutton(Guild_lf, text='結束關閉PVP', variable=leave_pvp_cb, onvalue=True, offvalue=False)
if leave_pvp:
    leave_pvp_chk.select()
leave_pvp_chk.place(x=xx, y=yy)
xx += 14*len1



### 突襲副本: 提前進場秒數, 9:00-24:00 (6 checkboxes)
### 預計新增: 裝備雕像
f_xx = 10
f_ww, f_hh = 550, 130
Raid_lf = tk.LabelFrame(text="突襲設定")
Raid_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_raid_cb = BooleanVar()
enable_raid_chk = tk.Checkbutton(text='開啟功能', variable= enable_raid_cb, onvalue=True, offvalue=False)
if enable_raid:
    enable_raid_chk.select()
enable_raid_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(Raid_lf, text='提前進場分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
early_raid_en = tk.Entry(Raid_lf)
early_raid_en.insert(0, early_raid)
early_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 3 # text length, value length
lb = tk.Label(Raid_lf, text='關卡等級')
lb.place(x=xx, y=yy)
xx += 14*len1
level_raid_en = tk.Entry(Raid_lf)
level_raid_en.insert(0, level_raid)
level_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 6, 3 # text length, value length
lb = tk.Label(Raid_lf, text='復活間隔(秒)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_resurrect_raid_en = tk.Entry(Raid_lf)
gap_resurrect_raid_en.insert(0, gap_resurrect_raid)
gap_resurrect_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

yy = yy-2
len1, len2 = 5, 1 # text length, value length
ticket_raid_cb = BooleanVar()
ticket_raid_chk = tk.Checkbutton(Raid_lf, text='使用入場券', variable=ticket_raid_cb, onvalue=True, offvalue=False)
if ticket_raid:
    ticket_raid_chk.select()
ticket_raid_chk.place(x=xx, y=yy)
xx += 14*len1

xx, yy = 10, yy+30 # 換行
len1, len2 = 3, 0 # text length, value length
lb = tk.Label(Raid_lf, text='場次: ')
lb.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 5, 1 # text length, value length
raid1_cb = BooleanVar()
raid1_chk = tk.Checkbutton(Raid_lf, text='09:00', variable=raid1_cb, onvalue=True, offvalue=False)
if raid1:
    raid1_chk.select()
raid1_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 5, 1 # text length, value length
raid2_cb = BooleanVar()
raid2_chk = tk.Checkbutton(Raid_lf, text='12:00', variable= raid2_cb, onvalue=True, offvalue=False)
if raid2:
    raid2_chk.select()
raid2_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 5, 1 # text length, value length
raid3_cb = BooleanVar()
raid3_chk = tk.Checkbutton(Raid_lf, text='15:00', variable= raid3_cb, onvalue=True, offvalue=False)
if raid3:
    raid3_chk.select()
raid3_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 5, 1 # text length, value length
raid4_cb = BooleanVar()
raid4_chk = tk.Checkbutton(Raid_lf, text='18:00', variable= raid4_cb, onvalue=True, offvalue=False)
if raid4:
    raid4_chk.select()
raid4_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 5, 1 # text length, value length
raid5_cb = BooleanVar()
raid5_chk = tk.Checkbutton(Raid_lf, text='21:00', variable= raid5_cb, onvalue=True, offvalue=False)
if raid5:
    raid5_chk.select()
raid5_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 5, 1 # text length, value length
raid6_cb = BooleanVar()
raid6_chk = tk.Checkbutton(Raid_lf, text='24:00', variable= raid6_cb, onvalue=True, offvalue=False)
if raid6:
    raid6_chk.select()
raid6_chk.place(x=xx, y=yy)
xx += 14*len1

xx, yy = 10, yy+30 # 換行
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Raid_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_raid_en = tk.Entry(Raid_lf)
equip_raid_en.insert(0, equip_raid)
equip_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Raid_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_raid_en = tk.Entry(Raid_lf)
statue_raid_en.insert(0, statue_raid)
statue_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Raid_lf, text='寵物編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_raid_en = tk.Entry(Raid_lf)
friend_raid_en.insert(0, friend_raid)
friend_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


xx = xx + 5
yy = yy - 3
len1, len2 = 9, 1 # text length, value length
sp_raid_cb = BooleanVar()
sp_raid_chk = tk.Checkbutton(Raid_lf, text='30% 狂暴藥劑', variable= sp_raid_cb, onvalue=True, offvalue=False)
if sp_raid:
    sp_raid_chk.select()
sp_raid_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
water_raid_cb = BooleanVar()
water_raid_chk = tk.Checkbutton(Raid_lf, text='30% HP藥水', variable= water_raid_cb, onvalue=True, offvalue=False)
if water_raid:
    water_raid_chk.select()
water_raid_chk.place(x=xx, y=yy)
xx += 14*len1

### 決鬥場: 開始, 結束, 是否只打到獎勵
### 預計新增: 裝備雕像
f_xx = 10
f_ww, f_hh = 550, 100
PVP_lf = tk.LabelFrame(text="決鬥場設定")
PVP_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_pvp_cb = BooleanVar()
enable_pvp_chk = tk.Checkbutton(text='開啟功能', variable= enable_pvp_cb, onvalue=True, offvalue=False)
if enable_pvp:
    enable_pvp_chk.select()
enable_pvp_chk.place(x=f_xx + 14*5, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(PVP_lf, text='開始時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_start_pvp_en = tk.Entry(PVP_lf)
hour_start_pvp_en.insert(0, hour_start_pvp)
hour_start_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(PVP_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_start_pvp_en = tk.Entry(PVP_lf)
min_start_pvp_en.insert(0, min_start_pvp)
min_start_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx = xx + 30
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(PVP_lf, text='結束時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_end_pvp_en = tk.Entry(PVP_lf)
hour_end_pvp_en.insert(0, hour_end_pvp)
hour_end_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(PVP_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_end_pvp_en = tk.Entry(PVP_lf)
min_end_pvp_en.insert(0, min_end_pvp)
min_end_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx += 20
xx_temp=xx
len1, len2 = 8, 1 # text length, value length
untilreward_cb = BooleanVar()
untilreward_chk = tk.Checkbutton(PVP_lf, text='拿到獎場就停止', variable=untilreward_cb, onvalue=True, offvalue=False)
if untilreward:
  untilreward_chk.select()
untilreward_chk.place(x=xx, y=yy)
xx += 14*len1

xx, yy = 10, yy+30 # 換行
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(PVP_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_pvp_en = tk.Entry(PVP_lf)
equip_pvp_en.insert(0, equip_pvp)
equip_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(PVP_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_pvp_en = tk.Entry(PVP_lf)
statue_pvp_en.insert(0, statue_pvp)
statue_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


len1, len2 = 4, 1 # text length, value length
lb = tk.Label(PVP_lf, text='寵物編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_pvp_en = tk.Entry(PVP_lf)
friend_pvp_en.insert(0, friend_pvp)
friend_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx = xx + 5
yy = yy - 3
len1, len2 = 9, 1 # text length, value length
sp_pvp_cb = BooleanVar()
sp_pvp_chk = tk.Checkbutton(PVP_lf, text='30% 狂暴藥劑', variable= sp_pvp_cb, onvalue=True, offvalue=False)
if sp_pvp:
    sp_pvp_chk.select()
sp_pvp_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 9, 1 # text length, value length
xx = xx_temp
ep_pvp_cb = BooleanVar()
ep_pvp_chk = tk.Checkbutton(PVP_lf, text='愛娜的祝福', variable= ep_pvp_cb, onvalue=True, offvalue=False)
if ep_pvp:
    ep_pvp_chk.select()
ep_pvp_chk.place(x=xx, y=yy)
xx += 14*len1

### 預計新增自動解狀態
f_xx = 10
f_ww, f_hh = 550, 70
DEBUFF_lf = tk.LabelFrame(text="解除異常狀態")
DEBUFF_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_debuff_cb = BooleanVar()
enable_debuff_chk = tk.Checkbutton(text='開啟功能', variable= enable_debuff_cb, onvalue=True, offvalue=False)
if enable_debuff:
    enable_debuff_chk.select()
enable_debuff_chk.place(x=f_xx + 14*6, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(DEBUFF_lf, text='技能頁碼')
lb.place(x=xx, y=yy)
xx += 14*len1
page_debuffskill_en = tk.Entry(DEBUFF_lf)
page_debuffskill_en.insert(0, page_debuffskill)
page_debuffskill_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(DEBUFF_lf, text='技能編號')
lb.place(x=xx, y=yy)
xx += 14*len1
key_debuffskill_en = tk.Entry(DEBUFF_lf)
key_debuffskill_en.insert(0, key_debuffskill)
key_debuffskill_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

def get_parameters():
    # enable
    enable_auction = enable_auction_cb.get()
    enable_food = enable_food_cb.get()
    enable_daily = enable_daily_cb.get()
    enable_hunt = enable_hunt_cb.get()
    enable_raid = enable_raid_cb.get()
    enable_pvp  = enable_pvp_cb.get()
    
    # window
    character_id = str(character_id_en.get())
    #
    num_resurrect = int(num_resurrect_en.get())
    gap_resurrect = int(gap_resurrect_en.get())
    #
    gap_auction = int(gap_auction_en.get())
    #
    key_food = str(key_food_en.get())
    gap_food  = int(gap_food_en.get())

    # daily
    hour_daily = int(hour_daily_en.get())
    min_daily = int(min_daily_en.get())

    # guild
    # equip_guild, sculpture_guild = 1, 1
    hour_guild = int(hour_guild_en.get())
    min_guild = int(min_guild_en.get())
    x_guild = float(x_guild_en.get())
    y_guild  = float(y_guild_en.get())
    enter_pvp = bool(enter_pvp_cb.get())
    leave_guild = bool(leave_guild_cb.get())
    lave_pvp  = bool(leave_pvp_cb.get())

    # raid
    # equip_raid, sculpture_raid = equip_raid_en.get(), sculpture_raid_en.get()
    early_raid = int(early_raid_en.get())
    raid1 = bool(raid1_cb.get())
    raid2 = bool(raid2_cb.get())
    raid3 = bool(raid3_cb.get())
    raid4 = bool(raid4_cb.get())
    raid5 = bool(raid5_cb.get())
    raid6   = bool(raid6_cb.get())
    level_raid = int(level_raid_en.get())
    ticket_raid  = bool(ticket_raid_cb.get())

    # pvp
    hour_start_pvp = int(hour_start_pvp_en.get())
    min_start_pvp = int(min_start_pvp_en.get())
    hour_end_pvp = int(hour_end_pvp_en.get())
    min_end_pvp = int(min_end_pvp_en.get())
    untilreward  = untilreward_cb.get()
   
def save_parameters():
    file1 = open("setup.py","w")
    # enable
    file1.write("enable_auction = " + str(enable_auction_cb.get()) + "\n")
    file1.write("enable_food = " + str(enable_food_cb.get()) + "\n")
    file1.write("enable_daily = " + str(enable_daily_cb.get()) + "\n")
    file1.write("enable_hunt = " + str(enable_hunt_cb.get()) + "\n")
    file1.write("enable_raid = " + str(enable_raid_cb.get()) + "\n")
    file1.write("enable_pvp  = " + str(enable_pvp_cb.get()) + "\n")
    file1.write("enable_debuff  = " + str(enable_debuff_cb.get()) + "\n")

    # basic
    file1.write("character_id = \"" +str(character_id_en.get()) + "\"\n")
    file1.write("num_resurrect = " +str(num_resurrect_en.get()) + "\n")
    file1.write("gap_resurrect = " +str(gap_resurrect_en.get()) + "\n")
    file1.write("equip_basic = " +str(equip_basic_en.get()) + "\n")
    file1.write("statue_basic = " +str(statue_basic_en.get()) + "\n")
    file1.write("friend_basic = " +str(friend_basic_en.get()) + "\n")
    file1.write("water_basic = " + str(water_basic_cb.get()) + "\n")
    file1.write("team_accept = " + str(team_accept_cb.get()) + "\n")
    file1.write("team_add = " + str(team_add_cb.get()) + "\n")
    file1.write("check_boss = " + str(check_boss_cb.get()) + "\n")

    # auction
    file1.write("gap_auction = " +str(gap_auction_en.get()) + "\n")

    # food
    file1.write("key_food = \"" +str(key_food_en.get()) + "\"\n")
    file1.write("gap_food = " +str(gap_food_en.get()) + "\n")

    # daily
    file1.write("hour_daily = " +str(hour_daily_en.get()) + "\n")
    file1.write("min_daily = " +str(min_daily_en.get()) + "\n")

    # guild
    file1.write("hour_guild = " +str(hour_guild_en.get()) + "\n")
    file1.write("min_guild = " +str(min_guild_en.get()) + "\n")
    file1.write("x_guild = " +str(x_guild_en.get()) + "\n")
    file1.write("y_guild = " +str(y_guild_en.get()) + "\n")
    file1.write("enter_pvp = " +str(enter_pvp_cb.get()) + "\n")
    file1.write("leave_guild = " +str(leave_guild_cb.get()) + "\n")
    file1.write("leave_pvp = " +str(leave_pvp_cb.get()) + "\n")

    # raid
    file1.write("early_raid = " + str(early_raid_en.get()) + "\n")
    file1.write("raid1 = " + str(raid1_cb.get()) + "\n")
    file1.write("raid2 = " + str(raid2_cb.get()) + "\n")
    file1.write("raid3 = " + str(raid3_cb.get()) + "\n")
    file1.write("raid4 = " + str(raid4_cb.get()) + "\n")
    file1.write("raid5  = " + str(raid5_cb.get()) + "\n")
    file1.write("raid6 = " + str(raid6_cb.get()) + "\n")
    file1.write("level_raid = " + str(level_raid_en.get()) + "\n")
    file1.write("ticket_raid = " + str(ticket_raid_cb.get()) + "\n")
    file1.write("equip_raid = " +str(equip_raid_en.get()) + "\n")
    file1.write("statue_raid = " +str(statue_raid_en.get()) + "\n")
    file1.write("friend_raid = " +str(friend_raid_en.get()) + "\n")
    file1.write("water_raid = " +str(water_raid_cb.get()) + "\n")
    file1.write("sp_raid = " +str(sp_raid_cb.get()) + "\n")
    file1.write("gap_resurrect_raid = " +str(gap_resurrect_raid_en.get()) + "\n")
    
    # pvp
    file1.write("hour_start_pvp = " + str(hour_start_pvp_en.get()) + "\n")
    file1.write("min_start_pvp = " + str(min_start_pvp_en.get()) + "\n")
    file1.write("hour_end_pvp = " + str(hour_end_pvp_en.get()) + "\n")
    file1.write("min_end_pvp = " + str(min_end_pvp_en.get()) + "\n")
    file1.write("untilreward = " + str(untilreward_cb.get()) + "\n")
    file1.write("equip_pvp = " +str(equip_pvp_en.get()) + "\n")
    file1.write("statue_pvp = " +str(statue_pvp_en.get()) + "\n")
    file1.write("friend_pvp = " +str(friend_pvp_en.get()) + "\n")
    file1.write("sp_pvp = " +str(sp_pvp_cb.get()) + "\n")
    file1.write("ep_pvp = " +str(ep_pvp_cb.get()) + "\n")

    # debuff
    file1.write("key_debuffskill = " +str(key_debuffskill_en.get()) + "\n")
    file1.write("page_debuffskill = " +str(page_debuffskill_en.get()) + "\n")

    file1.close()

    
def run_script():
    save_parameters()
    os.system('script.py')    
### 啟動按鈕
start_btn = tk.Button(text='啟動腳本', command = run_script, bg='#29DAD6')
start_btn.place(x = 290-140, y = f_yy+f_hh, width=280, height=50)

# 常駐主視窗
win.mainloop()
