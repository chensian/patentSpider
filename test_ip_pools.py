#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/21 11:43 
# @Author  : chesian
# @Site    : 
# @File    : test_ip_pools.py
# @Software: PyCharm
import random

import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup


def func():
    pass

reload(sys)
sys.setdefaultencoding('utf-8')

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60'
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50'
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
]


def clawer_ips():
    base_url = "http://www.kuaidaili.com/free/inha/"
    f_ips = open("ips.csv", "a")
    for page in range(1, 1789):
        url = base_url + str(page)
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        nodes = soup.find_all("tr")
        for node in nodes:
            # print node
            for a in node.select("td"):
                # print "".join(a.stripped_strings)
                f_ips.write("".join(a.stripped_strings)+",")
            f_ips.write("\n")
        # break


def test_useful(proxy):
    # print '[INFO] Testing proxy ', proxy, ' now...'
    try:
        proxies = {'http': proxy}
        requests.get('http://www.pss-system.gov.cn', timeout=5, proxies=proxies)
        # print '[Congra] Successfully get one'
        return True
    except Exception, e:
        # print e
        return False


if __name__ == "__main__":
    # clawer_ips()
    ip_pools = set()
    ips = pd.read_csv("ip.csv")


    for ip, port in zip(ips["IP"], ips["PORT"]):
        pro = str(ip)+":"+str(port)
        if test_useful(pro):
            ip_pools.add(pro)

    for ip in ip_pools:
        print ip
