def p(txt):
    print(txt)
## 油管剽竊大師 [Ver 0.1]
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
print('檢查必要套件，缺少時將嘗試自動進行安裝。')
os.system('pip install -r requirements.txt | find /V "already satisfied"')
import argparse
import platform
from pytube import YouTube
from pytube import Playlist
import subprocess

url = ""
res = ""
args = {}
List_END = 0
fileobj = {}
download_count = 1
file_index = 0

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
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if (out.stdout.decode('utf-8').rfind('Audio') == -1):
        return -1  # 沒有聲音
    else:
        return 1


def merge_media():
    vars(args)['a'] = False
    temp_video = os.path.join(fileobj['dir'], 'temp_video.mp4')
    temp_audio = os.path.join(fileobj['dir'], 'temp_audio.mp4')
    temp_output = os.path.join(fileobj['dir'], 'output.mp4')

    cmd = f'ffmpeg -i {temp_video} -i {temp_audio} \
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
    # p(("parser 1 :",parser))
    # url = url
    # print("url :",url)
    print("(res==test) :",(res=="debug"))
    parser.add_argument("url", nargs='?', default=url, help="指定YouTube視訊網址")    #← 幹!這個正解
    # parser.add_argument("list", help="該YouTube網址是否為撥放清單")
    # parser.add_argument("-sd", action="store_true", help="選擇普通（480P）畫質")
    # parser.add_argument("-hd", action="store_true", help="選擇HD（720P）畫質")
    # parser.add_argument("-fhd", action="store_true", help="選擇Full HD（1080P）畫質")
    # parser.add_argument("-a", action="store_true", help="僅下載聲音")
    parser.add_argument("-sd", default=(res=="480"), help="選擇普通（480P）畫質")
    parser.add_argument("-hd", default=(res=="720"), help="選擇HD（720P）畫質")
    parser.add_argument("-fhd", default=(res=="1080"), help="選擇Full HD（1080P）畫質")
    parser.add_argument("-t_k", default=(res=="1440"), help="選擇2K（1440p）畫質")
    parser.add_argument("-f_k", default=(res=="2160"), help="選擇4K（2160P）畫質")
    parser.add_argument("-e_k", default=(res=="4320"), help="選擇8K（4320P）畫質")
    parser.add_argument("-debug", default=(res=="debug"), help="debug使用")
    parser.add_argument("-a", default=(res=="S"), help="僅下載聲音")
    parser.add_argument("-end", default=List_END, help="影音清單下載數量(前幾個,2為前兩個影片)")

    args = parser.parse_args()
    
    print("args: ",args)
    print("url :",url)
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
        print("開始下載撥放清單")
        check_urls()
    if not "list" in url :
        print("開始下載影片")
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

    input_TXT = input("輸入網址 :").strip().replace("&"," ").replace("="," ").replace("?"," ").split()
    print("input_TXT :",input_TXT)
    if "list" in input_TXT :
        p("進入list")
        get_ID = input_TXT[2]
        print("get_ID :",get_ID)
        url = ("https://www.youtube.com/playlist?list="+get_ID)
        print("url :",url)
        res = input("""--------------------------------------
僅下載聲音 : S
480p : 480
720p : 720
1080p: 1080
1440p: 2k
2160p: 4k
4320p: 8k
--------------------------------------
請輸入欲下載的解析度 :""")
        List_END = input("你要下載至清單中的第幾個,若不輸入則全下載 :")
    else:
        p("進入單影片")
        get_ID = input_TXT[2]
        print("get_ID :",get_ID)
        url = ("https://www.youtube.com/watch?v="+get_ID)
        print("url :",url)
        res = input("""--------------------------------------
僅下載聲音 : S
480p : 480
720p : 720
1080p: 1080
1440p: 2k
2160p: 4k
4320p: 8k
--------------------------------------
請輸入欲下載的解析度 :""")
    main()