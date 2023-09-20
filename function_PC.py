# import matplotlib.pyplot as plt
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
import win32com.client
import imutils
from PIL import Image
from pywinauto import Application
import pywinauto

delay = 1 # 滑鼠點擊間隔
keywait = 0.3 # 滑鼠點擊後等待判斷時間
checkusing = 1 # 遊玩時暫停腳本
exe = 0 # 0: 正常執行腳本, -1: 關閉全功能, 1: 測試全功能

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def ImgSearch(icon, img, threshold=0.8, x_scale = 1, y_scale = 1, pos=0, show=0, value=0):
    # pos: return image position
    # show: plot the given region +margin = show
    # value: print the maximum res
    if x_scale!=1:
        icon = imutils.resize(icon, width = int(icon.shape[1] * x_scale), height = int(icon.shape[0] * y_scale))
    res = cv2.matchTemplate(img, icon, cv2.TM_CCOEFF_NORMED)
    if value:
        print(np.max(res), end=' ')
    loc = np.where(res >= threshold)
    if show: # plot
        y, x = np.unravel_index(res.argmax(), res.shape)
        plt.imshow(img[y:(y+icon.shape[0]),x:(x+icon.shape[1]),])
    if pos==1: # return the maximum position
        y, x = np.unravel_index(res.argmax(), res.shape)
        return np.max(res), x+int(icon.shape[1]/2), y+int(icon.shape[0]/2)
    else:
        return sum(sum(loc))>0
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    origin = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return origin[::-1]
def rgb_to_hex(rgb):
    return '0x%02x%02x%02x' % rgb[::-1]
def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
def rgba2rgb(rgba, background=(255,255,255) ):
    row, col, ch = rgba.shape
    if ch == 3:
        return rgba
    assert ch == 4, 'RGBA image has 4 channels.'
    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]
    a = np.asarray( a, dtype='float32' ) / 255.0
    R, G, B = background
    rgb[:,:,2] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,0] = b * a + (1.0 - a) * B
    return np.asarray( rgb, dtype='uint8' )

def clock2(mode='minute', tt=5): # modula by 240 minitues
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    if mode == 'minute':
        t_now = int(now.strftime("%H"))*60 + int(now.strftime("%M"))
    elif mode =='day':
        t_now = int(now.strftime("%Y"))*1000 + int(now.strftime("%j")) - (int(now.strftime("%H"))<tt)
    return(t_now)

