#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, subprocess, json, threading, requests, sqlite3

conn = sqlite3.connect("./db3.db")
try:
    conn.execute(
        "CREATE TABLE tb1(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL)"
    )
except:
    pass

for ch in ['test3']:
    os.system('md-to-pdf test3.md')

    count = conn.execute(
        "SELECT count(1) from tb1 where name = '{}'".format(ch)
    ).fetchone()[0]
    #if count == 0:
    if True:
#         conn.execute("INSERT INTO tb1(NAME) VALUES ('{}')".format(ch))
#         conn.commit()

        dfile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ch+'.pdf'), "rb")
        url = "https://file.moringstars.com/upload"
        test_res = requests.post(url, files = {"file": dfile})
        print(test_res)
        if test_res.ok:
            print(" File uploaded successfully ! ")
            print(test_res.text)
        else:
            print(" Please Upload again ! ")

conn.close()
