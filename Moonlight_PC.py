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
import numpy as np
from numpy import frombuffer, uint8
import cv2
import win32gui, win32con, win32ui, win32api
import imutils
# import matplotlib.pyplot as plt
from PIL import Image
from pywinauto import Application

win = tk.Tk()
# 標題
win.title("月光雕刻施輔助腳本")
rr, cc=0, 0
# 大小, 顏色, 透明度, 置頂
win.geometry("600x635+100+100")
#win.minsize(width=400, heigh=200)
#win.maxsize(width=400, heigh=200)
win.resizable(False, False)


try:
    exec(open('function_PC.py',encoding="utf-8").read())
except:
    exec(open('function_PC.py').read())
    
### default values
class setup:
    def __init__(self):
        try:
            exec(open('setup.py',encoding="utf-8").read())
        except:
            exec(open('setup.py').read())
self = setup()

f_xx, f_yy = 10, 10
### 基本資訊
f_ww, f_hh = 580, 90
Basic_lf = tk.LabelFrame(text="遊戲視窗設定", height=10)
Basic_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)

xx, yy = 10, 10
len1, len2 = 4, 12 # text length, value length
lb = tk.Label(Basic_lf, text='視窗標題')
lb.place(x=xx, y=yy)
xx = xx + 14*len1
character_id_en = tk.Entry(Basic_lf)
character_id_en.insert(0, self.character_id) # default value
character_id_en.place(x=xx, y=yy, width = max(20, 10*len2) )
xx = xx + max(20, 10*len2)