def get_child_windows(parent):
    '''
    Get all child window handles for parent
    Returns a list of sub-window handles
       '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList

def get_setup(self):
    # window
    self.character_id = str(character_id_en.get())
    self.num_resurrect = int(num_resurrect_en.get())
    self.gap_resurrect = int(gap_resurrect_en.get())
    self.equip_basic = int(equip_basic_en.get())
    self.statue_basic = int(statue_basic_en.get())
    self.friend_basic = int(friend_basic_en.get())
    self.water_basic = water_basic_cb.get()
    self.gap_economic= int(gap_economic_en.get())
    self.team_accept = team_accept_cb.get()    
    self.team_add = team_add_cb.get()

    # auction
    self.enable_auction = enable_auction_cb.get()
    self.gap_auction = int(gap_auction_en.get())
    self.auction_item = str(auction_item_en.get())

    # daily
    self.enable_reward = enable_reward_cb.get()
    self.enable_coinstore = enable_coinstore_cb.get()
    self.enable_daily = enable_daily_cb.get()
    self.hour_daily = int(hour_daily_en.get())
    self.min_daily = int(min_daily_en.get())
    

    # guild hunt
    self.enable_hunt = enable_hunt_cb.get()
    self.hour_guild = int(hour_guild_en.get())
    self.min_guild = int(min_guild_en.get())
    self.x_guild = float(x_guild_en.get())
    self.y_guild  = float(y_guild_en.get())
    self.equip_guild = int(equip_guild_en.get())
    self.statue_guild = int(statue_guild_en.get())
    self.friend_guild = int(friend_guild_en.get())
    self.leave_guild = bool(leave_guild_cb.get())
    
    # raid
    self.enable_raid = enable_raid_cb.get()
    self.early_raid = int(early_raid_en.get())
    self.raid1 = bool(raid1_cb.get())
    self.raid2 = bool(raid2_cb.get())
    self.raid3 = bool(raid3_cb.get())
    self.raid4 = bool(raid4_cb.get())
    self.raid5 = bool(raid5_cb.get())
    self.raid6 = bool(raid6_cb.get())
    self.raid7 = bool(raid7_cb.get())
    self.raid8 = bool(raid8_cb.get())
    self.level_raid = int(level_raid_en.get())
    self.ticket_raid  = bool(ticket_raid_cb.get())
    self.equip_raid = int(equip_raid_en.get())
    self.statue_raid = int(statue_raid_en.get())
    self.friend_raid = int(friend_raid_en.get())
    self.water_raid = water_raid_cb.get()
    self.sp_raid = sp_raid_cb.get()
    self.gap_resurrect_raid = int(gap_resurrect_raid_en.get())

    # pvp
    self.enable_pvp = enable_pvp_cb.get()
    self.hour_start_pvp = int(hour_start_pvp_en.get())
    self.min_start_pvp = int(min_start_pvp_en.get())
    self.hour_end_pvp = int(hour_end_pvp_en.get())
    self.min_end_pvp = int(min_end_pvp_en.get())
    self.until_reward  = until_reward_cb.get()
    self.equip_pvp = int(equip_pvp_en.get())
    self.statue_pvp = int(statue_pvp_en.get())
    self.friend_pvp = int(friend_pvp_en.get())
    self.sp_raid = ep_pvp_cb.get()
    self.ep_raid = ep_pvp_cb.get()
    
def save_setup(self):
    file1 = open("setup.py","w")
    file1.write('self.character_id = \'' + str(self.character_id) + '\'\n')
    file1.write('self.num_resurrect = ' + str(self.num_resurrect) + '\n')
    file1.write('self.gap_resurrect = ' + str(self.gap_resurrect) + '\n')
    file1.write('self.equip_basic = ' + str(self.equip_basic) + '\n')
    file1.write('self.statue_basic = ' + str(self.statue_basic) + '\n')
    file1.write('self.friend_basic = ' + str(self.friend_basic) + '\n')
    file1.write('self.water_basic= ' + str(self.water_basic) + '\n')
    file1.write('self.gap_economic= ' + str(self.gap_economic) + '\n')
    file1.write('self.team_accept = ' + str(self.team_accept) + '\n')
    file1.write('self.team_add = ' + str(self.team_add) + '\n')
    file1.write('\n')
    file1.write('self.enable_auction = ' + str(self.enable_auction) + '\n')
    file1.write('self.gap_auction = ' + str(self.gap_auction) + '\n')
    file1.write('self.auction_item = \'' + str(self.auction_item) + '\'\n')
    file1.write('\n')
    file1.write('self.enable_daily = ' + str(self.enable_daily) + '\n')
    file1.write('self.enable_reward = ' + str(self.enable_reward) + '\n')
    file1.write('self.enable_coinstore = ' + str(self.enable_coinstore) + '\n')
    file1.write('self.hour_daily = ' + str(self.hour_daily) + '\n')
    file1.write('self.min_daily = ' + str(self.min_daily) + '\n')
    file1.write('\n')
    file1.write('self.enable_hunt = ' + str(self.enable_hunt) + '\n')
    file1.write('self.hour_guild = ' + str(self.hour_guild) + '\n')
    file1.write('self.min_guild = ' + str(self.min_guild) + '\n')
    file1.write('self.x_guild = ' + str(self.x_guild) + '\n')
    file1.write('self.y_guild = ' + str(self.y_guild) + '\n')
    file1.write('self.equip_guild = ' + str(self.equip_guild) + '\n')
    file1.write('self.statue_guild = ' + str(self.statue_guild) + '\n')
    file1.write('self.friend_guild = ' + str(self.friend_guild) + '\n')
    file1.write('self.leave_guild = ' + str(self.leave_guild) + '\n')
    file1.write('\n')
    file1.write('self.enable_raid = ' + str(self.enable_raid) + '\n')
    file1.write('self.early_raid = ' + str(self.early_raid) + '\n')
    file1.write('self.level_raid = ' + str(self.level_raid) + '\n')
    file1.write('self.gap_resurrect_raid = ' + str(self.gap_resurrect_raid) + '\n')
    file1.write('self.ticket_raid = ' + str(self.ticket_raid) + '\n')
    file1.write('self.raid1 = ' + str(self.raid1) + '\n')
    file1.write('self.raid2 = ' + str(self.raid2) + '\n')
    file1.write('self.raid3 = ' + str(self.raid3) + '\n')
    file1.write('self.raid4 = ' + str(self.raid4) + '\n')
    file1.write('self.raid5 = ' + str(self.raid5) + '\n')
    file1.write('self.raid6 = ' + str(self.raid6) + '\n')
    file1.write('self.raid7 = ' + str(self.raid7) + '\n')
    file1.write('self.raid8 = ' + str(self.raid8) + '\n')
    file1.write('self.equip_raid = ' + str(self.equip_raid) + '\n')
    file1.write('self.statue_raid = ' + str(self.statue_raid) + '\n')
    file1.write('self.friend_raid = ' + str(self.friend_raid) + '\n')
    file1.write('self.water_raid = ' + str(self.water_raid) + '\n')
    file1.write('self.sp_raid = ' + str(self.sp_raid) + '\n')
    file1.write('\n')
    file1.write('self.enable_pvp = ' + str(self.enable_pvp) + '\n')
    file1.write('self.hour_start_pvp = ' + str(self.hour_start_pvp) + '\n')
    file1.write('self.min_start_pvp = ' + str(self.min_start_pvp) + '\n')
    file1.write('self.hour_end_pvp = ' + str(self.hour_end_pvp) + '\n')
    file1.write('self.min_end_pvp = ' + str(self.min_end_pvp) + '\n')
    file1.write('self.until_reward = ' + str(self.until_reward) + '\n')
    file1.write('self.equip_pvp = ' + str(self.equip_pvp) + '\n')
    file1.write('self.statue_pvp = ' + str(self.statue_pvp) + '\n')
    file1.write('self.friend_pvp = ' + str(self.friend_pvp) + '\n')
    file1.write('self.sp_pvp = ' + str(self.sp_pvp) + '\n')
    file1.write('self.ep_pvp = ' + str(self.ep_pvp) + '\n')
    file1.write('\n')
    file1.write('self.t_boss = ' + str(self.t_boss) + '\n')
    file1.write('self.t_auction = ' + str(self.t_auction) + '\n')
    file1.write('self.d_daily = ' + str(self.d_daily) + '\n')
    file1.write('self.d_pvp = ' + str(self.d_pvp) + '\n')
    file1.write('self.d_hunt = ' + str(self.d_hunt) + '\n')
    file1.write('self.d_reward = ' + str(self.d_reward) + '\n')
    file1.write('self.d_coinstore = ' + str(self.d_coinstore) + '\n')
    file1.close()
    
class Game_obj:
    def __init__(self, initialize=True, title=None, first_hwnd=False):
        if title:
            self.character_id = self.title=title
        else:
            try:
                exec(open('setup.py',encoding="utf-8").read())
            except:
                exec(open('setup.py').read())
        ## window setup
        if self.character_id=="Moonlight_Global":
            def windowEnumerationHandler(hwnd, top_windows):
                if  win32gui.GetWindowText(hwnd)==self.title:
                    top_windows.append(hwnd)
            hwnd_lst = []  # all open windows
            win32gui.EnumWindows(windowEnumerationHandler, hwnd_lst)
            print(hwnd_lst)
            if len(hwnd_lst)>1 and not first_hwnd:
                print('發現遊戲雙開，請點選遊戲視窗: ')
                while win32gui.GetWindowText (win32gui.GetForegroundWindow())!="Moonlight_Global":
                    pass
                self.hwnd = win32gui.GetForegroundWindow()
            else:
                self.hwnd = hwnd_lst[0]
            if initialize:
                self.win = Application().connect(handle=self.hwnd).window()
        ## Nox
        elif win32gui.GetClassName(win32gui.FindWindow(None, self.title))=='Qt5QWindowIcon':
            self.hwnd0 = win32gui.FindWindow(None, self.title)
            self.hwnd1 = get_child_windows(self.hwnd0)[3]
            self.hwnd=self.hwnd1 ##operation hwnd
        ## Moonlight_LD version
        else:
            self.hwnd0 = win32gui.FindWindow(None, self.title)
            self.hwnd1 = win32gui.FindWindowEx(self.hwnd0, None, None, None)
            self.hwnd=self.hwnd1 ##operation hwnd
        
        if self.character_id == 'Moonlight_Global':
            self.calibration = (8, 32, -9, -9) # 視窗位置校正
            self.key_left = "{A}"
            self.key_right = "{D}"
            self.key_up = "{W}"
            self.key_pet = "{V}"
            self.key_friend = "{B}"
            self.key_bag = "{I}"
            self.key_list = "{O}"
            self.key_profile = "{P}"
            self.key_switch = "{TAB}"
            self.key_back = "{ESC}"
            self.key_mall = '{U}'
            self.key_map = '{M}'
            self.key_decompose = "{-}"
            self.key_chat = "{ENTER}"
        ## Moonlight_LD version
        else:
            self.calibration = (0, 0, 0, 0) # 視窗位置校正
            self.key_left = (0.4, 0.52)
            self.key_right = (0.6, 0.52)
            self.key_up = (0.5, 0.3)
            self.key_pet = (0.026, 0.552)
            self.key_friend = (0.618, 0.481)
            self.key_bag = (0.912, 0.055)
            self.key_list = (0.97, 0.054)
            self.key_profile = (0.04,0.05)
            self.key_switch = (0.97, 0.883)
            self.key_back = 0x1B
            self.key_mall = (0.804, 0.061)
            self.key_map = (900/960, 200/540)
            self.key_decompose = (500/960, 493/540)
            self.key_chat = (0.5,0.93)
        if '釣' in self.character_id:
            self.team_accept = False
            self.t_sp = 0
        self.team_accept = False
        if self.team_accept:
            self.gap_economic = min(self.gap_economic, 60)
        self.t_sp, self.sp = 0, False
        self.t_ep, self.sp = 0, False
        self.t_economic = 0
        self.t_hardpotion = time.time()
        self.t_teamup, self.gap_teamup = 0, 600
        self.raid_start = [180,360,540,720,900,1080,1260,1440]
        self.check_boss = False
        self.mode='basic'
        self.key_openlist = key_info(key=(0.97,0.07),color_info='0x6B6152',keep=True)
        self.key_back_to_redblood = key_info(self.key_back, keep=True, color_info=color_redblood, msg='返回')

        if initialize:
            if '釣' in self.character_id:
                self.checkusing = -1
                self.home_screen()
            else:
                self.checkusing = -1
                self.home_screen()
                self.myclick(key_info(self.key_friend, keep=True, color_info=color_graycross))
                self.check_friend()
                self.myclick(self.key_back_to_redblood)                
        self.checkusing = 1
                
        
    def suit_setup(self, equip, statue, friend, water=0, sp=0, ep=0, msg=''):
        msg = msg+'裝備='+str(equip)+', 雕像='+str(statue)+', 夥伴='+str(friend)
        if water:
            msg = msg + ', 30%HP水'            
        if sp:
            msg = msg + ', 30%HP狂暴'
        if ep:
            msg = msg + ', 愛娜'
        print(msg)
    def time_reform(self, time_rest, endword='', countdown=False):
        time_add0 = [':0',':']
        output = str(time_rest//60) + time_add0[time_rest%60>=10] + str(time_rest%60)
        if countdown:
            return ' (倒數 '+ output+')'
        return output 
    def print_setup(self, t_now=None, d_now0=None, d_now5=None):
        self.screenshot()
        if self.PixelExist(color_redblood, shot=0):
            self.check_fmode(shot=0)
            self.check_equip(shot=0)
            self.check_statue(shot=0)
            self.check_ep(shot=0)
            self.check_location(shot=0)
        if not self.PixelExist(color_logout, shot=0):
            self.check_water(shot=0)
            self.check_page(shot=0); self.switch_page(1)
            
        self.check_sp()
        time_add0 = [':0',':']
        NY = ['否', '是']
        print('-----------------------基本設定-----------------------')
        print('遊戲視窗標題: '+ self.character_id )
        print('滑鼠位置:',end=''); str(self.getPosition(2))
        print('剩餘復活次數: ' + str(self.num_resurrect) + ', 間隔 = ' + str(self.gap_resurrect) +'秒')
        self.suit_setup(self.equip_basic, self.statue_basic, self.friend_basic, water=self.water_basic, msg='掛機裝備配置: ')
        switchable = True
        if t_now==None:
            t_now = clock2()
        if d_now0==None:
            d_now0 = clock2('day',tt=0)
        if d_now5==None:
            d_now5 = clock2('day',tt=5)            
        
        print('\n-----------------------狀態-------------------------')
        # 負重
        if self.check_bagfull(shot=0) and switchable:
            switchable = False
            self.mode='bagfull'
            print('背包狀態: 滿了')            
        elif self.check_weight(shot=0) and switchable:
            switchable = False
            self.mode='overweight'
            print('背包狀態: 負重')
        else:
            print('背包狀態: 正常')
        self.suit_setup(self.equip, self.statue, self.friend, water=self.water, msg='現在裝備配置: ')
        
        # teamup
        print('自動加入隊伍  : '+ NY[int(self.team_accept)])
        msg = '自動組隊密語人: '+ NY[int(self.team_add)]
        if self.team_add:
            time_rest = round(self.gap_teamup - time.time() + self.t_teamup)
            msg += self.time_reform(time_rest, countdown=True)
            if time_rest<0 and switchable:
                switchable = False
                self.mode = 'teamup' 
        print(msg)
        
        # 交易所
        msg = '自動買交易所  : '+ NY[int(self.enable_auction)]        
        if self.enable_auction:
            time_rest = round(self.gap_auction*60 - time.time() + self.t_auction)
            msg += self.time_reform(time_rest, countdown=True)
            if time_rest<=0 and switchable:
                switchable = False
                self.mode='auction'
        print(msg)

        # 每日活動獎勵
        msg = '自動領活動獎勵: '+ NY[int(self.enable_reward)]        
        if self.enable_reward:
            if self.d_reward >= d_now0:           
                msg += ' (已領取)'
            else:
                time_rest = round(5*60 - t_now)
                msg += self.time_reform(time_rest, countdown=True)
                if t_now > 5*60 and switchable:
                    switchable = False
                    self.mode='get_reward'
        print(msg)
        # 金幣商店
        msg = '自動買金幣商店: '+ NY[int(self.enable_coinstore)]
        if self.enable_coinstore:
            if self.d_coinstore>=d_now0:
                msg += ' (已購買)'
            else:
                time_rest = round(10 - t_now)
                msg += self.time_reform(time_rest, countdown=True)
                if time_rest<0 and switchable:
                    switchable = False
                    self.mode='coinstore'
        print(msg)
                    
        # 每日副本
        msg = '自動每日副本  : '+ NY[int(self.enable_daily)]
        if self.enable_daily:
            t_daily = self.hour_daily*60 + self.min_daily
            if self.d_daily>=d_now5:
                msg += " (已完成)"
            else:
                time_rest = round(t_daily- t_now)
                msg += self.time_reform(time_rest, countdown=True)
                if time_rest<0 and switchable:
                    switchable = False
                    self.mode='daily_raid'
        print(msg)

        
        print('\n-----------------------突襲功能-----------------------')  
        print( "自動進入突襲: "+ NY[int(self.enable_raid)] )        
        if self.enable_raid:
            self.suit_setup(self.equip_raid, self.statue_raid, self.friend_raid, water=self.water_raid, sp=self.sp_raid, msg='突襲裝備配置: ')                
            print('突襲等級 ' + ['(不使用入場券): ','(使用入場券): '][int(self.ticket_raid)]+str(self.level_raid)+ ', 復活間隔 = ' + str(self.gap_resurrect_raid) +'秒')
            time_rest_lst, t_raid_lst = [], []
            for i in range(0, 8):
                if getattr(self, 'raid'+str(i+1)):
                    t_raid_lst.append(self.raid_start[i]-self.early_raid)
                    time_rest_lst.append(self.raid_start[i]-t_now)
            if len(t_raid_lst)==0:
                print('突襲時間表: (請勾選)')
            else:
                print( '突襲時間表: '+str(self.time_reform(t_raid_lst.pop(0))), end='')
                if len(t_raid_lst)>0:
                    for t_raid in t_raid_lst:
                        print(', '+self.time_reform(t_raid),end='')
                time_rest = 1440
                for t in time_rest_lst:
                    if t>0 and t<time_rest:
                        time_rest = t    
                if time_rest==1440:
                    print('\n突襲已完成')
                else:
                    print('\n突襲下一場倒數: '+self.time_reform(time_rest)+ ' (提前'+str(self.early_raid)+'分鐘)')
                    if time_rest<=self.early_raid and switchable:
                        switchable = False
                        self.mode='normal_raid'

        print('\n---------------------公會狩獵功能---------------------') 
        # guild hunt
        msg = "自動進入公會狩獵: "+ NY[int(self.enable_hunt)]
        if self.enable_hunt:
            t_hunt = self.hour_guild*60+self.min_guild
            if self.d_hunt>=d_now5:
                if self.location == '公會狩獵地圖':
                    msg += ' (進行中)'
                else:
                    msg += ' (已完成)'
            else:
                time_rest = t_hunt - t_now
                if time_rest>0:
                    msg += self.time_reform(time_rest, countdown=True)
                elif time_rest<-1 and not self.ImgExist((0, 0, 0.13, 0.13, icon_guild,0.8,1400, 786)): ## 這個不能home_screen
                    msg += ' (腳本出問題，請手動進場)'
                elif switchable: # guild list is open
                    if self.location=='一般地圖':
                        switchable = False
                        self.mode='guild_hunt'
                        msg += ' (前往中)'
                    else:
                        msg += ' (請回到一般地圖)'
        if self.leave_guild and self.location=='公會基地' and switchable:
            switchable = False
            self.mode='leave_guild'
        print(msg)
        self.suit_setup(self.equip_guild, self.statue_guild, self.friend_guild, msg='狩獵裝備配置: ')
        print('\n----------------------決鬥場設定----------------------')
        tz = pytz.timezone('Asia/Taipei')
        msg = "自動打決鬥場: "+ NY[int(self.enable_pvp)]
        if self.enable_pvp:
            hl, ml = self.hour_start_pvp, self.min_start_pvp
            hu, mu = self.hour_end_pvp, self.min_end_pvp                
            if datetime.now(tz).isoweekday()==7:
                msg += ' (星期天不開放)'
            else:
                t_pvp_lower, t_pvp_upper = hl*60+ml, hu*60+mu
                if self.d_pvp>=d_now5:
                    msg += ' (已領取獎勵)'
                elif t_pvp_lower<t_now and t_now<t_pvp_upper and switchable:
                    switchable = False
                    self.mode='pvp'
                    msg += ' (進行中)'
                else:
                    msg += ' (時間未到)'                    
        print(msg)
        if self.enable_pvp:
            self.suit_setup(self.equip_pvp, self.statue_pvp, self.friend_pvp, ep=self.ep_pvp, sp=self.sp_pvp, msg='決鬥場裝備配置: ')
            print('決鬥場時間: ' + str(hl) + time_add0[int(ml>=10)] +str(ml) + ' 至 ' + str(hu) + time_add0[int(mu>=10)] +str(mu))
            print('領到獎勵就結束: '+NY[int(self.until_reward)])


        print('\n----------------------省電模式功能--------------------')
        msg = "自動進入省電模式: "+ NY[int(self.gap_economic>30)]
        if self.gap_economic>30:
            time_rest = self.gap_economic - round(time.time()-self.t_economic)
            if not switchable:
                msg += ' (解除中)' # some time check
            elif time_rest>0:
                msg += self.time_reform(time_rest, countdown=True) + str('解除')
                switchable = False
                self.mode='economic'
            elif self.check_home_screen():
                msg += ' 進入省電模' # enter economic
                switchable = False
                self.mode='economic'
            elif self.check_economic():
                msg += ' 省電模式超時' + str(-time_rest)+'秒' # leave economic
                switchable = False
                self.mode = None
        elif switchable: # do not go to economic
            self.mode = None
        print(msg)
        print('目前地圖: '+self.location)
        print(self.mode)

    ############
    ### Eyes ###
    ############
    def getWindowRect(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
        c1, c2, c3, c4 = self.calibration
        x1, y1, x2, y2 = x1+c1, y1+c2, x2+c3, y2+c4
        w, h = x2 - x1, y2 - y1            
        return x1, y1, w, h
    # screenshot: delay=0.01 to prevent cpu overload
    def screenshot(self, delay=0.01):
        try:
            if self.title == 'Moonlight_Global':
                while win32gui.IsIconic(self.hwnd):
                    win32gui.ShowWindow(self.hwnd, 4)
                hwndDC = win32gui.GetWindowDC(self.hwnd)
                mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                saveBitMap = win32ui.CreateBitmap()
                _, _, w, h = self.getWindowRect()            
                saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
                saveDC.SelectObject(saveBitMap)
                # Change the line below depending on whether you want the whole window or just the client area.
                if sys.getwindowsversion()[0]>7:
                    result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 3)
                else:
                    result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 1)
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)

                img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwndDC)
                self.img = np.asarray(img)
            else:
                while win32gui.IsIconic(self.hwnd):
                    win32gui.ShowWindow(self.hwnd, 4)
                hwindc = win32gui.GetWindowDC(self.hwnd)
                srcdc = win32ui.CreateDCFromHandle(hwindc)
                memdc = srcdc.CreateCompatibleDC()
                bmp = win32ui.CreateBitmap()
                _, _, w, h = self.getWindowRect()
                bmp.CreateCompatibleBitmap(srcdc, w, h)
                memdc.SelectObject(bmp)
                memdc.BitBlt((0 , 0), (w, h), srcdc, (0, 0), win32con.SRCCOPY)
                signedIntsArray = bmp.GetBitmapBits(True)
                img = frombuffer(signedIntsArray, uint8)
                img.shape = (h, w, 4)
                srcdc.DeleteDC()
                memdc.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwindc)
                win32gui.DeleteObject(bmp.GetHandle())
                img = rgba2rgb(img)
                self.img = img
            return self.img
        except Exception as e:
            print('Error: winkey-screenshot')
            print(e)
            time.sleep(delay)
    def save_img(self, filename='img.png', shot=False, plot=True):
        if shot:
            self.screenshot()
        if plot:
            plt.imshow(self.img)
        cv2.imwrite(filename, self.img)
            
    def PixelExist(self, color_info, tf=None, timemax=0, least=0.1, pos=0, show=-1, img=None, shot=1):
        # check whether a given pixel exists in a given region/point within timemax seconds
        
        # color_info = x_lefttop, y_lefttop, x_rightbottom, y_right_bottom, color, tolerance, T/F
        # pos: 1 give positions, 0 give T/F
        # show: expand plot margin
        # img: None screenshot
        try:
            if type(img)!=type(None): # if input img, current img = input img
                self.img = img
                shot=0
            if shot: # if not shot, use current img
                self.screenshot()
            else:
                timemax=0                
            color_info = list(color_info)
            if type(color_info[2])==str: # only include a point
                color_info[0]-=0.006
                color_info[1]-=0.01
                color_info.insert(2, color_info[0]+0.006*2)
                color_info.insert(3, color_info[1]+0.01*2)
            if type(color_info[-1])!=bool: # no given default tf in color_info
                if type(tf)!=bool:            
                    color_info.append(True)
                else:
                    color_info.append(tf)
            if type(color_info[5])!=int:  # default tolerance
                color_info.insert(5,5)
            c_x1, c_y1, c_x2, c_y2, pixel, tol, tf = color_info

            _, _, w, h, = self.getWindowRect()
            rgb = hex_to_rgb('#'+pixel[2:8])
            
            t_start = t_least = time.time() # t_least is the last time not success
            output = False
            timemax = max(timemax, least)
            while True:
                img_sub = self.img[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),]
                tf_pixel = (np.max(abs(img_sub-rgb),axis=2)<tol+5).any()
                if tf_pixel != tf:
                    t_least = time.time()
                elif time.time()-t_least>=least:
                    output = True
                    break                
                if time.time()-t_start>=timemax:
                    break
                if shot==0:
                    output = (tf_pixel == tf)
                    break;
                self.screenshot()
            if show>=0:
                img_show = self.img[(int(c_y1*h)-show):(int(c_y2*h)+show), (int(c_x1*w)-show):(int(c_x2*w)+show),]
                plt.imshow(img_show)
            if pos:
                posi = np.where((np.max(abs(img_sub-rgb),axis=2)<tol+5))
                return (c_x1+posi[1][0]/w, c_y1+posi[0][0]/h)
            else:
                return output
            
        except Exception as e:
            print(e)
            print('Error: winkey-PixelExist')
    def ImgExist(self, icon_info, tf=None, timemax=0, least=0.1, pos=0, show=-1, img=None, value=0, shot=1, gray=0):
        # check whether a given icon exists in a given region within timemax seconds
        # pos: return image position
        # show: plot the given region +margin = show
        # value: print the maximum res
        try:
            if type(img)!=type(None): # if input img, current img = input img
                self.img = img
                shot=0
            if shot: # if not shot, use current img
                self.screenshot()
            else:
                timemax=0
            
            icon_info = list(icon_info)
            if type(icon_info[-1])!=bool: # no given default tf in pic_info
                if type(tf)!=bool:
                    icon_info.append(True)
                else:
                    icon_info.append(tf)
            c_x1, c_y1, c_x2, c_y2, icon, thresh, x_icon, y_icon, tf = icon_info
            
            _, _, w, h, = self.getWindowRect()
            if gray:
                icon = cv2.cvtColor(icon,cv2.COLOR_BGR2GRAY)                
            t_start = t_least = time.time() # t_least is the last time not success
            timemax = max(timemax, least)
            output = False
            while True:
                sub_img = self.img[int(c_y1*h):int(c_y2*h), int(c_x1*w):int(c_x2*w),]
                if gray:
                    sub_img = cv2.cvtColor(sub_img,cv2.COLOR_BGR2GRAY)
                val, xx, yy = ImgSearch(icon, sub_img, threshold=thresh, x_scale = w/x_icon, y_scale = h/y_icon, pos=1, value=value)
                if ((val>thresh and tf!=True) or (val<thresh and tf!=False)):                    
                    t_least = time.time()
                elif time.time()-t_least>least:
                    output = True
                    break
                if time.time()-t_start>=timemax:
                    break
                if shot==0:
                    output = ((val>thresh and tf==True) or (val<thresh and tf==False))
                    break;
                self.screenshot()
            if pos:
                output = (val, c_x1+xx/w, c_y1+yy/h)            
            if show>=0: # show region
                plt.imshow(sub_img)
            return output
        except Exception as e:
            print(e)
            print('Error: winkey-ImgExist')
    def BestImgExist(self, icon_info_seq, thresh=0.7, shot=1, pos=0, gray=False):
        # return which icon is the best match
        if shot:
            self.screenshot()
        val_seq = [thresh]
        for icon_info in icon_info_seq:
            val_seq.append(self.ImgExist(icon_info, img=self.img, pos=1, gray=gray)[0])
        if pos:
            print(val_seq)
        return(np.argmax(val_seq))

            
    #############
    ### Hands ###
    #############
    def checkerror(self):
        if self.is_WinActive(): # if playing
            if self.checkusing == -1: # checusing=-1, never stop script. For example, in raid
                print('不停止腳本')
                return
            elif self.checkusing==0: # checkusing=0, pasue script. The script will keep runing after window is not active
                while self.is_WinActive():
                    print('暫停腳本')
                    time.sleep(3)
                return
            elif self.checkusing==1: # checkusing=1, rerun the script untill idle>60 seconds
                time_idle = getIdleTime()
                if time_idle<60:
                    raise ValueError('使用遊戲中, 閒置累積 '+str(int(time_idle))+' 秒')                    
                else:
                    print('閒置超過一分鐘，繼續腳本')                    
                    def windowEnumerationHandler(hwnd, top_windows):
                        if  'python.exe' in win32gui.GetWindowText(hwnd):
                            top_windows.append(hwnd)
                    lst = []  # all open windows
                    win32gui.EnumWindows(windowEnumerationHandler, lst)
                    win32gui.SetForegroundWindow(lst[0])
                    
        _, _, w, h = self.getWindowRect()
        if w>0.9*win32api.GetSystemMetrics(0) or h>0.9*win32api.GetSystemMetrics(1): # manually pause script
            raise ValueError('手動暫停中')
        if self.check_pause(shot=0) and self.checkusing==1:
            raise ValueError('手動暫停中')
        if self.ImgExist((0.226, 0.101, 0.855, 0.765, login_conflict, 0.95, 1400, 786), shot=0): # if someone login
            login_anyway = False
            if login_anyway:
                self.myclick((0.501, 0.597))
            else:
                raise ValueError('在其他設備上登錄')
                    
    def send(self, key, delay=1, msg=''):
        self.checkerror()
        try:
            if len(msg)>0:
                print(msg)
            if self.title == 'Moonlight_Global':
                self.win.send_keystrokes(key)                
                t_click = time.time()
                time.sleep(delay)
            else:
                win32api.PostMessage(self.hwnd, win32con.WM_ACTIVATE, 0, 0)
                win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, win32api.MapVirtualKey(key, 0) << 16)
                time.sleep(0.05)
                win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, win32api.MapVirtualKey(key, 0) << 16)        
                t_click = time.time()
                time.sleep(delay)                
            return(t_click)
        except Exception as e:
            print(e)
            print('Error: winkey-send')            
    def send_char(self, char, delay=1):
        self.win.send_chars(char)
    def click(self, key, delay=1, msg='', press=0.01, pressmax=1, color_info=None, least=0.01, key2=None, press2=0, timemax=10):
        # press: Lbuttondown duration
        # color_info: Lbuttonup duration
        # press2: duration after drag to key2
        self.checkerror()
        try:
            if len(msg)>0:
                print(msg)
            if key==(0,0):
                return(time.time())
            _, _, w, h = self.getWindowRect()
            x, y = int(key[0]*w), int(key[1]*h)

            if self.title =='Moonlight_Global':
                old_pos = win32gui.GetCursorPos()
                while abs(win32api.GetKeyState(0x11))>1 or abs(win32api.GetKeyState(0x10))>1:
                    pass            
                ok = windll.user32.BlockInput(True) #block input
                win32api.SetCursorPos(win32gui.ClientToScreen(self.hwnd, (x,y)))    
                win32gui.SendMessage(self.hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                if key2==None:
                    if color_info==None:
                        time.sleep(press)
                    else:
                        t_least = t_start = time.time()
                        while not self.PixelExist(color_info) or time.time()-t_least<least:
                            if not self.PixelExist(color_info):
                                t_lease = time.time()
                            if time.time()-t_start>pressmax:
                                break
                            
                elif key2!=None: # drag
                    x2, y2 = key2[0]*w, key2[1]*h
                    seg = 10
                    move = (x2-x)/seg, (y2-y)/seg
                    for i in range(0,seg):
                        x, y = x+move[0], y+move[1]
                        win32api.SetCursorPos(win32gui.ClientToScreen(self.hwnd, (int(x),int(y))))    
                        time.sleep(press)
                    time.sleep(press2)

                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
                time.sleep(0.01)    
                win32api.SetCursorPos(old_pos)
                ok = windll.user32.BlockInput(False) #enable input
                
            else:
                cx, cy = win32gui.GetCursorPos()
                win32api.SetCursorPos(win32gui.ClientToScreen(self.hwnd, (x,y)))    
                lParam = win32api.MAKELONG(x, y)
                win32api.SendMessage(self.hwnd, win32con.WM_ACTIVATE, 2)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                if key2==None:
                    if color_info==None:
                        time.sleep(press)
                    else:
                        t_least = t_start = time.time()
                        while not self.PixelExist(color_info) or time.time()-t_least<least:
                            if not self.PixelExist(color_info):
                                t_lease = time.time()
                            if time.time()-t_start>pressmax:
                                break
                            
                elif key2!=None: # drag
                    x2, y2 = int(key2[0]*w), int(key2[1]*h)
                    seg = 10
                    move = (x2-x)/seg, (y2-y)/seg
                    for i in range(0,seg):
                        x, y = int(x+move[0]), int(y+move[1])
                        lParam = win32api.MAKELONG(x, y)
                        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lParam);
                        time.sleep(press)
                    time.sleep(press2)
                win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, None, lParam)
                win32api.SetCursorPos((cx, cy))
            t_click = time.time()
            time.sleep(delay)
            return(t_click)
        except Exception as e:
            print(e)
            ok = windll.user32.BlockInput(False) #enable input
            print('Error: winkey-click')        
        return
    def myclick(self, key_info_seq, delay=1, keywait=0.3, least=0.3, msg='', mode=0, color_info=None, timemax=10, raise_error=True):
        # key_info_seq: (key, keywait, pic_info=None, least=None, keep=False, msg=''): key and print msg -> wait ketwait seconds -> check pixel/icon least
        # if key is string, used send method; else, use click
        # keep = True: keep clicking until color_info; Otherwise, click once
        # no color_info: just click
        # possibly use *arg and **kwarg to generalize this function to 1. 'do_func once/n_times', 2. 'until condition_func appear/disappear' 3. with timemax
        if type(key_info_seq)==tuple or type(key_info_seq)==str: ## old version
            key_info_seq=key_info(key=key_info_seq, delay=delay, keywait=keywait,timemax1=timemax,msg=msg,
                                  color_info=color_info, least=least, mode=mode)
        if type(key_info_seq)==key_info:
            key_info_seq=[key_info_seq]
        for e in key_info_seq:
            key, delay, keywait, keep, timemax1, dofirst, msg = e.key, e.delay, e.keywait, e.keep, e.timemax1, e.dofirst, e.msg
            icon_info, color_info, least, tf, timemax2 = e.icon_info, e.color_info, e.least, e.tf, e.timemax2
            # select click type
            if type(key)==str or type(key)==int: # if 
                point = self.send
            elif type(key)==tuple or type(key)==list:
                point = self.click
            else:
                raise ValueError('wrong key input')
            
            t_start = time.time()
            output = False
            keep = 1+keep*1e10
            if dofirst:
                point(key, delay=keywait, msg=msg)
                keep-=1

            if icon_info==None and color_info==None:
                continue
                
            while True:
                if icon_info!=None:
                    output=self.ImgExist(icon_info, timemax=timemax2, least=least, tf=tf, pos=0)
                elif color_info!=None:
                    output=self.PixelExist(color_info, timemax=timemax2, least=least, tf=tf)
                if output:
                    break
                if time.time()-t_start > timemax1:
                    if raise_error:
                        raise ValueError('wrong key input')
                    else:                    
                        return(False)
                if keep>0:
                    point(key, delay=keywait, msg=msg)
                    keep-=1
        return(True)
                    
            
    ############################
    ### basic game functions ###
    ############################
    def login_func(self):
        if 'LDPlayer' in win32gui.GetClassName(self.hwnd0):
            factor = 1.15
        elif 'WindowOwnDCIcon' in win32gui.GetClassName(self.hwnd0):
            factor = 1
        login = self.ImgExist((0,0,1,1,gamelogo, 0.9, 1400*factor, 786*factor),pos=1)
        if login[0]<0.9:
            return

        self.login_num += 1
        self.resizeWindow()
        while self.ImgExist((0,0,1,1,gamelogo, 0.9, 1400*factor, 786*factor)):
            self.click((login[1], login[2]), delay = 2)
        self.click((0.5, 0.02), delay = 1)
        if self.PixelExist(color_redblood):
            return
        t_start=time.time()
        
        while not self.PixelExist((870/960, 80/540, 930/960, 309/540, '0xD7D928', 5)): # not find select character
            if time.time()-t_start>30*60: # if wait too long
                print('關閉遊戲')               
                self.shutdown()
                raise ValueError('畫面卡住: 重新登入')
            self.click((730/960, 297/540), 2)
        self.char = 1 
        if self.char==1:
            self.myclick((900/960, 95/540), delay=2, color_info=(870/960, 85/540, 930/960, 95/540, '0xD7D928', 0), msg='選擇腳色 1', mode=4) 
        if self.char==2:
            self.myclick((900/960, 171/540), delay=2, color_info=(870/960, 170/540, 930/960, 175/540, '0xD7D928', 0), msg='選擇腳色 2', mode=4) 
        self.waitloading()
        self.home_screen(timemax=120)
        print('登入成功')
    
    def home_screen(self, timemax=10):
        # find red blood and fix white point
        if self.title=='Moonlight_Global':
            hwnd_promotion = win32gui.FindWindowEx(None, None, None, 'Promotion')
            while hwnd_promotion!=0: # advertisments
                time.sleep(5)
                lParam = win32api.MAKELONG(24, 653)
                win32api.SendMessage(hwnd_promotion, win32con.WM_ACTIVATE, 2)
                win32api.SendMessage(hwnd_promotion, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                time.sleep(0.05)
                win32gui.SendMessage(hwnd_promotion, win32con.WM_LBUTTONUP, None, lParam)
                time.sleep(2)
                hwnd_promotion = win32gui.FindWindowEx(None, None, None, 'Promotion')
        _, _, w, h = self.getWindowRect()
        if w!=1400:
            self.resizeWindow()
        ### picture check
        if self.mode=='economic':
            return

        if self.check_home_screen():
            print('返回主畫面成功')
            return
        elif self.check_economic(shot=0):
            self.myclick( key_info(key=(0.5,0.866), keep=True, color_info=(0.971, 0.051, 0.971, 0.051, '0xFFFFFF'),msg='解除省電'))
        elif self.check_dead(shot=0):
            self.resurrect(gap=self.gap_resurrect)
            self.num_resurrect -= 1
        elif self.check_loading(shot=0):
            self.waitloading()
        elif self.team_accept and self.PixelExist((0.225, 0.420, 0.229, 0.424, '0xD6DA29', 5), shot=0):
            self.myclick(key_info(key=(0.227,0.422), color_info='0xD6DA29', tf=False, msg='加入隊伍'))

        t_start = time.time()
        while not self.check_home_screen():
            self.myclick(self.key_back_to_redblood)
            if self.PixelExist(color_logout):
                self.myclick(key_info(key=(0.97,0.05), color_info=color_logout, tf=False, msg='關閉選單'))
            if time.time()-t_start>timemax:
                raise ValueError('返回主畫面出錯')
        if self.PixelExist((0.974, 0.571, 0.974, 0.571, '0xFFFFFF',0)) and self.PixelExist((0.934, 0.571, 0.934, 0.571, '0xD6D727',0)): # 撿到裝備
            self.myclick((0.974,0.571),delay=0)
            print('返回主畫面成功')
            
    def idle_fight(self):
        if self.check_home_screen():
            print('idle')
            if self.location == '公會狩獵地圖':
                self.suitup(self.equip_guild, self.statue_guild, self.friend_guild)
            else:
                self.suitup(self.equip_basic, self.statue_basic, self.friend_basic, water=self.water_basic)
            if self.location != '公會基地':
                self.fight(1)
                self.switch_page(1)
        
    def economic(self):
        if self.mode!='economic':
            return        
        if self.check_economic():
            return
        if not self.PixelExist(color_logout):
            while not self.check_home_screen():
                self.myclick(self.key_back_to_redblood)
            if not self.PixelExist(color_logout):
                self.myclick(self.key_openlist)
        self.myclick(key_info(key=(0.686, 0.94), color_info=color_logout, tf=False, msg='省電模式'))
        self.t_economic = time.time()

    def resurrect(self, gap):
        t_start = time.time()
        while time.time()-t_start<gap:
            print('復活倒數'+str(int(t_start+gap-time.time())))
            time.sleep(1)
        self.myclick((475/960, 270/540), delay=delay, msg='自動復活')                
        while not self.PixelExist(color_fight):
            self.fight(1)
        return
    def leave_guild_to_normal(self):
        if self.mode!='leave_guild':
            return
        print('離開公會')
        val, x, y = self.ImgExist((0.001, 0.162, 0.06, 0.9, back, 0.8, 1400, 786), pos=1)
        self.myclick((x, y),msg='離開公會', color_info=(0.535, 0.599, 0.535, 0.599, '0xD6D727', 5))
        self.myclick((0.535, 0.599))
        self.waitloading()
        time.sleep(1)  
                

    def suitup(self, equip=0, statue=0, num_friend=0, water=0, fight=1, fmode=2):
        while equip!=self.equip and equip!=0:
            pts_equip = [(0.551, 0.802), (0.586, 0.802), (0.623, 0.802)] # positions of equip=1, 2, 3
            self.fight(fmode)
            if statue!=self.statue and statue!=0 and self.PixelExist((0.190,0.832,0.192,0.834,'0xFFFFFF',0, False)):
                self.click((0.191,0.921),delay=0, color_info=(0.190,0.832,0.192,0.834,'0xFFFFFF',0))
            self.myclick(key_info(self.key_bag, keep=True, msg='背包', color_info=(0.895, 0.056, '0xe8a346'), tf=False, dofirst=False))
            self.myclick(pts_equip[equip-1])
            self.check_equip()        
        while statue!=self.statue and statue!=0:
            pts_statue = [(0.173, 0.826), (0.173, 0.752), (0.173, 0.678)] # positions of statue=1, 2, 3
            self.fight(fmode)
            if not self.PixelExist((0.191,0.833,0.191,0.833,'0xFFFFFF',0)) or not self.PixelExist((0.191,0.761,0.191,0.761,'0xFFFFFF',0)): # 未開啟雕像切換
                self.click((0.191,0.921),delay=0, color_info=(0.190,0.832,0.192,0.834,'0xFFFFFF',0))                                
            self.myclick(pts_statue[statue-1])
            self.check_statue()
        if not self.check_home_screen(shot=0):
            self.myclick(self.key_back_to_redblood)
            
        if self.water!=water and type(water)==bool:
            pts_water = [(0.705,0.62), (0.655,0.62)] # 20%HP, 30%HP
            self.click((0.68,0.934),delay=0, color_info=(0.770,0.524,0.775,0.526,'0xFFFFFF',0))
            self.myclick(pts_water[int(water)])
            self.water = water

        if self.friend!=num_friend and num_friend>0:
            if self.title != 'Moonlight_Global':
                self.myclick(key_list, delay=delay, color_info=color_graycross, msg='開啟選單', mode=2)
            self.myclick(self.key_friend, delay=delay, color_info=color_graycross, msg='切換夥伴', mode=2)
            num_friend -= 1
            row_friend, col_friend = num_friend//5, num_friend%5
            self.myclick( (0.679+col_friend*0.070, 0.346+row_friend*0.127) )
            if self.PixelExist((0.531, 0.921, 0.531, 0.921, '0xD6DA29',5)):
                self.myclick((0.531, 0.921), delay=delay, msg='召喚夥伴')
                self.friend = num_friend+1
            elif self.PixelExist((0.531, 0.921, 0.531, 0.921, '0x6B6152',5)):
                print('不用切換')
                self.friend = num_friend
            else:
                print('無法召喚夥伴')
            self.myclick(self.key_back_to_redblood)
        self.fight(fight)

    def supplement(self, sp=False, ep=False):
        if sp:
            if self.sp:
                print('30%狂暴藥水效果還在')
            else:
                sp_icon=[]
                for i in range(0, 5):
                    sp_icon.append( (0.707+i*0.047, 0.79, 0.707 + (i+1)*0.047, 0.847, speedpotion, 0.8, 1400, 786))
                t_start, posi = time.time(), 0
                while posi==0 and time.time()-t_start<2:
                    posi = self.BestImgExist(sp_icon, thresh=0.8)
                if posi==0:
                    print('找不到30%狂暴藥水')
                    self.switch_page()
                    t_start = time.time()
                    while posi==0 and time.time()-t_start<2:
                        posi = self.BestImgExist(sp_icon, thresh=0.8)
                    if posi==0:
                        print('找不到30%狂暴藥水')
                    else:
                        self.myclick((0.707+posi*0.047-0.023, 0.825), msg='使用30%狂暴藥水')
                        self.t_sp = time.time()
                        self.check_sp()
                if ep:
                    self.switch_page(2)
                else:
                    self.switch_page(1)
        if ep: # 喝速度水
            self.check_ep()
            if self.ep:
                print('愛娜效果還未消失')
            else:
                self.switch_page(2)
                ep_icon=[]
                for i in range(0, 5):
                    ep_icon.append( (0.707+i*0.047, 0.79, 0.707 + (i+1)*0.047, 0.847, enapotion, 0.8, 1400, 786))
                t_start, posi = time.time(), 0
                while posi==0 and time.time()-t_start<2:
                    posi = self.BestImgExist(ep_icon, thresh=0.8)
                if posi==0:
                    print('找不到愛娜')
                    output = False
                else:
                    self.myclick((0.707+posi*0.047-0.023, 0.825), msg='使用愛娜')
                    self.t_ep = time.time()
                    self.check_ep()
            self.switch_page(1)

            
    def fight(self, fmode=1):
        if self.location == '公會基地' or self.location == '家裡':
            print('無法切換')
            return            
        self.check_fmode()
        pt = (269/960, 495/540)
        if fmode==self.fmode:
            return
        elif fmode == 0: #
            self.myclick( pt, msg='停止戰鬥', mode=3, color_info=color_fight)
        elif fmode == 1:
            if self.fmode == 0:
                self.myclick( pt, msg='開始戰鬥', mode=1, color_info=color_fight)
            elif self.fmode == 2:
                self.click((0.28,0.913),delay=0, color_info=(0.293,0.831, 0.295, 0.833,'0xFFFFFF',10))
                self.click((0.28,0.828), delay=0.3, msg='自動攻擊模式')
        elif fmode == 2:
            self.click((0.28,0.913),delay=0, color_info=(0.293,0.831, 0.295, 0.833,'0xFFFFFF',10))
            self.click((0.28,0.777),delay=0.3, msg='半自動攻擊模式')

        self.fight(fmode) # recurssion
    def use_item(self, num, delay=1, msg=''):
        if num==0:
            return
        if len(msg)>0:
            msg= ': '+msg
        self.myclick( ((1090+77*num)/1600, 750/900), delay=delay, msg='使用物品 '+str(num)+msg)
    def switch_page(self, page=0):
        if self.page==0:
            return
        if page==0:
            page = 3-self.page
        if page!=self.page:
            if page==1:
                self.myclick( key_info(self.key_switch, icon_info=(0.95,0.86,0.99,0.91,pageone,0.9,1400,786), msg='切換到技能頁 1'))
            elif page==2:
                self.myclick( key_info(self.key_switch, icon_info=(0.95,0.86,0.99,0.91,pagetwo,0.9,1400,786), msg='切換到技能頁 2'))
            self.check_page()
            
    ###############################
    ### advanced game functions ###
    ###############################        
    def cutweight(self, delay=1, saveonly=False):
        if self.mode!='overweight' and self.mode!='bagfull':
            return
        self.home_screen()

        if not saveonly:
            print('執行功能: 呼叫商店')
            self.myclick(key_info(self.key_bag, keep=True, msg='背包', color_info=(0.895, 0.056, '0xe8a346'), tf=False))
            if not self.PixelExist((0.892, 0.751,0.892, 0.751, "0xD3D727", 5)):
                print("無法呼叫商店")        
            else:        
                c2=key_info( key=(0.893, 0.760), keep=True, color_info=color_blueconfirm, msg='呼叫商店')
                c3=key_info( key=(0.558, 0.601), keep=True, color_info=(0.1, 0.1, '0xFFFFFF'), msg='確認')
                c4=key_info( key=(0.214, 0.100), keep=True, color_info='0xFFFFFF', msg='販賣')
                c5=key_info( key=(0.303, 0.921), msg='全部販賣')
                self.myclick([c2, c3])
                num_potion = int((time.time()-self.t_hardpotion)//600)
                num_potion = 0
                if num_potion>0:
                    self.myclick((0.043, 0.573), color_info=(0.676, 0.872, '0xd6d726'), msg='硬化劑')
                    self.myclick((0.514, 0.686))
                    self.send_char(str(num_potion))
                    self.myclick(key_info((0.676, 0.872), color_info=(0.676, 0.872, '0xd6d726'), tf=False,msg='確認'))
                    self.t_hardpotion = time.time()
                self.myclick([c4, c5])            
            self.myclick(self.key_back_to_redblood)
            
            if not self.check_weight() and self.mode!='bagfull':
                return    
            print('執行功能: 裝備分解')
            c1=key_info((600/960, 100/540), color_info=(0.271, 0.151, '0xDEDEDE'))
            c2=key_info((780/960,  80/540), color_info=(0.860, 0.151, '0xDEDEDE'))
            c3=key_info(key=(0.478, 0.681), keep=True, color_info='0xFFFFFF', tf=False, msg='取消紫裝', dofirst=False)
            self.myclick([self.key_openlist, c1, c2, c3])
            
            while True:
                E1 = self.PixelExist((0.205, 0.405, '0x5B5B5B',-4), least=0.2)
                E2 = self.PixelExist((0.461, 0.907, '0xd6db29',-4), least=0, shot=0)
                if E1 and not E2:
                    break
                else:
                    self.myclick(key_info(key=self.key_decompose, delay=0))            
                if not E2:
                    self.myclick(key_info(key=self.key_decompose, delay=0))
            self.myclick(self.key_back_to_redblood)        
        
            if not self.check_weight():
                return    
        
        if self.title != 'Moonlight_Global':
            self.myclick(self.key_openlist)
        self.myclick(key_info(self.key_friend, color_info=(0.281,0.156,'0xDEDEDE'), msg='執行功能: 夥伴跑腿'))
        
        if not self.PixelExist( (0.422, 0.922,0.422, 0.922, "0x6B6152", 5) ):
            print("無法跑腿")
            self.myclick(self.key_back_to_redblood)
        if self.PixelExist( (0.539, 0.922, "0xD4D727") ):
            c1=key_info((0.684, 0.351), delay=1, msg="重新召喚寵物") # 第一個
            c2=key_info((0.539, 0.922), keep=True, color_info="0xD4D727", tf=False)
            self.myclick([c1, c2])

        c1=key_info(key=(0.422  ,   0.922), color_info=color_blueconfirm)
        c2=key_info(key=(580/960, 325/540), color_info=(0.862, 0.925,'0xD6DA29'), msg='確認')
        c3=key_info(key=(800/960, 500/540), color_info=(0.971, 0.925,'0xD6DA29'), msg='多項選擇')
        c4=key_info(key=(900/960, 500/540), msg='保管')
        self.myclick([c1, c2, c3, c4, self.key_back_to_redblood])

    def auction(self):
        if self.mode!='auction':
            return
        self.home_screen()
        items=[]
        if len(self.auction_item)>0:
            for item in (self.auction_item).split(','):
                items.append(item.replace(' ', ''))
        c1=key_info((0.925, 0.629), color_info=(0.31, 0.163,'0xDEDEDE'), msg='交易所', mode=1)
        c2=key_info((0.367, 0.950), color_info=(0.872,0.093,'0x6B6152'), msg='投標狀態', mode=1)
        c3=key_info((0.796, 0.903), delay=delay/4)
        c4=key_info((0.872, 0.093), color_info=(0.31, 0.163,'0xDEDEDE'), mode=1)
        self.myclick([self.key_openlist, c1, c2, c3, c4])
        
        def auction_buy():
            human_head = (0.679, 0.427, 0.681, 0.429, '0x6B6152', 0)
            y_upper = 0.335    
            while True:
                gold = self.PixelExist(human_head)
                if gold: # 1st page
                    lst = self.PixelExist((0.959, 0.333, 0.959, 0.91, '0xD5D728', 10))
                else: # 2nd page
                    lst = self.PixelExist((0.959, y_upper, 0.959, 0.91, '0xD5D728', 10))
                if gold:
                    if lst:
                        x, y = self.PixelExist((0.959, 0.333, 0.959, 0.91, '0xD5D728', 10), pos=1)
                        suc = self.myclick( key_info((x, y), color_info=color_graycross, tf=False, msg='投標'), raise_error=False)
                        if suc:
                            self.myclick(key_info((0.575, 0.707), color_info=human_head, msg='確認'))
                        else:
                            print('金幣不夠')
                            break
                        # 按完確定
                        if self.PixelExist( (x, y, '0xD5D728') ):
                            print('已經投滿20個物品')
                            break                    
                    else:
                        self.myclick((0.171, 0.252, 0.171, 0.252), color_info=human_head, delay=delay, msg='返回', mode=3)
                        y_upper = y_upper + 0.142
                else: # no gold
                    if lst:
                        x, y = self.PixelExist((0.959, y_upper, 0.959, 0.91, '0xD5D728', 10), pos=1)
                        self.myclick((x, y), delay=delay, color_info=human_head, msg='販賣清單', mode=1)
                    else:
                        break    
        self.myclick(key_info((0.13, 0.4), color_info='0xD5D5D5', msg='願望清單'))
        type = 1
        if not self.PixelExist((0.224,0.23,0.322,0.271,'0x6B6152'), timemax=2):
            self.myclick(key_info((0.13, 0.3), color_info='0xD5D5D5', msg='願望清單'))
            type = 2
        if not self.PixelExist((0.224,0.23,0.322,0.271,'0x6B6152'), timemax=2):
            raise ValueError('交易所出錯')
        auction_buy()
        print(type)
        if len(items)>0:
            while self.PixelExist((0.224,0.23,0.322,0.271,'0x6B6152'), timemax=2):
                if type==2:
                    self.click(key=(0.1, 0.3), key2=(0.1, 0.4)) # 拉到底.
                self.myclick(key_info((0.13, 0.3), color_info='0xD5D5D5', msg='全部'))

        for item in items:
            self.myclick((0.711,0.955), color_info=(0.96,0.978,0.96,0.978,'0xCED321'), timemax=11, msg='等待搜尋10秒...')
            self.send_char(item)
            self.myclick((0.96,0.978), color_info=(0.96,0.978,0.96,0.978,'0xCED321',False), timemax=2, msg='搜尋: '+item)
            auction_buy()
        
        self.myclick(self.key_back_to_redblood)
        self.t_auction = time.time()
        save_setup(self)        
    
    # this not yet
    def teamup(self, delay=1): # not yet fixed
        if self.mode!='teamup':
            return
        self.home_screen()
        icon_teamup = (0.068, 0.065, 0.304, 0.91, password_teamup2, 0.1,1400,786)
        c1=key_info(self.key_chat, keep=True, color_info=(0.324, 0.032,0.324, 0.032,'0x6B6152',0), msg='聊天室')
        c2=key_info(key=(0.062, 0.733), keep=True, color_info=(0.062, 0.733,0.062, 0.733,'0xDEDEDE'), dofirst=False, msg='悄悄話')
        self.myclick([c1, c2])
        val, x, y = self.ImgExist(icon_teamup,gray=1,pos=1)
        if val>0.93:
            self.myclick(key_info((x, y), keep=True, color_info=(0.181, 0.962, '0xFFFFFF')))
            self.myclick(key_info((0.135, 0.887), keep=True, color_info=(0.25, 0.19, '0xced321')), raise_error=False)
            self.myclick((0.25, 0.19))
            self.myclick((0.159, 0.955))
            self.send_char('OK')
            self.myclick((0.272, 0.961))    
        self.myclick(self.key_back_to_redblood)
        self.t_teamup = time.time()

    def guild_hunt(self): # done
        if self.mode!='guild_hunt':
            return
        self.home_screen()
        print("狩獵囉! hunt!!")
        ## 進入公會基地
        self.fight(2)
        color_guild = (0.175, 0.156, '0xDEDEDE')
        c1 = key_info(key=(0.614,0.627), color_info=color_guild, msg='公會')
        c2 = key_info(key=(0.221,0.873), color_info=color_guild, msg='公會基地', tf=False)
        c3 = key_info(key=(0.540,0.595), color_info=(0.533, 0.598, '0xd6d924'), msg='確認', tf=False)
        while True:
            if self.PixelExist(color_redblood):
                self.myclick([self.key_openlist, c1])
            if self.PixelExist(color_guild):
                self.myclick(c2)
                if self.PixelExist((0.481, 0.598, '0x6b6152',0)):
                    self.myclick(c3)
                else:   
                    print('進入公會太快')
                    self.myclick(self.key_back_to_redblood)
            if self.check_loading(timemax=5):
                break
        self.waitloading()
        
        ## 前往狩獵場入口
        t_start = time.time()
        self.map((0.718, 0.517), msg='前往公會狩獵場')        

        while time.time()-t_start<10:
            print('等待跑步')
            time.sleep(1)
        ## 進場
        self.myclick(key_info(key=(0.515, 0.586), color_info=color_redblood, tf=False))
        if self.PixelExist((0.671,0.808,0.675,0.812,'0xD6DA29',5)):
            self.myclick((0.673, 0.810), delay=delay, msg='確認進場')
        else:
            print('已經完成今天狩獵')
            self.myclick(self.key_back_to_redblood)
            self.d_hunt = clock2('day')
            save_setup(self)
            return

        ## 等loading 
        self.waitloading()
        time.sleep(delay)
        
        ## 前往狩獵點
        self.suitup(self.equip_guild, self.statue_guild, self.friend_guild, fight=1)
        self.map((self.x_guild, self.y_guild), msg='前往打怪點') # 打開地圖
        self.d_hunt = clock2('day')
        save_setup(self)
        
    def map(self, key, msg=''): # done, but need to fly to another map
        if len(msg)>0:
            print(msg)
        while not self.check_home_screen():
            self.myclick(self.key_back_to_redblood)
        self.myclick(key_info(key=self.key_map, color_info=color_graycross, msg='打開地圖'))
        x, y = key; t_start = time.time()
        while not self.myclick(key_info(key=(x, y), color_info='0x4856EE', timemax1=1, msg='前往x='+str(x)+', y='+str(y)), raise_error=False):
            # if humanhead at (x, y): break
            x+=0.01; y+=0.01
            if time.time()-t_start>30:
                raise ValueError('地圖出錯')
        self.myclick(self.key_back_to_redblood)
        
    def raid_boss(self, x_boss, y_boss): # done
        self.checkusing = 0 # 暫停腳本後繼續
        
        # 需要考慮死亡的情況下王死掉
        red_countdown = (0.915, 0.49, 0.938, 0.507, '0x0000FF', 0)
        boss_appear = (0.655, 0.105, 0.660, 0.109, '0x38C4FF', 10) # 黃色x3~x1
        boss_bloodnumber = (0.46, 0.095, 0.49, 0.1, '0xFFFFFF', 20)
        boss_debuff = (0.40, 0.12, 0.45, 0.15, '0x6550E7',0)
        check_result = (0.44, 0.734, 0.44, 0.734,'0x6B6152',0) # 查看結果
        confirm = (0.56, 0.734, 0.56, 0.734,'0xD6DB29',0) # 確認
        
        # exe=1: change friend and water
        key_num, key_moves, t_move = 0, [self.key_left, self.key_right], time.time()


        self.suitup(self.equip_raid, self.statue_raid, self.friend_raid, water=self.water_raid, fight=0, fmode=0)
        self.map((x_boss, y_boss))

        # prepare before raid fight
        gap_move = np.random.randint(20,40)
        while not self.PixelExist(boss_appear):
            if time.time()-t_move > gap_move:
                self.myclick(key_moves[key_num], msg='左移')
                key_num, t_move = 1-key_num, time.time()
                gap_move = np.random.randint(20,40)                
            if self.PixelExist(red_countdown) and self.sp!=self.sp_raid:
                self.supplement(sp=self.sp_raid)
            if self.ImgExist((0.913,0.488,0.940,0.51,countdown2, 0.9,1400,786), gray=True): # 剩兩秒時切自動
                break
        print('突襲boss出現!')
        self.fight(1)

        ct=0
        t_start = time.time()
        while time.time()-t_start<15*60:
            E0 = self.check_dead()
            E1 = (self.PixelExist(boss_appear, shot=0) and self.PixelExist(boss_bloodnumber, shot=0) and self.PixelExist(boss_debuff, shot=0))
            E2 = (self.PixelExist(check_result, shot=0) and self.PixelExist(confirm, shot=0))
            if E0:
                ct=0; print('角色死亡')
                self.resurrect(gap=self.gap_resurrect_raid)
            elif E1: # 王存在
                ct=0; print('突襲王未死亡!')
            elif E2: # 有可能在過場動畫前就判斷到，或者結束後才判斷到
                ct=0; print('過場畫面結束! ')
                self.myclick(key_info(key=(0.56, 0.734), keep=True, color_info='0xD6DB29', tf=False))
                break
            elif ct>3:
                print('突襲王死亡, 等待過場動畫')
            else:
                ct+=1
            time.sleep(1)

        # 離場
        self.myclick(key_info(key=(0.874, 0.575), keep=True, color_info=(0.535, 0.598, '0xD6DB29'), msg='離開突襲'))
        self.myclick((0.535, 0.598), delay=delay, msg='確定') # blue finish:
        self.checkusing = 1
        self.waitloading()
        
    def normal_raid(self, delay=1): # done
        if self.mode!='normal_raid':
            return
        print('進行突襲副本')
        self.home_screen()
        c1=key_info(key=(0.754, 0.332), color_info=(0.32,0.15,'0xDEDEDE',0), msg='突襲')
        self.myclick([self.key_openlist, c1])
        while not self.ImgExist((0, 0.87,0.2, 1, raidend, 0.7, 1400, 786), least=0):
            self.click(key=(0.1, 0.98), key2=(0.1, 0.02)) # 拉到底.
            time.sleep(1)
        
        if self.level_raid==280:
            h, name, fx, fy = 1, '冰龍的庇護所', 0.802, 0.498
        elif self.level_raid==295:
            h, name, fx, fy = 2, '冰龍深層的庇護所', 0.802, 0.498
        elif self.level_raid==290:
            h, name, fx, fy = 3, '暗紅宴會場', 0.8, 0.4
        elif self.level_raid==305:
            h, name, fx, fy = 4, '幻影暗紅宴會場', 0.8, 0.4
        elif self.level_raid==300:
            h, name, fx, fy = 5, '灰色祭壇', 0.744, 0.517
        elif self.level_raid==315: 
            h, name, fx, fy = 6, '損毀灰色祭壇', 0.744, 0.517
        
        self.myclick( (0.1, 0.097+0.144*h), delay=delay, msg='選擇關卡: '+name)

        # 判斷是否可進入
        if not self.PixelExist((0.739, 0.897, 0.741, 0.899, '0xD6DA29',5)):
            print('不能入場')
            return
        else:
            self.myclick( (0.741,0.896), delay=delay, msg='進入突襲')
            if self.PixelExist((0.57, 0.664, 0.57, 0.664, '0xD6DA29',5)): # 次數不足，使用票嗎
                if self.ticket_raid:
                    self.myclick((0.57,0.664), delay=delay, msg='確認')
                else:
                    return
        self.waitloading()
        x, y = np.random.uniform(-0.05,0.05,2) 
        self.raid_boss(x_boss=fx+x, y_boss=fy+y)
    
    def daily_raid(self, level=8): # done
        if self.mode!='daily_raid':
            return        
        print('進行每日副本')
        self.home_screen()
        self.fight(2)
        c1 = key_info( key=(0.615,0.333), color_info=color_redblood, tf=False, msg='副本')
        self.myclick([self.key_openlist, c1])
        if not self.PixelExist((0.022,0.153, '0x0000FF')):
            print('每日副本已完成')
            self.d_daily = clock2('day', tt=5)
            save_setup(self)
            self.myclick(self.key_back_to_redblood)
            self.fight(1)
            return 
        
        # c2 = key_info( key=(0.169,0.266), color_info='0xDEDEDE', msg='每日副本')
        self.myclick((0.169,0.266), color_info='0xDEDEDE', msg='每日副本')
        self.click(key=(0.1, 0.98), key2=(0.1, 0.02)) # 拉到底.
        c3 = key_info( key=(0.158, 0.150+0.105*level), keep=True, color_info='0xDEDEDE')
        c4 = key_info( key=(0.75, 0.81), keep=True, color_info=color_graycross, tf=False, msg='確認進入: 難度'+str(level))
        self.myclick([c3, c4])

        self.waitloading()
        self.fight(1)
        while not self.PixelExist((0.530, 0.665, 0.535, 0.670, '0x6B6152',5), least=0.5):
            print('等待完成副本')
            if not self.PixelExist(color_fight):
                self.myclick((0.5,0.02),delay=delay)
            time.sleep(1)
        self.myclick((0.531, 0.669), delay=delay, msg='每日副本完成! 離開副本')
        self.waitloading()
        self.daily_raid()
        
        
    def get_reward(self, end=2): # done
        if self.mode!='get_reward' or end<=0:
            return
        else:
            self.get_reward(end=end-1)

        self.home_screen()
        def red_point_detecter():
            pts_posi = []
            pts_type = []
            val, _, y_lim = self.ImgExist((0.059, 0.087,0.261, 0.933,achieve_level,0.85,1400,786),pos=1) # 等級達成位置
            if val<0.85:
                y_lim = 0.95
            y_upper = 0.087
            while self.PixelExist((0.074, y_upper, 0.076, y_lim-0.04, '0x0000FF',0), shot=0):    
                cx, cy = self.PixelExist((0.074, y_upper, 0.076, y_lim-0.04, '0x0000FF',0), shot=0, pos=1)
                pts_posi.append( (cx, cy) )
                if self.PixelExist((cx+0.01, cy, cx+0.01, cy, '0xEEEEEE',-3), shot=0): # 大區域
                    pts_type.append(1)
                elif self.PixelExist((cx+0.01, cy, cx+0.01, cy, '0xCECECE',-3), shot=0): # 未被選取的小區域
                    pts_type.append(2)
                elif self.PixelExist((cx+0.01, cy, cx+0.01, cy, '0xDEDEDE',-3), shot=0): # 已被選取的小區域
                    pts_type.append(3)
                y_upper = cy + 0.04
            return (pts_posi, pts_type)
        key_event = key_info(key=(0.79, 0.28), color_info=(0.93,0.127,0.93,0.127,'0x6B6152',0))
        while True:
            if self.PixelExist(color_redblood):
                self.myclick(key_event) # 活動
            elif not self.PixelExist((0.93,0.127,0.93,0.127,'0x6B6152',0)):
                self.myclick((0.5,0.02),delay=delay)

            pts_posi, pts_type = red_point_detecter()
            if 3 in pts_type: # 存在已被選取的小區域: 領獎
                h, w, _ = self.img.shape
                if self.PixelExist((0.479, 0.845,0.479, 0.845, '0xD6DA29',5)): #輪盤
                    cx, cy = 0.479, 0.845
                elif self.PixelExist((0.897, 0.557,0.897, 0.557, '0xD6DA29',5)): #公會簽到
                    cx, cy = 0.897, 0.557
                else:
                    region = [[0.512,0.408, 0.915, 0.616],
                              [0.512,0.674, 0.915, 0.832],
                              [0.279,0.202, 0.913, 0.854]]
                    i, img0, t_start = -1, self.screenshot(), time.time()
                    time.sleep(1)
                    while True:
                        i = (i+1)%3
                        c_x1, c_y1, c_x2, c_y2 = region[i]
                        img1 = self.screenshot()
                        diff_sub = img0[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),] - img1[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),]
                        yy, xx = np.where(np.sum(abs(diff_sub),axis=2)>10)
                        if len(yy)>2 and len(xx)>2:
                            break
                        if time.time()-t_start>3:
                            raise ValueError('找不到禮物')
                    cx, cy = (c_x1+(min(xx)+max(xx))/2/w, c_y1+(min(yy)+max(yy))/2/h)
                self.myclick(key_info(key=(cx, cy), color_info=(0.931, 0.126,'0x6b6153'), tf=False, msg='領獎'))
                
            elif 2 in pts_type: # 未被選取的小區域: 點開第一個pts_type==2
                for i in range(0,len(pts_type)):
                    if pts_type[i]==2:
                        self.myclick(pts_posi[i],delay=delay)
                        break    
            elif 1 in pts_type: # 紅點只有大區域
                cx, cy = pts_posi[0]
                if self.PixelExist((cx, cy+0.078, cx+0.01, cy+0.079, '0xCECECE',-3),shot=0) or self.PixelExist((cx, cy+0.078, cx+0.01, cy+0.079, '0xDEDEDE',-3),shot=0):
                    print('向下捲')
                    self.click(key=(0.2, 0.82), key2=(0.2, 0.15),press2=0.6)                                            
                else:
                    self.myclick((cx, cy),delay=1)
            else:
                self.myclick([self.key_back_to_redblood, key_event]) # 活動
                val, _, y_lim = self.ImgExist((0.059, 0.087,0.261, 0.933,achieve_level,0.85,1400,786),pos=1) # 等級達成位置
                pts_posi, pts_type = red_point_detecter()
                if len(pts_type)==0:
                    self.myclick([self.key_back_to_redblood])
                    break
        self.d_reward = clock2('day',tt=0)
        save_setup(self)
                
    def coinstore(self, end=2): # done # 增加狂暴, 紅水, 藍水, 硬化
        if self.mode!='coinstore' or end<=0:
            return
        else:
            self.coinstore(end=end-1)

        coin_store_page = (0.674,0.191,0.674, 0.191,'0xDEDEDE', 0)

        self.home_screen()
        self.myclick(self.key_mall, delay=1, color_info=(0.205, 0.162, 0.205, 0.162, '0xDEDEDE'), mode=1, msg='開啟商城')
        self.myclick((0.538, 0.155), delay=1, color_info=coin_store_page,mode=1, msg='金幣商店')
            
        items = os.listdir('figures/item_daily')

        threshold = 0.8
        if self.title=='Moonlight_Global':
            threshold = 0.92
        pages = range(0,4)
        for i in pages:
            self.myclick( key_info( key=(0.15,0.257+i*0.094),keep=True, color_info='0xDEDEDE', msg='下一頁'))
            j=0
            while j < len(items):
                icon_info = (0,0,1,1, cv2.imread('figures//item_daily//'+str(items[j])), 0.1,1400,786)
                val, x, y = self.ImgExist(icon_info,pos=1,gray=True)
                if val>threshold:
                    self.myclick( key_info(key=(x, y), color_info=coin_store_page,tf=False, msg='選擇物品'))
                    if self.PixelExist((0.74,0.602,'0x6B6152')): # 買到最大
                        self.myclick((0.74,0.602),delay=0.1, msg='買到最大')
                    self.myclick((0.584,0.856), color_info = coin_store_page, msg='確認')
                    while val>threshold: # 等待目標物品消失
                        val, _, _ = self.ImgExist(icon_info,pos=1,gray=True)
                    items.pop(i)
                    j=0
                else:
                    j=j+1
        self.myclick(self.key_back_to_redblood)
        self.d_coinstore = clock2('day',tt=0)
        save_setup(self)
        
    def pvp(self, delay=1):
        if self.mode != 'pvp':
            return
        print('pvp 開啟中')

        self.home_screen()
        # check pvp is open

        c1 = key_info((0.891, 0.345), keep=True, color_info=color_redblood, tf=False, msg='決鬥場')
        self.myclick([self.key_openlist, c1])

        if self.PixelExist((0.858, 0.952, '0xf7f8d5')):
            print('決鬥場未開放')
            self.myclick(self.key_back_to_redblood)                       
            return
        elif self.until_reward and self.PixelExist((0.796, 0.786, 0.796, 0.786, '0x7F3F00',0)) and self.PixelExist((0.978, 0.786, 0.978, 0.786, '0x5A5A5A',0)):
            print('已完成決鬥場獎賞')
            self.myclick(self.key_back_to_redblood)                       
            self.d_pvp = clock2('day')
            save.setup(self)
            return            

        print('換裝')
        self.myclick(self.key_back_to_redblood)        
        self.suitup(self.equip_pvp, self.statue_pvp, self.friend_pvp)
        self.supplement(sp=(self.sp!=self.sp_pvp), ep=(self.ep!=self.ep_pvp))

        c2 = key_info((0.858, 0.949), keep=True, color_info=color_graycross, tf=False, msg='開始排隊')
        c3 = key_info((0.63, 0.565))
        self.myclick([self.key_openlist, c1, c2, c3])

        lose = (0.532,0.622, '0x6B6152') # 輸的確認位置
        win = (0.532,0.710, '0x6B6152')  # 贏的確認位置
        pvp_finish = (0.607,0.432,0.607,0.432,'0xFFFFFF',0) # 結束畫面一定出現的白色點


        t_pvp_upper = self.hour_end_pvp*60+self.min_end_pvp
        while True:
            print('等待配對')
            if self.PixelExist((0.625,0.675,0.630,0.68,'0xD6DA29',3)): # 確認配對
                self.myclick( (0.627, 0.676), delay=delay, msg='確認進入戰鬥')
            elif self.PixelExist((0.566, 0.547, 0.566, 0.547,'0xD6DA29',3), shot=0): # 被拒絕的確認點
                self.myclick( (0.566, 0.547), delay=delay, msg='確認拒絕戰鬥')
            elif self.check_loading(timemax=2):
                self.waitloading()                
                break
            if clock2()>t_pvp_upper:
                return
        
        while True:
            print('等待戰鬥結束')
            E1 = self.PixelExist(lose)
            E2 = self.PixelExist(win, shot=0)
            E3 = self.PixelExist(pvp_finish, shot=0)
            if E1 and E3:
                self.myclick( key_info( (0.532,0.622), msg='輸了'))
            elif E2 and E3:
                self.myclick( key_info( (0.532,0.710), msg='贏了'))
            elif self.check_loading(timemax=2):
                self.waitloading()
                break
        self.fight(1)
        
    ################
    ### checking ###
    ################
    def check_loading(self, shot=1, timemax=0):
        if timemax>0:
            shot=1
        return self.ImgExist(icon_loading, shot=shot, timemax=timemax)
    def check_weight(self, shot=1):
        return self.PixelExist( (892/960, 37/540, 892/960, 39/540, "0xECA647", 10), shot=shot) # blue bar
    def check_bagfull(self, shot=1):
        return self.ImgExist((0.4, 0.28, 0.595, 0.340, bag_full, 0.5, 1135, 637), gray=True, shot=shot)
    def check_merchant(self, shot=1):
        if self.ImgExist((0.35, 0.28, 0.65, 0.40, merchant, 0.9, 1400, 786), gray=True, shot=shot):            
            output = 1+self.BestImgExist([(0.57,0.28,0.63,0.4,merchant2,0.8,1400,786),
                                          (0.57,0.28,0.63,0.4,merchant3,0.8,1400,786),
                                          (0.57,0.28,0.63,0.4,merchant4,0.8,1400,786),
                                          (0.57,0.28,0.63,0.4,merchant5,0.8,1400,786)], shot=0, gray=True)
            return output
        else:
            return 0
    def check_dead(self, shot=1):
        E1 = self.PixelExist((0.5, 0.600, 0.5, 0.600, '0xD4D725', 5), shot=shot) # search middle blue
        E2 = self.PixelExist((0.5, 0.666, 0.5, 0.666, '0x6B6152', 5), shot=0) # search middle gray
        return (E1 and E2)
    def check_fmode(self, shot=1):
        self.fmode = self.BestImgExist( [(0.263, 0.887, 0.3, 0.957, auto, 0.1, 1400, 786),
                                         (0.263, 0.887, 0.3, 0.957, semi, 0.1, 1400, 786)], shot=shot, thresh=0.7)
    def check_bait1000(self, shot=1):
        return(self.PixelExist((0.722, 0.840, 0.728, 0.857, '0xFFFFFF', 5)))
    def check_equip(self, shot=1):
        self.equip = self.BestImgExist([(0.123, 0.877, 0.162, 0.953, change1, 0.1, 1400, 786),
                                        (0.123, 0.877, 0.162, 0.953, change2, 0.1, 1400, 786),
                                        (0.123, 0.877, 0.162, 0.953, change3, 0.1, 1400, 786)], shot=shot, thresh=0.7)
    def check_statue(self, shot=1):
        self.statue = self.BestImgExist([(0.168, 0.877, 0.207, 0.953, change1, 0.1, 1400, 786),
                                         (0.168, 0.877, 0.207, 0.953, change2, 0.1, 1400, 786),
                                         (0.168, 0.877, 0.207, 0.953, change3, 0.1, 1400, 786)], shot=shot, thresh=0.7)
    def check_water(self, shot=1):
        self.water = self.BestImgExist([(0.659,0.88, 0.7, 0.934, hp20potion, 0.9, 1400, 786),
                                        (0.659,0.88, 0.7, 0.934, hp30potion, 0.9, 1400, 786)], shot=shot, thresh=0.7)
        self.water = bool(self.water-1)
    def check_page(self, shot=1):
        self.page = self.BestImgExist([(0.95,0.86,0.99,0.91,pageone,0.9,1400,786),
                                       (0.95,0.86,0.99,0.91,pagetwo,0.9,1400,786)], shot=shot, thresh=0.7)
    def check_ep(self, shot=1):
        self.ep = self.ImgExist((0.001,0.08, 0.21, 0.13, epeffect, 0.8, 1400, 786), least=0.2) or (time.time()-self.t_ep<60*30)
    def check_sp(self):
        self.sp = (time.time()-self.t_sp<600)
    def check_friend(self, shot=1):
        if shot:
            self.screenshot()
        x_d, y_d = 0.0688, 0.1228
        self.friend = 0
        for i in range(0, 5):
            for j in range(0, 5):
                E1 = self.PixelExist((0.662+x_d*i, 0.354+y_d*j, 0.662+x_d*i, 0.354+y_d*j, '0xFFFFFF',0), shot=0)
                E2 = self.PixelExist((0.674+x_d*i, 0.373+y_d*j, 0.675+x_d*i, 0.373+y_d*j, '0xFFFFFF',0), shot=0)
                E3 = self.PixelExist((0.698+x_d*i, 0.333+y_d*j, 0.698+x_d*i, 0.333+y_d*j, '0xFFFFFF',0), shot=0)
                if E1 and E2 and E3:
                    self.friend = j*5+i+1
                    return        

    def check_location(self, shot=1):
        if self.ImgExist((0.001, 0.162, 0.06, 0.9, back, 0.8, 1400, 786), shot=0):
            self.location = '公會基地'
        elif self.ImgExist((0.001, 0.162, 0.06, 0.9, chair, 0.8, 1400, 786), shot=0):
            self.location = '家裡'        
        elif not self.PixelExist((0.312,0.971, 0.318, 0.985, '0xFFFFFF',0),shot=shot): # channel
            self.location = '公會狩獵地圖'
        else:
            self.location = '一般地圖'
    def check_economic(self, shot=1):
        if shot:
            self.screenshot()
        _, _, w, h, = self.getWindowRect()
        c_x1, c_y1, c_x2, c_y2 = 0.89, 0.04, 0.97, 0.19
        img_sub = self.img[int(c_y1*h):(int(c_y2*h)+1), int(c_x1*w):(int(c_x2*w)+1),]
        rgb = img_sub[1, 1, :]
        return np.max(np.sum(abs(img_sub-rgb),axis=2))<10
    def check_pause(self, shot=1):
        if shot:
            self.screenshot()
        return self.PixelExist(color_pause) and self.PixelExist((0.895, 0.056, '0xe8a346'))
    def check_home_screen(self, shot=1):
        if shot:
            self.screenshot()
        E1 = self.PixelExist(color_info=color_redblood,  img=self.img) 
        E2 = self.PixelExist(color_info=color_graycross, img=self.img) 
        E3 = self.PixelExist(color_info=color_whitebell, img=self.img) 
        return( E1 and (not E2) and E3 )
    def check_map_position(self, shot=1):
        if shot:
            self.screenshot()
        while not self.PixelExist(color_graycross):
            self.myclick((900/960, 200/540), delay=0.5, msg='打開地圖')
        while True:            
            posi = self.ImgExist((0.584, 0.106, 0.999, 0.842, mapposition, 0.1, 1400, 786), pos=1)
            if self.PixelExist((posi[1], posi[2]-0.01, posi[1], posi[2]-0.01, '0xFFFFFF',0)):
                break
        return (posi[1], posi[2])
        
    def BossExist(self, img=None):
        if type(img)==type(None):
            self.screenshot()
            img = self.img
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img_gray.shape
        E1 = E2 = (0,0,0)
        #for scale in np.linspace(0.5, 1.4, 20)[::-1]:
        for scale in np.linspace(0.7, 1.3, 8)[::-1]:
            E1_s = ImgSearch(icon_lwgray, img_gray, threshold=0.8, x_scale=w/1322*scale, y_scale=h/742*scale, pos=1)
            E2_s = ImgSearch(icon_rwgray, img_gray, threshold=0.8, x_scale=w/1322*scale, y_scale=h/742*scale, pos=1)
            if E1_s[0]>E1[0]:
                E1 = E1_s
            if E2_s[0]>E2[0]:
                E2 = E2_s
            if E1[0]>0.8 or E2[0]>0.8: # early stop
                print('scale = '+str(scale))
                break
        if E1[0]>0.8 and E2[0]>0.8:
            x, y = (E1[1]+E2[1])/2/w, (E1[2]+E2[2])/2/h
        elif E1[0]>0.8:
            x, y = E1[1]/w+0.1, E1[2]/h
        elif E2[0]>0.8:
            x, y = E2[1]/w-0.09, E2[2]/h
        else:
            self.boss_status = max(0, self.boss_status-1)
            print('沒有發現王: '+str(self.boss_status))
            return 0, 0

        # if boss exist
        self.boss_status = self.boss_status_max
        print('王的位置在 ('+str(round(x,3))+','+ str(round(y+0.14,3))+')')
        return x, y+0.14   
    def waitloading(self, timemax=120):
        if self.title!='Moonlight_Global':
            timemax = 120
        t_start=time.time()
        t_print=0
        while not self.check_loading(): # 等待進入loading
            if time.time()-t_print>1:
                print('等待進入loading...')
                t_print = time.time()
            if time.time()-t_start>timemax:
                raise ValueError('執行超時-waitloding')
            time.sleep(0.1)

        time.sleep(3)        
        while self.check_loading(): # 等待離開loading
            if time.time()-t_print>1:
                print('等待結束loading...')
                t_print = time.time()
            if time.time()-t_start>timemax:
                raise ValueError('執行超時-waitloding')
            time.sleep(0.1)
        time.sleep(2)   
     
        
    ###########################
    ### debugging and tools ###
    ###########################
    def is_WinActive(self):
        if self.title == 'Moonlight_Global':
            return(self.hwnd==win32gui.GetForegroundWindow())
        else:
            return(self.hwnd0==win32gui.GetForegroundWindow())    
    def resizeWindow(self):
        self.checkerror()
        
        if 'UnityWndClass' in win32gui.GetClassName(self.hwnd):
            w_target, h_target = 1400, 786
        elif 'LDPlayer' in win32gui.GetClassName(self.hwnd0):
            w_target, h_target = 1402, 824
        elif 'WindowOwnDCIcon' in win32gui.GetClassName(self.hwnd0):
            w_target, h_target = 1402, 822
        elif 'Qt5QWindowIcon' in win32gui.GetClassName(self.hwnd0):
            w_target, h_target = 1418, 821

        if self.character_id!='Moonlight_Global':    
            self.hwnd = self.hwnd0
            _, _, w, h = self.getWindowRect()
            if (w-2)/(h-36)>1.8 and 'LDPlayer' in win32gui.GetClassName(self.hwnd0):
                self.myclick((0.99,0.03), delay=0.2)
        x, y, w, h = self.getWindowRect()
        X, Y = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        y0 = y
        if x>X:
            x0 = x-X
        else:
            x0 = x       
        x0 = min(X-w_target, x0)
        y0 = min(Y-(h_target+100), y0)        
        if x>X:
            x0 = x0+X        
        if w==w_target and x0+w_target<X and y0+(h_target+100)<Y:
            if self.character_id!='Moonlight_Global':    
                self.hwnd = self.hwnd1
            return
        c0, c1, c2, c3 = self.calibration
        win32gui.MoveWindow(self.hwnd, x0-c0, y0-c1, w_target+c0-c2, h_target+c1-c3, True)
        if self.character_id!='Moonlight_Global':
            self.hwnd = self.hwnd1
        time.sleep(0.01)
    def getPosition(self, output=1):
        x0, y0 = win32gui.GetCursorPos()
        x1, y1, w, h = self.getWindowRect()
        if 0<x0-x1 and x0-x1<w and 0<y0-y1 and y0-y1<h:
            self.screenshot()
            rgb = self.img[y0-y1, x0-x1,]
            x, y, color = round((x0-x1)/w,3), round((y0-y1)/h,3), rgb_to_hex(tuple(rgb))
            if output==1:
                print( 'key=('+str(x)+', '+str(y)+'), color_info=\''+ str(color)+'\'' )
            else:
                print( '('+str(x)+', '+ str(y)+', \''+str(color)+'\')' )
        else:
            x, y = round((x0-x1)/w,3), round((y0-y1)/h,3)
            if output==1:               
                print( 'key=('+str(x)+', '+str(y)+')' )
            else:
                print( '('+str(x)+', '+ str(y)+')' )
    def check_WindowRect(self, vertex = 1):
        rect = self.getWindowRect()
        if vertex:
            win32api.SetCursorPos((rect[0],rect[1]))
        else:
            win32api.SetCursorPos((rect[0]+rect[2],rect[1]+rect[3]))
    
    def gameloop(self, once=False):
        while True:
            try:
                os.system('cls')
                self.print_setup()
                self.idle_fight()
                self.home_screen()
                self.teamup()
                self.cutweight()     # 賣雜物
                self.auction()       # 交易所
                self.get_reward()    # 每日禮物
                self.coinstore()     # 金幣商店
                self.daily_raid()    # 每日副本
                self.normal_raid()   # 突襲副本
                self.guild_hunt()    # 每日狩獵
                self.leave_guild_to_normal()   # 離開公會
                self.pvp()           # 自動打PVP
                self.economic()            
                time.sleep(1)
                if once:
                    return
            except Exception as e:
                print('exception:')
                print(e)                
                time.sleep(1)
    def fishingloop(self, once=False):
        while True:
            try:
                while True:
                    prt = 0
                    tic1 = time.time()
                    while self.PixelExist( (0.46,0.542,0.46,0.55,'0xD5D827',0) ):
                        if not prt:
                            print("wait", end=' ')
                            prt = 1
                    print(round(time.time()-tic1,3))
                    tic = time.time()
                    time.sleep(1.8)
                    while not self.PixelExist( (0.46,0.55,0.46,0.55,'0xD5D827',0) ):
                        self.send('{F1}',delay=0.1)
                        self.myclick((0.5,0.524),delay=0.1)
                        
                    print(round(time.time()-tic,3))
            except Exception as e:
                print('exception:')
                print(e)                
                time.sleep(1)

                


# 格式: 傳點(mx, my), 王點(f, fy), 子區(subregion), "區(region)" 
MAP = {
"席倫": (628/960, 111/540,  31/960, 195/540),
"拉賈": (853/960, 122/540, 788/960, 155/540),
"沙漠掠奪者": (691/960, 170/540, 769/960, 266/540),
"范霍克": (731/960, 152/540, 890/960, 214/540),
"吉拉隆": (787/960, 341/540, 609/960, 303/540),
"大蟑螂": (820/960, 321/540, 847/960, 233/540),
"巴風特": (776/960, 256/540, 890/960, 221/540),
"獨眼巨人": (620/960, 341/540, 659/960, 288/540),
"獅鳩": (677/960, 228/540, 641/960, 292/540),
"巴古德": (610/960, 360/540, 642/960, 260/540),
"夏魯卡": (820/960, 118/540, 758/960, 217/540),
"戴貝克": (840/960, 120/540, 903/960, 144/540),
"阿格瑪": (651/960, 407/540, 697/960, 150/540),
"北巴": (771/960, 135/540, 783/960, 192/540),
"卡勒修": (771/960, 214/540, 910/960, 172/540, '勒加斯郊區', '布里頓聯盟'),
"阿格瑪": (0.679, 0.752, 0.725, 0.259, "孤寂的洞窟", "莫拉塔"), 
"卡翠娜": (0.704, 0.306, 0.727, 0.261, "莫拉塔冰牆", "莫拉塔"), 
"格林姆迦爾": (0.656, 0.454, 0.676, 0.686, "莫拉塔山入口", "莫拉塔"),
"芬里爾": (0.839, 0.545, 0.930, 0.339, "迷霧森林", "莫拉塔"),
"伊克利普斯": (0.755, 0.46, 0.858, 0.285, "冰霜葉片平原", "莫拉塔"),
"史凱拉女王": (0.695, 0.364, 0.641, 0.217, "瓦爾納藏身處", "莫拉塔"),
"路卡": (0.835, 0.731, 0.948, 0.648, "瓦爾納河口", "莫拉塔"),
"塔羅夫": (0.677, 0.341, 0.665, 0.346, "瓦爾納河口", "莫拉塔")
}

SUBREGION = {
'勒加斯郊區': (0.77, 0.692),
'冰霜葉片平原': (0.79, 0.294),
'迷霧森林': (0.696, 0.405),
'莫拉塔山入口': (0.82, 0.466),
'莫拉塔冰牆': (0.909, 0.423),
'瓦爾納藏身處':(0.768, 0.601),
'孤寂的洞窟':(0.89, 0.595),
'瓦爾納非法地帶':(0.691, 0.756),
'瓦爾納河口':(0.778, 0.719),
'流浪民溫泉帶':(0.784, 0.518)
}
REGION ={
"尼普爾海姆遺址": (0.755, 0.246),
"莫拉塔": (0.802, 0.209),
"布里頓聯盟": (0.789, 0.451),
"巴洛克山脈": (0.837, 0.482),
"拉比亞斯": (0.8, 0.584),
"塞拉堡": (0.851, 0.572)    
}


class key_info():
    def __init__(self, key=(0,0), delay=delay, keywait=0.3, keep=False, timemax1=10, dofirst=True, msg='', 
                icon_info=None, color_info=None, least=0.1, tf=True, timemax2=delay, 
                mode=None):
        self.key = key
        self.delay = delay
        self.keywait = keywait
        self.keep = keep
        self.timemax1 = timemax1
        self.dofirst = dofirst
        self.msg = msg
        self.icon_info = icon_info
        self.color_info = color_info
        if color_info!=None and type(color_info[0])==str:
            if type(color_info)==str:
                if type(key)==str:
                    raise ValueError("please give color_info position")
                else:
                    self.color_info = (key[0], key[1], color_info)
        self.least = least
        self.tf = tf
        self.timemax2 = timemax2
        if type(mode)==int:
            if mode>2: # wait disappear
                self.tf= False
            else:
                self.tf= True
            if mode==2 or mode==4: # keep clicking
                self.keep=True
            else:
                self.keep=False


os.system('chcp 936')
epeffect = cv2.imread('figures\\epeffect_1400x786.png')
hp30potion = cv2.imread('figures\\hp30potion_1400x786.png')
hp20potion = cv2.imread('figures\\hp20potion_1400x786.png')
speedpotion = cv2.imread('figures\\speedpotion_1400x786.png')
enapotion = cv2.imread('figures\\enapotion_1400x786.png')
knockout = cv2.imread('figures\\knockout_1400x786.png')
back = cv2.imread('figures\\back_1400x786.png')
chair = cv2.imread('figures\\chair_1400x786.png')
pageone = cv2.imread('figures\\pageone_1400x786.png')
pagetwo = cv2.imread('figures\\pagetwo_1400x786.png')
change1 = cv2.imread('figures\\change1_1400x786.png')
change2 = cv2.imread('figures\\change2_1400x786.png')
change3 = cv2.imread('figures\\change3_1400x786.png')
auto = cv2.imread('figures\\auto_1400x786.png')
semi = cv2.imread('figures\\semi_1400x786.png')
mapposition = cv2.imread('figures\\mapposition_1400x786.png')
raidend = cv2.imread('figures\\raidend_1400x786.png')
countdown2 = cv2.imread('figures\\countdown2_1400x786.png')
login_conflict = cv2.imread('figures\\login_conflict_1400x786.png')
loading = cv2.imread('figures\\loading_1400x786.png')
icon_burn = cv2.imread('figures\\icon_burn_1919x1015.jpg')
icon_poison = cv2.imread('figures\\icon_poison_1600x900.png')
icon_guild = cv2.imread('figures\\icon_guild_1400x786.png')
icon_rw = cv2.imread('figures\\icon_rightwing_1322x742.png')
icon_lw = cv2.imread('figures\\icon_leftwing_1322x742.png')
icon_lwgray = cv2.cvtColor(icon_lw,cv2.COLOR_BGR2GRAY) # 1322x742
icon_rwgray = cv2.cvtColor(icon_rw,cv2.COLOR_BGR2GRAY) # 1322x742
password_teamup2 = cv2.imread('figures\\password_teamup2_1400x786.png') # 0.95
bag_full = cv2.imread('figures\\bag_full_1135x637.png') # 1135x637
merchant = cv2.imread('figures\\merchant_1400x786.png') # 1135x637
merchant2 = cv2.imread('figures\\merchant2F_1400x786.png')
merchant3 = cv2.imread('figures\\merchant3F_1400x786.png')
merchant4 = cv2.imread('figures\\merchant4F_1400x786.png')
merchant5 = cv2.imread('figures\\merchant5F_1400x786.png')

achieve_level = cv2.imread('figures\\achieve_level_1400x786.png')



color_fight = [0.268, 0.912, 0.274, 0.933, '0xFFFFFF', 0]
color_graycross = [0.981, 0.05, 0.981, 0.05, '0x6B6152', 5]
color_graycross2 = [0.6, 0.05, '0x6B6152', 5]
color_blueconfirm=[0.57, 0.595, '0xD6DA29', 10]
color_redblood=[0.082, 0.016, 0.102, 0.04,"0x6E44F3", 5]
color_whitebell=[0.695, 0.071, 0.696, 0.071, '0xFFFFFF', 0]
color_pause=[0.695,0.071,0.696,0.071, '0xD4D827',-3] # bluebell
color_logout = [0.939, 0.929, 0.939, 0.929, '0xd6d726']
icon_loading = (0.470, 0.460, 0.530, 0.510, loading, 0.85, 1400, 786)
