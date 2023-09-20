try:
    exec(open('function_PC.py',encoding="utf-8").read())
except:
    exec(open('function_PC.py').read())
if is_admin():
    try:
        self=Game_obj(title='Moonlight_Global')
        self.fishingloop()
    except Exception as e:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')                
        print(e)
        time.sleep(10)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

