# -*- coding:utf-8 -*- 


import urlparse

FILE_404 = "404.list.txt"
FILE_RESULT = "result_img.txt"

OUTPUT = "result.txt"

l_404 = []
l_result = {}

with open(FILE_404) as f:
    for line in f:
        path = urlparse.urlparse(line.strip()).path
        l_404.append(path)

with open(FILE_RESULT) as f:
    for line in f:
        path = urlparse.urlparse(line.split()[0]).path
        l_result[path] = line


with open(OUTPUT, "wb") as f:
    for i in l_404:
        if i in l_result:
            f.write(l_result[i])
