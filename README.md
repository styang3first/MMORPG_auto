# MMORPG_auto_PC

## 腳本安裝與開啟 ##

安裝腳本方法:
0. 下載Python並且安裝: https://www.python.org/downloads/. 記得勾選add to path
1. 下載資料夾，解壓縮到C槽隨便一個位置
2. 點兩下"install.cmd"，然後等他跑完
3. 安裝完成

啟動腳本方法:
1. 要改設定的時候點兩下"Moonlight_PC.py"，點一下啟動腳本才會把設定存檔
2. 不需要改設定的話可以直接點兩下"script.py"
3. 跳出黑色視窗有跑腳本就成功了，第一次開黑色視窗記得要改:
    a. 右鍵點最左上角的圖示 -> 內容 -> 選項
    b. 把"快速編輯模式"取消掉 (不然腳本會被暫停)

##  使用須知 ##
- 腳本會直接一直把技能頁切回第一頁，所以常駐藥水/硬化劑/食物請放第一頁
- 暫停腳本有三種:
    a. 使用遊戲視窗中(視窗在最上層)，但是如果閒置電腦一分鐘以上腳本就會繼續跑
    b. 把遊戲視窗放到最大
    c. 把通知的鈴鐺點一下變藍色 (容易忘記點回白色，腳本就會一直暫停

##  腳本設定 ##
- 省電模式秒數30以下就不會觸發
- 勾選自動接受隊伍邀請的話，省電模式大於60秒則會直接變成60秒
- 勾選自動買金幣商店，會在凌晨0:10執行，不要買的東西請到figures/item_daily裡面把圖片刪掉
- 勾選自動領活動獎勵，會在凌晨5:00執行
- 公會狩獵位置(x, y)就是執行腳本後的"滑鼠位置". (先把滑鼠移動到你要打怪的點)
- 夥伴編號由左至右，由上至下，例如:
1   2   3   4   5
6   7   8   9   10
11 12   13  14  15

- 決鬥場的愛娜必須放在第二頁

Purposes and features of the gamebot:
I programmed a gamebot (link for codes) to execute tedious daily tasks in "M___l____ S____t__ ," an MMORPG game. With my gamebot, players do not waste their time doing daily routines, such as getting rewards, guild hunting, raids, and dungeons. The gamebot has the following features:
User interface: for users who do not know how to program to read and set up program parameters easily.
Background clicking and typing: allows users to keep using their computer or playing multiple characters (for "farming game items").
Automatical task executions : (1) resurrecting character, (2) accepting and sending team invitation, (3) exchange store shopping, (4) daily raid, (5) getting daily rewards, (6) daily coinstore shopping, (7) daily guild hunt, (8) timed dungeon, (9) daily arena.
The interface of my gamebot is presented below. The left panel shows the gamebot setting, and the right panel shows game information while running  the gamebot (No English version gamebot because all users speak Chinese): 

![image](https://github.com/styang3first/MMORPG_auto/assets/78116927/7ba5202c-ae44-47fc-83ab-9e3141ad8992)

## Main elements of the program: ##
I choose Python for building the gamebot because it has packages, such as cv2, scikit-learn, and sys, to help make decisions according to game images and execute system commands. More importantly, these packages help to apply machine learning techniques and train customized decision-making procedures. To build this gamebot, I need to:
- Use Python Tkinter: creates a clean user interface.
- Accomplish background screenshot: obtain real-time game image (OBS, a streaming application, also use this technique).
- Accomplish background mouse clicking: send mouse clicks to inactive game windows.
- Accomplish background mouse dragging: send mouse drags to inactive game windows.
- Accomplish background keyboard typing: send keyboard press to inactive game windows.
## Challenges: ##
1. The first challenge is that the gamebot has to be compatible with different desktops because users' desktops may lag occasionally or in different conditions. That is, time-gaps between each click should be adaptable but not constant. Therefore, I design the clicking function to possess the following features:
    - Click after conditions, such as "certain images are presented" or "certain pixel are disappeared," are satisfied.
    - Finish clicking until conditions are satisfied.
    - Click once or multiple times before the clicking function finishes.
After optimizing the clicking function, it turns out that the gamebot is more efficient and capable of dealing with unexpected errors.
2. Next, create decision-making procedures as conditions used in the clicking function. Because all decision-making procedures are based on the current gameplay screen, the gamebot has to decide whether pixels, icons, or objects are presented. According to my Statistics background, it is not hard to apply statistical models and machine learning skills to train my gamebot.
3. Last, design stable and structured workflows to run the gamebot. This makes it easier for me to organize and maintain the gamebot program and achieve "Don't Repeat Yourself (DRY)." More importantly, unexpected bugs occasionally interrupt gamebot workflows, so the designed workflows have to be capable of handling these bugs. I spend more time on this part because I have to test some functions over and over (while seeing what happens in the gameplay).
