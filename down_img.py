# -*- coding:utf-8 -*-


import requests
import os

FILE = "./result.txt"
DIR = "./result"

with open(FILE) as f:
    lines = f.readlines()
    for line in lines:
        if line.strip():
            down_url, filename = line.strip().split()
            r = requests.get(down_url, stream=True) 
            filename = filename.replace("/", "#")
            path = os.path.join(DIR, filename)
            print path
            with open(path, "wb") as fw:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        fw.write(chunk)
                        fw.flush()

