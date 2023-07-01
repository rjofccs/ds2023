#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, arrow, subprocess, json, sqlite3, requests

# from youtube_transcript_api import YouTubeTranscriptApi
import webvtt


def upload(f):
    dfile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), "rb")
    url = "https://file.moringstars.com/upload"
    test_res = requests.post(url, files={"file": dfile})
    print(test_res.reason)
    if test_res.ok:
        print("File uploaded successfully ! ")
        return True
    else:
        print("Please Upload again ! ")
        return False


def down(videoId):
    os.system('yt-dlp --list-subs "https://www.youtube.com/watch?v=' + videoId + '"')
    os.system(
        'yt-dlp --format "bv*[ext=mp4][height<=720]+ba[ext=m4a]/b[ext=mp4][height<=720]" --write-auto-sub -o "./%(id)s.%(ext)s" "https://www.youtube.com/watch?v='
        + videoId
        + '"'
    )
    # now = arrow.utcnow().to("US/Pacific").format("YYYYMMDD-HHmmss")
    # os.rename(videoId + '.mp4', now + '.mp4')
    # os.system('ffmpeg -i ' + videoId + '.mp4 -vf scale=1280:-1 -c:a copy ' + now + '.mp4')
    os.system("ls -al")
    if(os.path.exists(videoId + ".en.vtt")):
        os.system(
            "ffmpeg -i "
            + videoId
            + '.mp4 -lavfi "subtitles='
            + videoId
            + ".en.vtt:force_style='Alignment=0,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=18,MarginL=5,MarginV=25'\" "
            + videoId
            + "-.mp4"
        )
        os.system("ls -al")
        ret = upload(videoId + "-.mp4")
        print(ret)
        # if ret:
        #   file = now+'.txt'
        #   vtt = webvtt.read(videoId+'.en.vtt')
        #   transcript = ""
        #   lines = []
        #   for line in vtt:
        #       lines.extend(line.text.strip().splitlines())

        #   previous = None
        #   for line in lines:
        #       line += "\n"
        #       if line == previous:
        #         continue
        #       transcript += " " + line
        #       previous = line

        #   open(file,'a', encoding='utf-8').writelines(transcript)
        #   upload(file)

key = sys.argv[1]

def duration_to_seconds(duration):
    day_time = duration.split("T")
    day_duration = day_time[0].replace("P", "")
    day_list = day_duration.split("D")
    if len(day_list) == 2:
        day = int(day_list[0]) * 60 * 60 * 24
        day_list = day_list[1]
    else:
        day = 0
        day_list = day_list[0]
    hour_list = day_time[1].split("H")
    if len(hour_list) == 2:
        hour = int(hour_list[0]) * 60 * 60
        hour_list = hour_list[1]
    else:
        hour = 0
        hour_list = hour_list[0]
    minute_list = hour_list.split("M")
    if len(minute_list) == 2:
        minute = int(minute_list[0]) * 60
        minute_list = minute_list[1]
    else:
        minute = 0
        minute_list = minute_list[0]
    second_list = minute_list.split("S")
    if len(second_list) == 2:
        second = int(second_list[0])
    else:
        second = 0
    return day + hour + minute + second

os.system(
    """curl -o ids.json 'https://youtube.googleapis.com/youtube/v3/search?part=id&channelId=UCuFFtHWoLl5fauMMD5Ww2jA&maxResults=5&order=date&type=video&key={}' \
  -H 'authority: youtube.googleapis.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-AU,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,pl;q=0.6,pt;q=0.5,af;q=0.4' \
  -H 'cache-control: max-age=0' \
  -H 'sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIa2yQEIpLbJAQjEtskBCKmdygEIgv3KAQiWocsBCIWTzQEIy5PNAQiSls0BCOKXzQEI45fNAQjpm80BCMuczQEI+pzNAQi/n80BCIagzQEIu6HNARjXnM0B' \
  --compressed""".format(
        key
    )
)

conn = sqlite3.connect("./db1.db")
try:
    conn.execute(
        "CREATE TABLE tb1(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL)"
    )
except:
    pass

ids = []
with open("ids.json") as json_file:
    data = json.load(json_file)
    for item in data["items"]:
        videoId = item["id"]["videoId"]
        count = conn.execute(
            "SELECT count(1) from tb1 where name = '{}'".format(videoId)
        ).fetchone()[0]
        if count == 0:
            ids.append(videoId)
            conn.execute("INSERT INTO tb1(NAME) VALUES ('{}')".format(videoId))
    conn.commit()
conn.close()

print(ids)

os.system(
    """curl -o ids.json 'https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key={}' \
  -H 'authority: youtube.googleapis.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-AU,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,pl;q=0.6,pt;q=0.5,af;q=0.4' \
  -H 'cache-control: max-age=0' \
  -H 'sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIa2yQEIpLbJAQjEtskBCKmdygEIgv3KAQiWocsBCIWTzQEIy5PNAQiSls0BCOKXzQEI45fNAQjpm80BCMuczQEI+pzNAQi/n80BCIagzQEIu6HNARjXnM0B' \
  --compressed""".format(
        ','.join(ids),
        key
    )
)

with open("ids.json") as json_file:
    data = json.load(json_file)
    for item in data["items"]:
        videoId = item["id"]
        dur = item["contentDetails"]["duration"]
        print(dur)
        seconds = 0
        try:
            seconds = duration_to_seconds(dur)
        except:
            pass
        if seconds > 0 and seconds < 600:
            down(videoId)
