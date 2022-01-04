#!/usr/bin/python
#####pyinstaller -F --version-file=YTDLInfo.py YTDL_GUI_merge.py
#####https://pixnashpython.pixnet.net/blog/post/28052204-%E3%80%90pyinstaller%E3%80%91%E7%94%A8pyinstaller%E4%B9%BE%E6%B7%A8%E4%BF%90%E8%90%BD%E6%89%93%E5%8C%85%E4%BD%A0%E7%9A%84.py
###Unicode Type : gb18030  # -*- coding: utf-8 -*-


## 油管剽竊大師 [Ver 0.2.1]  -尚未優化
def call_var(call,Ue="儲存時錯誤",u="儲存時錯誤",re="儲存時錯誤",ar="儲存時錯誤",Li="儲存時錯誤",fileob="儲存時錯誤",down="儲存時錯誤",filein="儲存時錯誤",inpe="儲存時錯誤",inputl="儲存時錯誤",DLnu="儲存時錯誤",isL="儲存時錯誤",vid="儲存時錯誤",NeedVar=0):
    global url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos
    varList = [url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos] #0~12
    if call == 1 :
        print("load_var")
        check_var(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
        return varList[NeedVar]
    if call == 0 :
        print("save_var")
        url_error=Ue
        url=u
        res=re
        args=ar
        List_END=Li
        fileobj=fileob
        download_count=down
        file_index=filein
        input_error=inpe
        input_limit=inputl
        DL_num=DLnu
        isList=isL
        videos=vid
        check_var(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
        return

def check_var (url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList="無", videos="無"):
    p("-----------------------check-----------------------")
    p(("url_error :",url_error))
    p(("url :",url))
    p(("res :",res))
    p(("args :",args))
    p(("List_END :",List_END))
    p(("fileobj :",fileobj))
    p(("download_count :",download_count))
    p(("file_index :",file_index))
    p(("input_error :",input_error))
    p(("input_limit :",input_limit))
    p(("DL_num :",DL_num))
    p(("isList :",isList))
    p(("videos :",videos))
    p("---------------------------------------------------")


def backup_TXT() :
    print("備份 : !/usr/bin/python")
def p(txt):
    if debug == 1 :
        print(txt)


#導入模組
import os
print('檢查必要套件，缺少時將嘗試自動進行安裝。')
os.system('pip install -r requirements.txt | find /V "already satisfied"')
from time import sleep
import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, END, EXTENDED, LEFT, RIGHT, TOP
import argparse
import platform
from pytube import YouTube
from pytube import Playlist
import subprocess
import threading
import tkinter.messagebox as msg


### - 初始化
url_error = 0
url = ""
res = ""
args = {}
List_END = 0
fileobj = {}
download_count = 0
file_index = 0
input_error = 0
input_limit = []
DL_num = 0
folder_path = "未實裝"
### - GUI初始化
win = tk.Tk()
win.title('YT影片下載器')
win.geometry('800x480')
win.resizable(False, False) #關起來了,拉來拉去只會更醜
win.iconphoto(True, tk.PhotoImage(file='./PlunderMaster.png'))
btnstr = tk.StringVar()
# win.rowconfigure(1, weight=1)
# win.columnconfigure(1, weight=1)

### - 多線程
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

def setting_read():
    global folder_path
    try:
        f = open("setting.json","r")
        print("找到setting")
        
    except FileNotFoundError:
        print ("沒找到檔案")
        print ("第一次運行\"setting.json\"")
        f = open("setting.json","w+") #不知道為啥這功能可寫讀,但好像讀出...空氣?
        f.write("""[folder_path]:[]""")
    except PermissionError:
        print ("你沒有權限訪問該檔案")
        exit()
    
    folder_path = "不打算實裝了"

#################################
#debug 1 = true
debug = 0
#################################



for i in range(0, 9):
    input_limit.append(i+1)
p(input_limit)
p(range(0,input_limit[-1]))
res_Label = [144,240,360,480,720,1080,1440,2160,4320]
ask_txt = """--------------------------------------
1) 144p
2) 240p
3) 360p
4) 480p
5) 720p
6)1080p
7)1440p
8)2160p
9)4320p
--------------------------------------
請輸入欲下載的解析度 :\r"""

#YTDL_main
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
def pyTube_folder():
    sys = platform.system()
    home = os.path.expanduser('~')

    if sys == 'Windows':
        folder = os.path.join(home, 'Videos', 'PyTube')
    elif sys == 'Darwin':
        folder = os.path.join(home, 'Movies', 'PyTube')

    if not os.path.isdir(folder):  # 若'PyTube'資料夾不存在…
        os.mkdir(folder)        # 則新增資料夾

    return folder


def onProgress(stream, chunk, remains):
    total = stream.filesize
    percent = (total-remains) / total * 100
    # NOWDL_name = fileobj['name'].strip().replace(".mp4"," ")
    # DLing_info.set(' [ ',NOWDL_name,' ] ','下載中… {:05.2f}%'.format(percent), end='\r')
    DLing_info.set('下載中… {:05.2f}%'.format(percent))
    print('下載中… {:05.2f}%'.format(percent), end='\r')

# 列舉可用的解析度
def video_res(yt):
    res_set = set()
    video_list = yt.streams.filter(type="video")
    for v in video_list:
        res_set.add(v.resolution)

    # 傳回解析度表列，例如：['720p', '480p', '360p', '240p', '144p']
    return sorted(res_set, reverse=True, key=lambda s: int(s[:-1]))


def download_media(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos):
    global RE_res_str
    # check_var(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
    try:
        yt = YouTube(args.url, on_progress_callback=onProgress,
                    on_complete_callback=onComplete)
    except Exception as error:
        p(error)
        print('下載影片時發生錯誤，請確認網路連線和YouTube網址無誤。')
        return

    filter = yt.streams.filter
    p(filter)

    if args.a:  # 只下載聲音
        target = filter(type="audio").first()
    elif args.debug:
        target = filter(type="video", resolution="999999p").first()
    elif args.e_k:
        target = filter(type="video", resolution="4320p").first()
    elif args.f_k:
        target = filter(type="video", resolution="2160p").first()
    elif args.t_k:
        target = filter(type="video", resolution="1440p").first()
    elif args.fhd:
        target = filter(type="video", resolution="1080p").first()
    elif args.hd:
        target = filter(type="video", resolution="720p").first()
    elif args.sd:
        target = filter(type="video", resolution="480p").first()
    elif args.res360:
        target = filter(type="video", resolution="360p").first()
    elif args.res240:
        target = filter(type="video", resolution="240p").first()
    elif args.res144:
        target = filter(type="video", resolution="144p").first()
    else:
        target = filter(type="video").first()

    if target is None:
        print('沒有您指定的解析度，可用的解析度如下：')
        res_list = video_res(yt)
        # res_list = reversed(res_list)
        print(type(res_list))
        print("res_list :",res_list)
        for i, res in enumerate(reversed(res_list)):
            print('{}) {}'.format(i+1, res))   # {} 這個東西放在裡面,配合enumerate(res_list) 可以把for 的值 in  放到{}裡面,順序看  format裡面怎麼設定
            # os.system('res_{}.config(state=tk.NORMAL)'.format(i+1)) #好可惜,不知道這想法有沒有搞頭?
            if i+1 == 1 :res_1.config(state=tk.NORMAL)
            if i+1 == 2 :res_2.config(state=tk.NORMAL)
            if i+1 == 3 :res_3.config(state=tk.NORMAL)
            if i+1 == 4 :res_4.config(state=tk.NORMAL)
            if i+1 == 5 :res_5.config(state=tk.NORMAL)
            if i+1 == 6 :res_6.config(state=tk.NORMAL)
            if i+1 == 7 :res_7.config(state=tk.NORMAL)
            if i+1 == 8 :res_8.config(state=tk.NORMAL)
            if i+1 == 9 :res_9.config(state=tk.NORMAL)
            input_limit = i+1
            
        RE_res_str = None
        # res_str = None
        # val = input('請選擇（預設{}）：'.format(res_list[0]))
        #thread_it
        while True :
            
            try :
                val = RE_res_str
                call_RE_res(input_limit)
                p("val :",val)
            except :
                # val = RE_res()
                p(("沒抓到val :",val))
                if val != None : break
                sleep(1)
        try:
            trun = input_limit
            for a in range(0,input_limit[-1]):
                if int(val) == input_limit :
                    reversed(trun)
                    val = trun[len(a)]
            print('val :',val)
            res = res_list[int(val)-1]
        except:
            res = res_list[0]

        print('您選擇的是 {} 。'.format(res))
        target = filter(type="video", resolution=res).first()

    # 開始下載
    target.download(output_path=pyTube_folder())


def check_media(filename):
    out = subprocess.run(["ffprobe", filename],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if (out.stdout.decode('utf-8').rfind('Audio') == -1):
        return -1  # 沒有聲音
    else:
        return 1


def merge_media(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos):
    vars(args)['a'] = False
    temp_video = os.path.join(fileobj['dir'], 'temp_video.mp4')
    temp_audio = os.path.join(fileobj['dir'], 'temp_audio.mp4')
    temp_output = os.path.join(fileobj['dir'], 'output.mp4')
    search_path = os.path.dirname(__file__)
    cmd = f'{search_path}\\ffmpeg\\bin\\ffmpeg -i {temp_video} -i {temp_audio} \
        -map 0:v -map 1:a -c copy -y {temp_output}'

    try:
        subprocess.run(cmd, shell=True)
        # 視訊檔重新命名
        os.rename(temp_output, os.path.join(fileobj['dir'], fileobj['name']))
        os.remove(temp_audio)
        os.remove(temp_video)
        DL_num +=1
        DL_List_num.insert(END, DL_num)
        DL_List_name.insert(END, fileobj['name'])
        DL_List_res.insert(END, (str(res_Label[int(res_var.get())-1])+"P"))
        print('視訊和聲音合併完成')
        if isList == 1 :
            check_urls(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
    except Exception as error:
        p(error)
        print('視訊和聲音合併失敗')


def onComplete(stream, file_path):
    # print(stream, file_path)
    # call_var(1)
    # check_var(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
    fileobj['name'] = os.path.basename(file_path)
    p(("fileobj['name'] :",fileobj['name']))
    fileobj['dir'] = os.path.dirname(file_path)
    p(("fileobj['dir'] :",fileobj['dir']))
    print('\r')
    print("download_count :","None")
    download_count = call_var(1,NeedVar=6)
    print("download_count :",download_count)
    if download_count == 1:
        if check_media(file_path) == -1:
            print('此影片沒有聲音')
            download_count += 1
            try:
                # 視訊檔重新命名
                os.rename(file_path, os.path.join(
                    fileobj['dir'], 'temp_video.mp4'))
            except:
                print('視訊檔重新命名失敗')
                return

            print('準備下載聲音檔')
            vars(args)['a'] = True  # 設定成a參數
            call_var(0,url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
            download_media(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)    # 下載聲音
        else:
            print('此影片有聲音，下載完畢！')
            if isList == 1 :
                check_urls(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
    else:
        try:
            # 聲音檔重新命名
            os.rename(file_path, os.path.join(
                fileobj['dir'], 'temp_audio.mp4'))
        except:
            print("聲音檔重新命名失敗")
        # 合併聲音檔
        p("進入merge_media")
        merge_media(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)

def TK_lock(TorF) :
    if TorF == 1 :
        DL_Button.config(state=tk.DISABLED)
        res_1.config(state=tk.DISABLED)
        res_2.config(state=tk.DISABLED)
        res_3.config(state=tk.DISABLED)
        res_4.config(state=tk.DISABLED)
        res_5.config(state=tk.DISABLED)
        res_6.config(state=tk.DISABLED)
        res_7.config(state=tk.DISABLED)
        res_8.config(state=tk.DISABLED)
        res_9.config(state=tk.DISABLED)
        txtbox_02.config(state=tk.DISABLED)
        DL_Button_txt.set('下載中')

    if TorF == 0 :
        DL_Button.config(state=tk.NORMAL)
        res_1.config(state=tk.NORMAL)
        res_2.config(state=tk.NORMAL)
        res_3.config(state=tk.NORMAL)
        res_4.config(state=tk.NORMAL)
        res_5.config(state=tk.NORMAL)
        res_6.config(state=tk.NORMAL)
        res_7.config(state=tk.NORMAL)
        res_8.config(state=tk.NORMAL)
        res_9.config(state=tk.NORMAL)
        txtbox_02.config(state=tk.NORMAL)
        DL_Button_txt.set('下載')
        DLing_info.set('下載完成')

def check_urls(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos):
    download_count = 1
    call_var(0,url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)

    if file_index < len(videos):
        vars(args)['url'] = videos[file_index]  # 設定成url參數
        file_index = file_index + 1
        print("下載影片：", vars(args)['url'])
        call_var(0,url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
        download_media(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
    if file_index == len(videos):
        TK_lock(0)
        

## 判斷下載
def YT_catcher(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList):
    parser = argparse.ArgumentParser()
    p(("(res==is debugmode?) :",(res=="debug")))
    parser.add_argument("url", nargs='?', default=url, help="指定YouTube視訊網址")    #← 幹!這個正解
    parser.add_argument("-a", action="store_true", help="僅下載聲音")
    parser.add_argument("-res144", default=(res=="1"), help="選擇普通（144P）畫質")
    parser.add_argument("-res240", default=(res=="2"), help="選擇普通（240P）畫質")
    parser.add_argument("-res360", default=(res=="3"), help="選擇普通（360P）畫質")
    parser.add_argument("-sd", default=(res=="4"), help="選擇普通（480P）畫質")
    parser.add_argument("-hd", default=(res=="5"), help="選擇HD（720P）畫質")
    parser.add_argument("-fhd", default=(res=="6"), help="選擇Full HD（1080P）畫質")
    parser.add_argument("-t_k", default=(res=="7"), help="選擇2K（1440p）畫質")
    parser.add_argument("-f_k", default=(res=="8"), help="選擇4K（2160P）畫質")
    parser.add_argument("-e_k", default=(res=="9"), help="選擇8K（4320P）畫質")
    parser.add_argument("-debug", default=(res=="debug"), help="debug使用")
    parser.add_argument("-end", default=List_END, help="影音清單下載數量(前幾個,2為前兩個影片)")

    args = parser.parse_args()
    print(args)

    p(("args: ",args))
    p(("url :",url))
    if isList == 1 :
        global videos
        try:
            pl = Playlist(url)

            if args.end:
                videos = pl.video_urls[:int(args.end)]
            else:
                videos = pl.video_urls
        except Exception as error:
            p(error)
            print('下載影片時發生錯誤，請確認網路連線和YouTube網址無誤。')
            return
        print("! 開始下載播放清單 !")
        p(("videos :",videos))
        check_urls(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList, videos)
    else :
        print("! 開始下載影片 !")
        
        download_media(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList)

###  整理網址
def YTDL_main(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num) :
    global isList
    input_TXT = ""
    get_ID = ""
    isList = 0

    input_TXT = url.strip().replace("?"," ").replace("&"," ").replace("="," ").split()
    p(("input_TXT :",input_TXT))
    input_TXT = list(input_TXT)
    if "list" in input_TXT :
        isList = 1
        p("進入list")
        get_ID = input_TXT[4]
        p(("get_ID :",get_ID))
        url = ("https://www.youtube.com/playlist?list="+get_ID)
        p(("url :",url))
        # while True :
        #     res = input(ask_txt)
        #     List_END = input("你要下載至清單中的第幾個,若不輸入則全下載 :\r")
        #     input_error = 0
        #     try :
        #         for i in range(0,input_limit[-1]) :
        #             p(i)
        #             if (i+1) == int(res) :
        #                 p(("i :",(i+1),'｜res :',res))
        #                 p(("i type :",type(i),'｜res type :',type(res)))
        #             if i == (input_limit[-1]-1) and input_limit[-1] < int(res):
        #                 p("input_error")
        #                 input_error = 1
        #             if input_error == 1 :
        #                 os.system('cls')
        #                 print("輸入錯誤")
        #                 print("只能填入",input_limit[0],"~",input_limit[-1],"!")
        #     except ValueError:
        #         os.system('cls')
        #         print("下載類型只能填入",input_limit[0],"~",input_limit[-1],"\n且必須為數字 !")
        #     p("--------------------------------------------------")
        #     p(res)
        #     p(List_END)
        #     p("--------------------------------------------------")
        #     try :
        #         int(res)
        #         int(List_END)
        #         if input_error == 0:
        #             break
        #     except ValueError:
        #         os.system('cls')
        #         print("下載播放清單數量僅能輸入數字")
    else:
        p("進入單影片")
        get_ID = input_TXT[2]
        p(("get_ID :",get_ID))
        url = ("https://www.youtube.com/watch?v="+get_ID)
        p(("url :",url))
        while True :
            res = res
            input_error = 0
            try :
                for i in range(0,input_limit[-1]) :
                    p(i)
                    if (i+1) == int(res) :
                        p(("i :",(i+1),'｜res :',res))
                        p(("i type :",type(i),'｜res type :',type(res)))
                    if i == (input_limit[-1]-1) and input_limit[-1] < int(res):
                        p("input_error")
                        input_error = 1
                    if input_error == 1 :
                        os.system('cls')
                        print("輸入錯誤")
                        print("只能填入",input_limit[0],"~",input_limit[-1],"!")
            except ValueError:
                os.system('cls')
                print("下載類型只能填入",input_limit[0],"~",input_limit[-1],"\n且必須為數字 !")
            p("--------------------------------------------------")
            p(res)
            p("--------------------------------------------------")
            if input_error == 0:
                    break

    # check_var(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList)
    YT_catcher(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num, isList)

####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
def List_num_check(key):
    data = listtxt.get()
    data = data.strip()
    p(data)
    p(len(data))
    print("List_num_check :"+str(len(data)))
    if len(data) <= 3: return
    print("1")
    listtxt.set(data[:3])
    
    p(type(listtxt.get()))
    data = listtxt.get()
    print(data) 


def List_singl(key) :
    p(key.char)
    check = urltxt.get().strip().replace("?"," ").replace("&"," ").replace("="," ").split()
    if "list" in check :
        txtbox_02.config(state=tk.NORMAL)
        p(check)
        p("1")
    else :
        txtbox_02.config(state=tk.DISABLED)
        p(check)
        p("2")

def Simple_check_YTURL(url):
    global url_error
    check_url = url.strip().replace("/"," ").replace("="," ").replace("?"," ").replace("&"," ").replace("="," ").split()
    if not "watch" in check_url and not "list" in check_url :
        url_error = 1
        print("不是YT網址")
    if "watch" in check_url or "list" in check_url :
        url_error = 0
        print("是YT")
    
def DL_url(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num):
    TK_lock(1)
    DL_Button.config(state=tk.DISABLED)
    DL_Button_txt.set('下載')
    List_END = listtxt.get()
    url = urltxt.get()
    res = res_var.get()
    Simple_check_YTURL(url)
    
    if url_error == 1 :
        tk.messagebox.showerror(title='錯誤', message='你輸入的不是Youtube網址！') 
        DL_Button.config(state=tk.NORMAL)
        DL_Button_txt.set('下載')
    if res == "0" :
        tk.messagebox.showerror(title='錯誤', message='你還沒有選擇要下載的畫質！') 
        DL_Button.config(state=tk.NORMAL)
        url_error = 1
    if url_error == 0 :
        DL_Button.config(state=tk.DISABLED)
        DL_Button_txt.set('下載中')
        p(url)
        p(res)
        p(List_END)
        YTDL_main(url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num)
    print(url_error)





### - 底色
#放在下載紀錄底左邊,為了讓表單有間隔
DLed_Area_Lside = tk.Frame(win, bg='#aba2a2', width=10)
DLed_Area_Lside.pack(side=LEFT, fill=BOTH)
DLed_Area_Rside = tk.Frame(win, bg='#aba2a2', width=10)
DLed_Area_Rside.pack(side=RIGHT, fill=BOTH)
DLed_Area_bot = tk.Frame(win, bg='#aba2a2', height=10)
DLed_Area_bot.pack(side=BOTTOM, fill=BOTH)
DLed_Area_top = tk.Frame(win, bg='#aba2a2', height=10)
DLed_Area_top.pack(side=TOP, fill=BOTH)

#網址區域底
fm_lbl = tk.Frame(win, bg='#FF9955', height=60)
fm_lbl.pack(side=tk.TOP,fill=tk.X)
Area_Line01 = tk.Frame(win, bg='black', height=2)
Area_Line01.pack(side=TOP, fill=BOTH)

#下載進度底
fm_cal = tk.Frame(win, bg='skyblue', height=60)
fm_cal.pack(side=tk.TOP,fill=tk.X,expand=False)
Area_Line02 = tk.Frame(win, bg='black', height=2)
Area_Line02.pack(side=TOP, fill=BOTH)

#下載紀錄底
DLed_Area01 = tk.Frame(win, bg='#8b358f', width=0, height=0)
DLed_Area01.pack(side=LEFT, fill=BOTH,expand=False)
DLed_Area02 = tk.Frame(DLed_Area01, bg='#484587', width=0, height=0)
DLed_Area02.pack(side=TOP, fill=BOTH, expand=False)
DLed_Area03 = tk.Frame(win, bg='#8074b8', width=10, height=25)
DLed_Area03.pack(side=BOTTOM, fill=tk.X, expand=False)
#畫質選擇區
DLed_Area04 = tk.Frame(win, bg='#5da17e', width=10, height=25)
DLed_Area04.pack(side=LEFT, fill=BOTH, expand=True)
#如果是LIST輸入下載量的區域
DLed_Area05 = tk.Frame(win, bg='#5ebbf9', width=200, height=25)
DLed_Area05.pack(side=BOTTOM, fill=BOTH, expand=True)
#存檔選擇區
DLed_Area06 = tk.Frame(win, bg='#aabd4f', width=200, height=25)
DLed_Area06.pack(side=BOTTOM, fill=BOTH, expand=True)

######### expand :是否要將剩下的空間區域都當作可擴張空間?    http://yhhuang1966.blogspot.com/2018/10/python-gui-tkinter_12.html
######### 範例 : text.py def EX01
### - 文字
#上方固定文字
lbl_01 = tk.Label(fm_lbl, bg='#858383', fg='black', 
               text='網址 :', font=('微軟正黑體', 11), 
               padx=10)
lbl_01.pack(side=LEFT)
#左邊列表,上方文字
lbl_02 = tk.Label(DLed_Area02, bg='#858383', fg='black', 
               justify='center', text='編號', font=('微軟正黑體', 11), 
               padx=3, relief="groove")
lbl_02.pack(side=LEFT)

lbl_03 = tk.Label(DLed_Area02, bg='#5e5e5e', fg='black', 
               justify='center', text='名稱', font=('微軟正黑體', 11), 
               padx=160, relief="groove")
lbl_03.pack(side=LEFT)

lbl_04 = tk.Label(DLed_Area02, bg='#858383', fg='black', 
               justify='center', text='畫質', font=('微軟正黑體', 11), 
               padx=28, relief="groove")
lbl_04.pack(side=LEFT)

#視窗右下一套的狀態表示
lbl_05_txt = tk.StringVar()
lbl_05_txt.set("目前狀態 :")
# lbl_05_txt.set("1234567")
lbl_05 = tk.Label(DLed_Area03, bg='#ffffff', fg='black', 
               justify='center', textvariable=lbl_05_txt, font=('微軟正黑體', 11), 
               padx=2, relief="groove")
lbl_05.pack(side=LEFT)

lbl_06_txt = tk.StringVar()
# lbl_06_txt.set("等待")
lbl_06_txt.set("未實裝")
lbl_06 = tk.Label(DLed_Area03, bg='#ffffff', fg='black', 
               justify='center', textvariable=lbl_06_txt, font=('微軟正黑體', 11),
               relief="groove")
lbl_06.pack(side=LEFT,fill=tk.X,expand=True)

#LIST下載字
None_Area01 = tk.Frame(DLed_Area05, bg='#ffffff', width=5, height=5)
None_Area01.pack(anchor=tk.NW,pady=10)

lbl_08 = tk.Label(DLed_Area05, bg='#ffffff', fg='black', 
               justify='center', text='未輸入則視為下載整個撥放清單', font=('微軟正黑體', 8), 
               padx=2)
lbl_08.pack(anchor=tk.NW,side=TOP)

lbl_07 = tk.Label(DLed_Area05, bg='#ffffff', fg='black', 
               justify='center', text='撥放清單下載數量 :', font=('微軟正黑體', 8), 
               padx=2)
lbl_07.pack(anchor=tk.NW,side=LEFT)




#中間籃底文字
DLing_info = tk.StringVar() # 初始化tk的字串變數
DLing_info.set('等待下載')
DLing_str = tk.Label(fm_cal, bd=3, bg='skyblue', fg='black', 
               justify='center', textvariable=DLing_info, font=('微軟正黑體', 11)
               )#'#375e5e'# side代表排版對齊時跟上個元件從哪個方向開始對齊
DLing_str.pack(side=TOP, expand=True) # padx/pady分別就是x方向跟y方向



### - 文字輸入
fm_ent = tk.Frame(fm_lbl, bg='#858383', width=1, height=1)
fm_ent.pack(side=LEFT)
urltxt = tk.StringVar(None, '')
txtbox_01 = tk.Entry(fm_ent, width=90, justify='left', textvariable=urltxt)
txtbox_01.bind("<KeyRelease>", List_singl)
txtbox_01.pack(side=LEFT)

listtxt = tk.StringVar()
listtxt.set('')
txtbox_02 = tk.Entry(DLed_Area05, width=5, justify='center', textvariable=listtxt)
txtbox_02.bind("<KeyRelease>", List_num_check)
txtbox_02.pack(anchor=tk.NW, side=LEFT)


txtbox_02.config(state=tk.DISABLED)

### - 按鈕
#下載紐 - 同時是啟動點
DL_Button_txt = tk.StringVar()
DL_Button_txt.set("下載")
DL_Button = tk.Button(fm_lbl, bg="#e6e6e6", width=5, height=1, textvariable=DL_Button_txt, font=('微軟正黑體', 9), command=lambda :thread_it( DL_url, url_error, url, res, args, List_END, fileobj, download_count, file_index, input_error, input_limit, DL_num))
DL_Button.pack(side=LEFT, padx=5, pady=5)



### - 選擇畫質
res_var = tk.StringVar()
res_var.set("0")
show_your_select = tk.Label(DLed_Area04, width=12,text='尚未選擇')
show_your_select.pack(side=TOP)

def call_RE_res(input_limit):
    global RE_input_limit
    RE_input_limit = input_limit
    RE_res_Btn.pack(side=TOP, pady=10)
    RE_res_Btn_txt.set("重新選擇畫質")
    RE_res_Btn.config(state=tk.NORMAL)

def RE_res():
    global RE_res_str
    res_str = res_var.get()
    res_str = int(res_str)
    p(("RE_input_limit :",RE_input_limit))
    for i in range(0,RE_input_limit) :
        i += 1
        p((i,"and",res_str))
        if i == res_str :
            res_check = 1
        if i != res_str and i == RE_input_limit and res_check != 1:
            show_your_select.config(text="! 未知錯誤 !")
            tk.messagebox.showerror(title='錯誤', message='發生了未知的錯誤 !') 
    if res_check == 1 :
        show_your_select.config(text='你選擇 :' + str(res_Label[res_str-1]) + "P")
        RE_res_str = str(res_str)
        RE_res_Btn.pack_forget()

def select_res():
    res_check = 0
    res_str = res_var.get()
    res_str = int(res_str)
    p(input_limit)
    for i in range(0,input_limit[-1]) :
        i += 1
        p((i,"and",res_str))
        if i == res_str :
            res_check = 1
        if i != res_str and i == input_limit[-1] and res_check != 1:
            show_your_select.config(text="! 未知錯誤 !")
            tk.messagebox.showerror(title='錯誤', message='發生了未知的錯誤 !') 
    if res_check == 1 :
        show_your_select.config(text='你選擇 :' + str(res_Label[res_str-1]) + "P")
        res_str = str(res_str)

res_0 = tk.Radiobutton(win, text='未選擇', variable=res_var, value='0')

res_1 = tk.Radiobutton(DLed_Area04, text='144P', variable=res_var, value='1', command=select_res)
res_1.pack(side=TOP)

res_2 = tk.Radiobutton(DLed_Area04, text='240P', variable=res_var, value='2', command=select_res)
res_2.pack(side=TOP)

res_3 = tk.Radiobutton(DLed_Area04, text='360P', variable=res_var, value='3', command=select_res)
res_3.pack(side=TOP)

res_4 = tk.Radiobutton(DLed_Area04, text='480P', variable=res_var, value='4', command=select_res)
res_4.pack(side=TOP)

res_5 = tk.Radiobutton(DLed_Area04, text='720P', variable=res_var, value='5', command=select_res)
res_5.pack(side=TOP)

res_6 = tk.Radiobutton(DLed_Area04, text='1080P', variable=res_var, value='6', command=select_res)
res_6.pack(side=TOP)

res_7 = tk.Radiobutton(DLed_Area04, text='1440P', variable=res_var, value='7', command=select_res)
res_7.pack(side=TOP)

res_8 = tk.Radiobutton(DLed_Area04, text='2160P', variable=res_var, value='8', command=select_res)
res_8.pack(side=TOP)

res_9 = tk.Radiobutton(DLed_Area04, text='4320P', variable=res_var, value='9', command=select_res)
res_9.pack(side=TOP)

res_10 = tk.Radiobutton(DLed_Area04, text='debug', variable=res_var, value='10', command=select_res)
# res_10.pack(side=TOP)




#重新選擇畫質的按鈕
RE_res_Btn_txt = tk.StringVar()
RE_res_Btn_txt.set("-----")
# RE_res_Btn_txt.set("重新選擇畫質")
RE_res_Btn = tk.Button(DLed_Area04, bg="#e6e6e6", width=9, height=1, textvariable=RE_res_Btn_txt, font=('微軟正黑體', 8), command=RE_res) #
# RE_res_Btn.pack(side=TOP, pady=10)
# RE_res_Btn.config(state=tk.NORMAL)
# RE_res_Btn.pack_forget()
RE_res_Btn.config(state=tk.DISABLED)


### - 滾動軸,自己動時檢查其他軸的y是否相同,不等同時直接更改其他軸
# Scrollbar 表單右邊的拉把
Scrollbar = tk.Scrollbar(DLed_Area01, orient='vertical')
Scrollbar.pack(side=RIGHT, fill=tk.Y, expand=True)


def yscroll1(*args):
    if DL_List_num.yview != DL_List_res.yview or DL_List_name.yview != DL_List_res.yview :
        DL_List_num.yview_moveto(args[0])
        DL_List_name.yview_moveto(args[0])
    Scrollbar.set(*args)
def yscroll2(*args):
    if DL_List_res.yview != DL_List_num.yview or DL_List_name.yview != DL_List_num.yview :
        DL_List_res.yview_moveto(args[0])
        DL_List_name.yview_moveto(args[0])
    Scrollbar.set(*args)
def yscroll3(*args):
    if DL_List_res.yview != DL_List_name.yview or DL_List_num.yview != DL_List_name.yview :
        DL_List_res.yview_moveto(args[0])
        DL_List_num.yview_moveto(args[0])
    Scrollbar.set(*args)

### - 下載完成紀錄清單
# #能的話打算之後改w,h吃當前視窗大小

# NowDLres紀錄該影片下載的畫質
NowDLres = tk.StringVar()
NowDLres.set("")
DL_List_res = tk.Listbox(DLed_Area01, listvariable=NowDLres, width=10, yscrollcommand=yscroll1)
DL_List_res.pack(side=RIGHT, fill=tk.Y, expand=True)

#紀錄該影片是第幾個下載的
NowDL_num = tk.StringVar()
NowDL_num.set("")
DL_List_num = tk.Listbox(DLed_Area01, listvariable=NowDL_num, width=5, yscrollcommand=yscroll2)
DL_List_num.pack(side=LEFT, expand=True, fill=tk.Y)

#紀錄影片名稱
NowDLName = tk.StringVar()
NowDLName.set("")
DL_List_name = tk.Listbox(DLed_Area01, listvariable=NowDLName, width=50, yscrollcommand=yscroll3)
DL_List_name.pack(side=LEFT, expand=True, fill=tk.Y)

Scrollbar.config(command=DL_List_name.yview)

# ### - 測試
###備註
# 可能是forGUI跟原本的module用錯了YT_DL
# ==靠邀,現在下載影片是能了拉,但會沒辦法邊載視窗邊看阿,會沒回應
# 合併失敗?,UTF-8才是王道,沒可能      吧
# 
# 正在撥放的撥放清單:
# https://www.youtube.com/watch?v=0firv69LkgI&list=PLAo9RlHR2tDakgakxbOxT9dAZD0rpwvXQ&ab_channel=TowaCh.%E5%B8%B8%E9%97%87%E3%83%88%E3%83%AF
# 撥放清單:
# https://www.youtube.com/playlist?list=PLB8Nt5W7hnKA_pG2qljWbgVmJPobrLTm4
# 帳號推薦的合集網址:
# https://www.youtube.com/watch?v=MlGVqjjyeXc&list=RDMlGVqjjyeXc&start_radio=1&ab_channel=AU16
# 撥放中的撥放清單無法辨識與觀看單影片出現的合輯差別,要新增框框打勾來直接進入LIST


# #預計放 影片詳細資料,或下載總攬之類的


# #模擬下載紀錄
# insert_times = 0
# for x in range(100):
#     DL_List_res.insert(END, x)
#     DL_List_num.insert(END, x)
#     DL_List_name.insert(END, x)
#     insert_times += 1
# DL_List_res.insert(insert_times,)



win.mainloop()