len1, len2 = 6, 1 # text length, value length
lb = tk.Label(Basic_lf, text='復活次數上限')
lb.place(x=xx, y=yy)
xx += 14*len1
num_resurrect_en = tk.Entry(Basic_lf)
num_resurrect_en.insert(0, self.num_resurrect)
num_resurrect_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 6, 3 # text length, value length
lb = tk.Label(Basic_lf, text='復活間隔(秒)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_resurrect_en = tk.Entry(Basic_lf)
gap_resurrect_en.insert(0, self.gap_resurrect)
gap_resurrect_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


xx = xx + 30
xx_temp1 = xx
len1, len2 = 8, 1 # text length, value length
team_accept_cb = BooleanVar()
team_accept_chk = tk.Checkbutton(Basic_lf, text='自動確認加入隊伍', variable=team_accept_cb, onvalue=True, offvalue=False)
if self.team_accept:
    team_accept_chk.select()
team_accept_chk.place(x=xx+5, y=yy-2)
xx += 14*len1


xx, yy = 10, yy+30
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Basic_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_basic_en = tk.Entry(Basic_lf)
equip_basic_en.insert(0, self.equip_basic)
equip_basic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Basic_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_basic_en = tk.Entry(Basic_lf)
statue_basic_en.insert(0, self.statue_basic)
statue_basic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Basic_lf, text='夥伴編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_basic_en = tk.Entry(Basic_lf)
friend_basic_en.insert(0, self.friend_basic)
friend_basic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

yy = yy - 3
len1, len2 = 6.5, 1 # text length, value length
water_basic_cb = BooleanVar()
water_basic_chk = tk.Checkbutton(Basic_lf, text='30% HP藥水', variable= water_basic_cb, onvalue=True, offvalue=False)
if self.water_basic:
    water_basic_chk.select()
water_basic_chk.place(x=xx, y=yy)
xx += 14*len1

yy = yy + 2
len1, len2 = 5.5, 3 # text length, value length
lb = tk.Label(Basic_lf, text='省電模式(秒)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_economic_en = tk.Entry(Basic_lf)
gap_economic_en.insert(0, self.gap_economic)
gap_economic_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx = xx_temp1
len1, len2 = 8, 1 # text length, value length
team_add_cb = BooleanVar()
team_add_chk = tk.Checkbutton(Basic_lf, text='自動邀請密語人', variable=team_add_cb, onvalue=True, offvalue=False)
if self.team_add:
    team_add_chk.select()
team_add_chk.place(x=xx+5, y=yy)
xx += 14*len1

f_xx, f_yy = 10, f_yy+f_hh
xx, yy = 10, 10
### 交易所: 間隔
f_ww, f_hh = 170, 60
Auction_lf = tk.LabelFrame(text="交易所自動買")
Auction_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_auction_cb = BooleanVar()
enable_auction_chk = tk.Checkbutton(text='開啟功能', variable= enable_auction_cb, onvalue=True, offvalue=False)
if self.enable_auction:
    enable_auction_chk.select()
enable_auction_chk.place(x=f_xx + 14*6, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy


xx, yy = 10, 10
len1, len2 = 7.5, 2 # text length, value length
lb = tk.Label(Auction_lf, text='交易所間隔(分鐘)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_auction_en = tk.Entry(Auction_lf)
gap_auction_en.insert(0, self.gap_auction)
gap_auction_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


### 每日副本: 小時, 分鐘
f_ww, f_hh = 205, 60
Daily_lf = tk.LabelFrame(text="每日副本設定")
Daily_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_daily_cb = BooleanVar()
enable_daily_chk = tk.Checkbutton(text='開啟功能', variable= enable_daily_cb, onvalue=True, offvalue=False)
if self.enable_daily:
    enable_daily_chk.select()
enable_daily_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy

xx, yy = 10, 10
len1, len2 = 4, 1.8 # text length, value length
lb = tk.Label(Daily_lf, text='進場時間:')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_daily_en = tk.Entry(Daily_lf)
hour_daily_en.insert(0, self.hour_daily)
hour_daily_en.place(x=xx, y=yy, width = max(10, 10*len2))
xx += max(10, 10*len2)

len1, len2 = 0.5, 1.8 # text length, value length
lb = tk.Label(Daily_lf, text=':')
lb.place(x=xx, y=yy)
xx += 14*len1
min_daily_en = tk.Entry(Daily_lf)
min_daily_en.insert(0, self.min_daily)
min_daily_en.place(x=xx, y=yy, width = max(10, 10*len2))
xx += max(10, 10*len2)

## 活動
f_ww, f_hh = f_ww, 30
Reward_lf = tk.LabelFrame(text="每日活動設定")
Reward_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_reward_cb = BooleanVar()
enable_reward_chk = tk.Checkbutton(text='開啟功能', variable= enable_reward_cb, onvalue=True, offvalue=False)
if self.enable_reward:
    enable_reward_chk.select()
enable_reward_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx ,f_yy+30

## 金幣商店
f_ww, f_hh = f_ww,30
Coinstore_lf = tk.LabelFrame(text="金幣商店設定")
Coinstore_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_coinstore_cb = BooleanVar()
enable_coinstore_chk = tk.Checkbutton(text='開啟功能', variable= enable_coinstore_cb, onvalue=True, offvalue=False)
if self.enable_coinstore:
    enable_coinstore_chk.select()
enable_coinstore_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

### 公會狩獵設定: 小時, 分鐘, 位置, 離開模式
f_xx = 10
f_ww, f_hh = 580, 100
Guild_lf = tk.LabelFrame(text="公會狩獵設定")
Guild_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_hunt_cb = BooleanVar()
enable_hunt_chk = tk.Checkbutton(text='開啟功能', variable= enable_hunt_cb, onvalue=True, offvalue=False)
if self.enable_hunt:
    enable_hunt_chk.select()
enable_hunt_chk.place(x=f_xx + 14*6, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(Guild_lf, text='進場時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_guild_en = tk.Entry(Guild_lf)
hour_guild_en.insert(0, self.hour_guild)
hour_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(Guild_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_guild_en = tk.Entry(Guild_lf)
min_guild_en.insert(0, self.min_guild)
min_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx += 10
len1, len2 = 6, 5 # text length, value length
lb = tk.Label(Guild_lf, text='狩獵位置: X軸')
lb.place(x=xx, y=yy)
xx += 14*len1
x_guild_en = tk.Entry(Guild_lf)
x_guild_en.insert(0, self.x_guild)
x_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 5 # text length, value length
lb = tk.Label(Guild_lf, text='Y軸')
lb.place(x=xx, y=yy)
xx += 14*len1
y_guild_en = tk.Entry(Guild_lf)
y_guild_en.insert(0, self.y_guild)
y_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx, yy = 10, yy+30
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Guild_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_guild_en = tk.Entry(Guild_lf)
equip_guild_en.insert(0, self.equip_guild)
equip_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Guild_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_guild_en = tk.Entry(Guild_lf)
statue_guild_en.insert(0, self.statue_guild)
statue_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Guild_lf, text='夥伴編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_guild_en = tk.Entry(Guild_lf)
friend_guild_en.insert(0, self.friend_guild)
friend_guild_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 8, 1 # text length, value length
leave_guild_cb = BooleanVar()
leave_guild_chk = tk.Checkbutton(Guild_lf, text='自動離開公會', variable=leave_guild_cb, onvalue=True, offvalue=False)
if self.leave_guild:
    leave_guild_chk.select()
leave_guild_chk.place(x=xx, y=yy)
xx += 14*len1



### 突襲副本: 提前進場秒數, 3:00-24:00 (8 checkboxes)
### 預計新增: 裝備雕像
f_xx = 10
f_ww, f_hh = 580, 120
Raid_lf = tk.LabelFrame(text="突襲設定")
Raid_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_raid_cb = BooleanVar()
enable_raid_chk = tk.Checkbutton(text='開啟功能', variable= enable_raid_cb, onvalue=True, offvalue=False)
if self.enable_raid:
    enable_raid_chk.select()
enable_raid_chk.place(x=f_xx + 14*4, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(Raid_lf, text='提前進場分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
early_raid_en = tk.Entry(Raid_lf)
early_raid_en.insert(0, self.early_raid)
early_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 3 # text length, value length
lb = tk.Label(Raid_lf, text='關卡等級')
lb.place(x=xx, y=yy)
xx += 14*len1
level_raid_en = tk.Entry(Raid_lf)
level_raid_en.insert(0, self.level_raid)
level_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 6, 3 # text length, value length
lb = tk.Label(Raid_lf, text='復活間隔(秒)')
lb.place(x=xx, y=yy)
xx += 14*len1
gap_resurrect_raid_en = tk.Entry(Raid_lf)
gap_resurrect_raid_en.insert(0, self.gap_resurrect_raid)
gap_resurrect_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

yy = yy-2
len1, len2 = 5, 1 # text length, value length
ticket_raid_cb = BooleanVar()
ticket_raid_chk = tk.Checkbutton(Raid_lf, text='使用入場券', variable=ticket_raid_cb, onvalue=True, offvalue=False)
if self.ticket_raid:
    ticket_raid_chk.select()
ticket_raid_chk.place(x=xx, y=yy)
xx += 14*len1

xx, yy = 10, yy+30 # 換行
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Raid_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_raid_en = tk.Entry(Raid_lf)
equip_raid_en.insert(0, self.equip_raid)
equip_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Raid_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_raid_en = tk.Entry(Raid_lf)
statue_raid_en.insert(0, self.statue_raid)
statue_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(Raid_lf, text='夥伴編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_raid_en = tk.Entry(Raid_lf)
friend_raid_en.insert(0, self.friend_raid)
friend_raid_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx = xx + 5
yy = yy - 3
len1, len2 = 9, 1 # text length, value length
sp_raid_cb = BooleanVar()
sp_raid_chk = tk.Checkbutton(Raid_lf, text='30% 狂暴藥劑', variable= sp_raid_cb, onvalue=True, offvalue=False)
if self.sp_raid:
    sp_raid_chk.select()
sp_raid_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
water_raid_cb = BooleanVar()
water_raid_chk = tk.Checkbutton(Raid_lf, text='30% HP藥水', variable= water_raid_cb, onvalue=True, offvalue=False)
if self.water_raid:
    water_raid_chk.select()
water_raid_chk.place(x=xx, y=yy)
xx += 14*len1

xx, yy = 10, yy+30 # 換行
len1, len2 = 3, 0 # text length, value length
lb = tk.Label(Raid_lf, text='場次: ')
lb.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid1_cb = BooleanVar()
raid1_chk = tk.Checkbutton(Raid_lf, text='03:00', variable=raid1_cb, onvalue=True, offvalue=False)
if self.raid1:
    raid1_chk.select()
raid1_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid2_cb = BooleanVar()
raid2_chk = tk.Checkbutton(Raid_lf, text='6:00', variable= raid2_cb, onvalue=True, offvalue=False)
if self.raid2:
    raid2_chk.select()
raid2_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid3_cb = BooleanVar()
raid3_chk = tk.Checkbutton(Raid_lf, text='9:00', variable= raid3_cb, onvalue=True, offvalue=False)
if self.raid3:
    raid3_chk.select()
raid3_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid4_cb = BooleanVar()
raid4_chk = tk.Checkbutton(Raid_lf, text='12:00', variable= raid4_cb, onvalue=True, offvalue=False)
if self.raid4:
    raid4_chk.select()
raid4_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid5_cb = BooleanVar()
raid5_chk = tk.Checkbutton(Raid_lf, text='15:00', variable= raid5_cb, onvalue=True, offvalue=False)
if self.raid5:
    raid5_chk.select()
raid5_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid6_cb = BooleanVar()
raid6_chk = tk.Checkbutton(Raid_lf, text='18:00', variable= raid6_cb, onvalue=True, offvalue=False)
if self.raid6:
    raid6_chk.select()
raid6_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid7_cb = BooleanVar()
raid7_chk = tk.Checkbutton(Raid_lf, text='21:00', variable= raid7_cb, onvalue=True, offvalue=False)
if self.raid7:
    raid7_chk.select()
raid7_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 4, 1 # text length, value length
raid8_cb = BooleanVar()
raid8_chk = tk.Checkbutton(Raid_lf, text='24:00', variable= raid8_cb, onvalue=True, offvalue=False)
if self.raid8:
    raid8_chk.select()
raid8_chk.place(x=xx, y=yy)
xx += 14*len1


### 決鬥場: 開始, 結束, 是否只打到獎勵
### 預計新增: 裝備雕像
f_xx = 10
f_ww, f_hh = 580, 90
PVP_lf = tk.LabelFrame(text="決鬥場設定")
PVP_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
enable_pvp_cb = BooleanVar()
enable_pvp_chk = tk.Checkbutton(text='開啟功能', variable= enable_pvp_cb, onvalue=True, offvalue=False)
if self.enable_pvp:
    enable_pvp_chk.select()
enable_pvp_chk.place(x=f_xx + 14*5, y=f_yy-4)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh

xx, yy = 10, 10
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(PVP_lf, text='開始時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_start_pvp_en = tk.Entry(PVP_lf)
hour_start_pvp_en.insert(0, self.hour_start_pvp)
hour_start_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(PVP_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_start_pvp_en = tk.Entry(PVP_lf)
min_start_pvp_en.insert(0, self.min_start_pvp)
min_start_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx = xx + 30
len1, len2 = 6, 2 # text length, value length
lb = tk.Label(PVP_lf, text='結束時間: 小時')
lb.place(x=xx, y=yy)
xx += 14*len1
hour_end_pvp_en = tk.Entry(PVP_lf)
hour_end_pvp_en.insert(0, self.hour_end_pvp)
hour_end_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 2, 2 # text length, value length
lb = tk.Label(PVP_lf, text='分鐘')
lb.place(x=xx, y=yy)
xx += 14*len1
min_end_pvp_en = tk.Entry(PVP_lf)
min_end_pvp_en.insert(0, self.min_end_pvp)
min_end_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx += 20
xx_temp=xx
len1, len2 = 8, 1 # text length, value length
until_reward_cb = BooleanVar()
until_reward_chk = tk.Checkbutton(PVP_lf, text='拿到獎場就停止', variable=until_reward_cb, onvalue=True, offvalue=False)
if self.until_reward:
  until_reward_chk.select()
until_reward_chk.place(x=xx, y=yy)
xx += 14*len1

xx, yy = 10, yy+30 # 換行
len1, len2 = 4, 1 # text length, value length
lb = tk.Label(PVP_lf, text='裝備編號')
lb.place(x=xx, y=yy)
xx += 14*len1
equip_pvp_en = tk.Entry(PVP_lf)
equip_pvp_en.insert(0, self.equip_pvp)
equip_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

len1, len2 = 4, 1 # text length, value length
lb = tk.Label(PVP_lf, text='雕像編號')
lb.place(x=xx, y=yy)
xx += 14*len1
statue_pvp_en = tk.Entry(PVP_lf)
statue_pvp_en.insert(0, self.statue_pvp)
statue_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)


len1, len2 = 4, 1 # text length, value length
lb = tk.Label(PVP_lf, text='夥伴編號')
lb.place(x=xx, y=yy)
xx += 14*len1
friend_pvp_en = tk.Entry(PVP_lf)
friend_pvp_en.insert(0, self.friend_pvp)
friend_pvp_en.place(x=xx, y=yy, width = max(20, 10*len2))
xx += max(20, 10*len2)

xx = xx + 5
yy = yy - 3
len1, len2 = 9, 1 # text length, value length
sp_pvp_cb = BooleanVar()
sp_pvp_chk = tk.Checkbutton(PVP_lf, text='30% 狂暴藥劑', variable= sp_pvp_cb, onvalue=True, offvalue=False)
if self.sp_pvp:
    sp_pvp_chk.select()
sp_pvp_chk.place(x=xx, y=yy)
xx += 14*len1

len1, len2 = 9, 1 # text length, value length
xx = xx_temp
ep_pvp_cb = BooleanVar()
ep_pvp_chk = tk.Checkbutton(PVP_lf, text='愛娜的祝福', variable= ep_pvp_cb, onvalue=True, offvalue=False)
if self.ep_pvp:
    ep_pvp_chk.select()
ep_pvp_chk.place(x=xx, y=yy)
xx += 14*len1


f_ww, f_hh = 580, 50
f_xx = 10
Auction2_lf = tk.LabelFrame(text="交易所物品")
Auction2_lf.place(x=f_xx, y=f_yy, width=f_ww, height=f_hh)
xx, yy = 10, 10
len1, len2 = 7, 200 # text length, value length
lb = tk.Label(Auction2_lf, text='物品(逗號分隔)')
lb.place(x=xx, y=yy)
xx = xx + 14*len1
auction_item_en = tk.Entry(Auction2_lf)
auction_item_en.insert(0, self.auction_item) # default value
auction_item_en.place(x=xx, y=yy, width = max(20, 10*len2) )
xx = xx + max(20, 10*len2)
f_xx ,f_yy = f_xx+f_ww ,f_yy+f_hh


def run_script():
    get_setup(self)
    save_setup(self)
    os.system('script.py')    
### 啟動按鈕
start_btn = tk.Button(text='啟動腳本', command = run_script, bg='#29DAD6')
start_btn.place(x = 300-140, y = f_yy+10, width=280, height=50)

# 常駐主視窗
win.mainloop()
