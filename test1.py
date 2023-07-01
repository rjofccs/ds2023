#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, subprocess, json, threading, requests, sqlite3
# subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
# os.system('pip3 install selenium')
#os.system('wget https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip')
# https://github.com/iamadamdev/bypass-paywalls-chrome/archive/master.zip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
from lxml import etree
from urllib.parse import urlparse


display = Display(visible=0, size=(1100, 8000))  
display.start()

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension('bypass-paywalls-chrome.crx');
options = [
   "--window-size=1100,8000",
   "--ignore-certificate-errors"
]
for option in options:
    chrome_options.add_argument(option)

conn = sqlite3.connect("./db2.db")
try:
    conn.execute(
        "CREATE TABLE tb1(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL)"
    )
except:
    pass

durl = "https://www.wsj.com/news/types/china-news"
driver = webdriver.Chrome(options=chrome_options)
driver.get(durl)
driver.get(durl)
page_source = driver.page_source
html = etree.HTML(page_source)
xs = html.xpath("//article/div[1]/a/@href")
for x in xs:
    print(x)
    ch = os.path.basename(urlparse(x).path)
    
    count = conn.execute(
        "SELECT count(1) from tb1 where name = '{}'".format(ch)
    ).fetchone()[0]
    if count == 0:
        driver.get(x)
        driver.save_screenshot(ch+'.png')

        conn.execute("INSERT INTO tb1(NAME) VALUES ('{}')".format(ch))
        conn.commit()

        dfile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ch+'.png'), "rb")
        url = "https://file.moringstars.com/upload"
        test_res = requests.post(url, files = {"file": dfile})
        print(test_res)
        if test_res.ok:
            print(" File uploaded successfully ! ")
            print(test_res.text)
        else:
            print(" Please Upload again ! ")

conn.close()
driver.quit()
