import pyautogui
import pyperclip

try:
    exec(open('function_PC.py',encoding="utf-8").read())
except:
    exec(open('function_PC.py').read())

class LINE_obj:
    def __init__(self, title):
        def windowEnumerationHandler(hwnd, top_windows):
            if  title in win32gui.GetWindowText(hwnd):
                top_windows.append(hwnd)
        hwnd_lst = []  # all open windows
        win32gui.EnumWindows(windowEnumerationHandler, hwnd_lst)
        self.hwnd = hwnd_lst[0]
    def notify(self, notify='individual', floor=None):
        try:
            while abs(win32api.GetKeyState(0x11))>1 or abs(win32api.GetKeyState(0x10))>1:
                pass            
            ok = windll.user32.BlockInput(True) #block input
            time.sleep(0.2)
            try:
                win32gui.SetForegroundWindow(self.hwnd)
            except:
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(self.hwnd)
            time.sleep(0.5)
            t_now = clock2()
            hl, ml = t_now//60, t_now%60
            hu, mu = (t_now+30)//60, (t_now+30)%60
            time_period = str(hl) + [':0',':'][int(ml>=10)] +str(ml) + ' - '+str(hu) + [':0',':'][int(mu>=10)] +str(mu)
            

            _, _, w, h = self.getWindowRect()
            self.click([w-10,h-60], delay=0.25); time.sleep(0.1) # reset cursor
            pyperclip.copy(' 魔窟商人'+str(floor)+'F, '+time_period+
                           ' (不想被tag的時段(上班/睡覺)可以跟我說)'); time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v'); time.sleep(0.5)
            
            names = ['亞柏','William','柯志岳','Jye','謝阿原','廖偉翔','葉 承 毓', 'Mavis',
                     '周超','軒','Domain','PAUl','達聞西', 'yappy', '山下桑', '雯','蚊女', ['米樓', 2*60+0,18*60+0]]
            for name in names:
                if type(name) is str:
                    name, start, end = name, 0, 0        
                else: 
                    name, start, end = name
                if start<t_now and t_now<end:
                    continue
                win32gui.SetForegroundWindow(self.hwnd); time.sleep(0.1)
                self.click([w-10,h-60], delay=0.25); time.sleep(0.1) # reset cursor 
                pyautogui.typewrite(' @'); time.sleep(0.1)
                pyperclip.copy(name); time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'v'); time.sleep(0.5)
                self.click([50,h-140], delay=0.25) # select ppl
                    
            self.click([w-10,h-60], delay=0.25) # reset cursor
            pyautogui.press('enter') #按下enter鍵
        except Exception as e:
            print(e)
            print('Error: notify')
        ok = windll.user32.BlockInput(False) #block input
    def getWindowRect(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
        c1, c2, c3, c4 = 0,0,0,0
        x1, y1, x2, y2 = x1+c1, y1+c2, x2+c3, y2+c4
        w, h = x2 - x1, y2 - y1            
        return x1, y1, w, h
    def getPosition(self, output=1):
        x0, y0 = win32gui.GetCursorPos()
        x1, y1, w, h = self.getWindowRect()
        x, y = x0-x1, y0-y1
        print(x, y)        
    def click(self, key, delay=0.2):
        try:
            x, y = key
            lParam = win32api.MAKELONG(x, y)
            win32api.SendMessage(self.hwnd, win32con.WM_ACTIVATE, 2)
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, None, lParam)
        except Exception as e:
            print(e)
        return
            
self = Game_obj(initialize=False, first_hwnd=True)
i=0
if is_admin():
    while True:
        try:
            floor = self.check_merchant()
            print(floor)
            if floor>0:
                print('魔窟商人出現了!')
                i+=1
                # self.save_img('merchant'+str(i)+'.png', shot = False, plot=False)
                line = LINE_obj('月光公會群-夏沫')
                line.notify('individual', floor=floor)
                time.sleep(60*1)
            else:
                print('沒有訊息')
            time.sleep(2)        
        except Exception as e:
            print(e)
            self = Game_obj(initialize=False, first_hwnd=True)
            time.sleep(10)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


