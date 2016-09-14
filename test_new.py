# -*- coding:utf-8 -*-


from pymogile import Client
import multiprocessing

import time


CI_CLIENT = Client(domain="ci", trackers=['ip'])
GROUP_CLIENT = Client(domain="group", trackers=['ip'])
SHOP_CLIENT = Client(domain="shop", trackers=['ip'])
CLIENT_MAP = {
    "5": CI_CLIENT,
    "2": GROUP_CLIENT,
    "1": SHOP_CLIENT
}

FAIL_FILE = "./result_err.txt"   # 跑失败的结果文件
RESULT_FILE = "./result_new.txt"  # 结果输出
RESULT_ERR_FILE = "./result_new_err.txt"  # 这次失败的结果

PROCESS_NUM = 10


def handler(line):
    if not line:
        return ""
    domain_id, key = line.split()[0].strip(), line.split()[1].strip()
    datastore = CLIENT_MAP.get(domain_id)
    if not datastore:
        if domain_id in ("1", "2", "5"):
            if domain_id == "1":
                SHOP_CLIENT = Client(domain="shop", trackers=['10.1.115.13:6001'])
                if SHOP_CLIENT:
                    datastore = SHOP_CLIENT
            elif domain_id == "2":
                GROUP_CLIENT = Client(domain="group", trackers=['10.1.115.13:6001'])
                if GROUP_CLIENT:
                    datastore = GROUP_CLIENT
            elif domain_id == "5":
                CI_CLIENT = Client(domain="ci", trackers=['10.1.115.13:6001'])
                if CI_CLIENT:
                    datastore = CI_CLIENT
            if not datastore:
                with open(RESULT_ERR_FILE, "a+") as ferr:
                    ferr.write("{0}\t{1}{2}".format(domain_id, key, "\n"))
                    return ""
    file_paths = datastore.get_paths(key)
    if file_paths:
        return "".join([file_paths[0].split(",")[0], '\t', key, "\n"])
    else:
        retry = 0
        while retry < 3:
            file_paths = datastore.get_paths(key)
            if file_paths:
                return "".join([file_paths[0].split(",")[0], '\t', key, "\n"])
            retry += 1
            time.sleep(0.00001)

        with open(RESULT_ERR_FILE, "a+") as ferr:
            ferr.write("{0}\t{1}{2}".format(domain_id, key, "\n"))
            return ""

start = time.time()
fw = open(RESULT_FILE, "wb")
with open(FAIL_FILE) as f:
    p = multiprocessing.Pool(PROCESS_NUM)
    it = p.imap(handler, f, 5)
    while True:
        try:
            res = it.next()
            if res is None:
                time.sleep(0.0000001)
                continue
        except StopIteration:
            break
        fw.write(res)
        time.sleep(0.0000001)
fw.close()
print time.time() - start
