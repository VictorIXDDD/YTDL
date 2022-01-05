#!/usr/bin/python
# -*- coding: utf-8 -*-
###Unicode Type : gb18030
## 油管剽竊大師 [Ver 0.2]  -尚未優化
def backup_TXT() :
    print("備份 : !/usr/bin/python")
def p(txt):
    if debug == 1 :
        print(txt)
import os

print('檢查必要套件，缺少時將嘗試自動進行安裝。')
os.system('pip install -r requirements.txt | find /V "already satisfied"')
import argparse
import platform
from pytube import YouTube
from pytube import Playlist
import subprocess

#################################
#debug 1 = true
debug = 1
#################################

url = ""
res = ""
args = {}
List_END = 0
fileobj = {}
download_count = 1
file_index = 0
input_error = 0
input_limit = []
for i in range(0, 9):
    input_limit.append(i+1)
p(input_limit)
p(range(0,input_limit[-1]))
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
請輸入欲下載的解析度 :"""


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
    print('下載中… {:05.2f}%'.format(percent), end='\r')

# 列舉可用的解析度


def video_res(yt):
    res_set = set()
    video_list = yt.streams.filter(type="video")
    for v in video_list:
        res_set.add(v.resolution)

    # 傳回解析度表列，例如：['720p', '480p', '360p', '240p', '144p']
    return sorted(res_set, reverse=True, key=lambda s: int(s[:-1]))


def download_media(args):
    try:
        yt = YouTube(args.url, on_progress_callback=onProgress,
                    on_complete_callback=onComplete)
    except:
        print('下載影片時發生錯誤，請確認網路連線和YouTube網址無誤。')
        return

    filter = yt.streams.filter

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

        for i, res in enumerate(res_list):
            print('{}) {}'.format(i+1, res))

        val = input('請選擇（預設{}）：'.format(res_list[0]))

        try:
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
    if (out.stdout.decode('utf-16').rfind('Audio') == -1):
        return -1  # 沒有聲音
    else:
        return 1


def merge_media():
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
        print('視訊和聲音合併完成')
        if isList == 1 :
            check_urls()
    except:
        print('視訊和聲音合併失敗')


def onComplete(stream, file_path):
    global download_count, fileobj
    # print("isList :",isList)
    fileobj['name'] = os.path.basename(file_path)
    fileobj['dir'] = os.path.dirname(file_path)
    print('\r')

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
            download_media(args)    # 下載聲音
        else:
            print('此影片有聲音，下載完畢！')
            if isList == 1 :
                check_urls()
    else:
        try:
            # 聲音檔重新命名
            os.rename(file_path, os.path.join(
                fileobj['dir'], 'temp_audio.mp4'))
        except:
            print("聲音檔重新命名失敗")
        # 合併聲音檔
        merge_media()
def check_urls():
    global args
    global file_index
    global download_count
    global isList
    download_count = 1

    if file_index < len(videos):
        vars(args)['url'] = videos[file_index]  # 設定成url參數
        file_index = file_index + 1
        print("下載影片：", vars(args)['url'])
        download_media(args)


def main():
    global videos
    global args
    global isList
    global url,res
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
    
    p(("args: ",args))
    p(("url :",url))
    if "list" in url :
        isList = 1
        try:
            pl = Playlist(url)

            if args.end:
                videos = pl.video_urls[:int(args.end)]
            else:
                videos = pl.video_urls
        except:
            print('下載影片時發生錯誤，請確認網路連線和YouTube網址無誤。')
            return
        print("! 開始下載播放清單 !")
        check_urls()
    if not "list" in url :
        print("! 開始下載影片 !")
        download_media(args)


if __name__ == '__main__':
    input_TXT = ""
    get_ID = ""
    isList = 0
    # url = " "+"https://www.youtube.com/watch?v=3cqV5BKJHyk&list=PLAo9RlHR2tDZwddeEyp9nTfpaFB58DrXd&ab_channel=SuiseiChannel"
    # print(("python "+os.path.basename(__file__)+url+" -fhd"))
    # print("cmd :",os.system("python "+os.path.basename(__file__)+url+" -fhd"))
### 使用說明
### 指令
### python Youtube_donwloader.py {下載需求,可多個} {網址}
###
### 使用撥放清單網址時https://www.youtube.com/watch?v=3cqV5BKJHyk&list=PLAo9RlHR2tDZwddeEyp9nTfpaFB58DrXd&ab_channel=SuiseiChannel
### 可以取  list= PLAo9RlHR2tDZwddeEyp9nTfpaFB58DrXd   這串ID的部分
### ID輸入進以下 https://www.youtube.com/playlist?list=ID
### 單影片可不要包含 &以後的部分↓
### https://www.youtube.com/watch?v=lv6FeylmJsk&ab_channel=%E3%83%A1%E3%82%AC%E3%83%86%E3%83%A9%E3%82%BC%E3%83%AD
### https://www.youtube.com/watch?v=W6a1C1ojzH0&ab_channel=USAO
### https://www.youtube.com/watch?v=W6a1C1ojzH0

### 各種YT url範例 :
### http://www.youtube.com/watch?v=-wtIMTCHWuI
### http://www.youtube.com/v/-wtIMTCHWuI?version=3&autohide=1
### https://m.youtube.com/watch?v=-wtIMTCHWuI&ab_channel=TechCrunch
### http://youtu.be/-wtIMTCHWuI
### https://www.youtube.com/embed/M7lc1UVf-VE
### http://www.youtube.com/attribution_link?a=JdfC0C9V6ZI&u=%2Fwatch%3Fv%3DEhxJLojIE_o%26feature%3Dshare
### https://www.youtube.com/attribution_link?a=8g8kPrPIi-ecwIsS&u=/watch%3Fv%3DyZv2daTWRZU%26feature%3Dem-uploademail
### 以下不明,但屬於YT
### http://s.ytimg.com/yt/favicon-wtIMTCHWuI.ico
### http://i2.ytimg.com/vi/-wtIMTCHWuI/hqdefault.jpg
### http://www.youtube.com/oembed?url=http%3A//www.youtube.com/watch?v%3D-wtIMTCHWuI&format=json

    input_TXT = input("輸入網址 :").strip().replace("?"," ").replace("&"," ").replace("="," ").split()
    p(("input_TXT :",input_TXT))
    input_TXT = list(input_TXT)
    if "list" in input_TXT :
        p("進入list")
        get_ID = input_TXT[4]
        p(("get_ID :",get_ID))
        url = ("https://www.youtube.com/playlist?list="+get_ID)
        p(("url :",url))
        while True :
            res = input(ask_txt)
            List_END = input("你要下載至清單中的第幾個,若不輸入則全下載 :")
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
                        # print("os.system('cls')")
                        print("輸入錯誤")
                        print("只能填入",input_limit[0],"~",input_limit[-1],"!")
            except ValueError:
                os.system('cls')
                # print("os.system('cls')")
                print("下載類型只能填入",input_limit[0],"~",input_limit[-1],"\n且必須為數字 !")
            p("--------------------------------------------------")
            p(res)
            p(List_END)
            p("--------------------------------------------------")
            try :
                int(res)
                int(List_END)
                if input_error == 0:
                    break
            except ValueError:
                os.system('cls')
                # print("os.system('cls')")
                print("下載播放清單數量僅能輸入數字")
    else:
        p("進入單影片")
        get_ID = input_TXT[2]
        p(("get_ID :",get_ID))
        url = ("https://www.youtube.com/watch?v="+get_ID)
        p(("url :",url))
        while True :
            res = input(ask_txt)
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
                        # print("os.system('cls')")
                        print("輸入錯誤")
                        print("只能填入",input_limit[0],"~",input_limit[-1],"!")
            except ValueError:
                os.system('cls')
                # print("os.system('cls')")
                print("下載類型只能填入",input_limit[0],"~",input_limit[-1],"\n且必須為數字 !")
            p("--------------------------------------------------")
            p(res)
            p("--------------------------------------------------")
            if input_error == 0:
                    break
    main()