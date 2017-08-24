#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/8 23:00 
# @Author  : chesian
# @Site    : 
# @File    : patent_clawer.py
# @Software: PyCharm
import csv
import json
import random
import re

import sys

import time
from bs4 import BeautifulSoup

from test_ip_pools import test_useful

reload(sys)
sys.setdefaultencoding('utf-8')

pros = [
    # "202.119.162.138:80",
    # "210.29.26.250:80",
    # "43.240.138.31:8080",
    # "111.1.3.36:8000",
    # "121.12.170.233:8998",
    # "121.232.144.81:9000",
    # "118.117.139.144:9000",
    # "43.240.138.31:8080",
    "119.254.84.90:80",
    # "114.215.192.135:8118",
    # "101.4.60.50:80",
    # "121.232.148.143:9000",
    # "117.90.7.194:9000",
    "182.254.246.215:8123",
    # "101.4.136.34:81",
    "58.254.132.87:80",
    "183.62.60.100:80",
]

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

cookies_strs = [
    "WEE_SID=r9UTtXo8y2yXNcf7K8wjgAH-7fUjyMcd91HeSqRUcbdX_ZzJrSo_!-1520733268!2083373865!1503569214012; IS_LOGIN=true; wee_username=cHBwcHAxMjM%3D; wee_password=cHFwNTQ1MjUwNw%3D%3D; JSESSIONID=r9UTtXo8y2yXNcf7K8wjgAH-7fUjyMcd91HeSqRUcbdX_ZzJrSo_!-1520733268!2083373865; _gscu_761734625=03501374f8hl8s15; _gscs_761734625=t03575978x4yu6v91|pv:3; _gscbrs_761734625=1",

    "WEE_SID=HUUUG1rxKZlWzLgVf4keAnux2CpW6HFHPAOYcmHixMXxccUKA8O3!879531882!187197179!1503575890673; IS_LOGIN=true; avoid_declare=declare_pass; JSESSIONID=HUUUG1rxKZlWzLgVf4keAnux2CpW6HFHPAOYcmHixMXxccUKA8O3!879531882!187197179; _gscu_761734625=03401759u08w3823; _gscs_761734625=t03576099mxlcjl23|pv:1; _gscbrs_761734625=1"
]


def get_cookies():
    cookies_str = random.choice(cookies_strs)
    cookies = {}  # 初始化cookies字典变量
    for line in cookies_str.split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容

    return cookies


def extract_data(content):
    rows = []
    soup = BeautifulSoup(content)
    # print soup.prettify()
    nodes = soup.find_all("li", class_="patent")
    for patent in nodes:
        row = {}
        vIdHidden = patent.find_all(attrs={"name": "vIdHidden"})[0]['value']
        idHidden = patent.find_all(attrs={"name": "idHidden"})[0]['value']
        titleHidden = patent.find_all(attrs={"name": "titleHidden"})[0]['value']
        nrdAnHidden = patent.find_all(attrs={"name": "nrdAnHidden"})[0]['value']
        nrdAdpHidden = patent.find_all(attrs={"name": "nrdAdpHidden"})[0]['value']
        nrdpdHidden = patent.find_all(attrs={"name": "nrdpdHidden"})[0]['value']
        nrdPnHidden = patent.find_all(attrs={"name": "nrdPnHidden"})[0]['value']
        appSnHidden = patent.find_all(attrs={"name": "appSnHidden"})[0]['value']
        pnSnHidden = patent.find_all(attrs={"name": "pnSnHidden"})[0]['value']
        langHidden = patent.find_all(attrs={"name": "langHidden"})[0]['value']
        docStatusHidden = patent.find_all(attrs={"name": "docStatusHidden"})[0]['value']
        appNameHidden = patent.find_all(attrs={"name": "appNameHidden"})[0]['value']
        appAddrHidden = patent.find_all(attrs={"name": "appAddrHidden"})[0]['value']
        appZipHidden = patent.find_all(attrs={"name": "appZipHidden"})[0]['value']
        appCountryHidden = patent.find_all(attrs={"name": "appCountryHidden"})[0]['value']

        row["文献标识"] = vIdHidden
        row["文献唯一标识"] = idHidden
        row["发明名称"] = titleHidden
        row["nrdAnHidden"] = nrdAnHidden
        # row["申请日"] = nrdAdpHidden
        # row["公开（公告）日"] = nrdpdHidden
        # row["公开（公告）号"] = nrdPnHidden
        row["appSnHidden"] = appSnHidden
        row["pnSnHidden"] = pnSnHidden
        row["国家"] = langHidden
        row["文献状态"] = docStatusHidden
        # row["申请人/专利权人"] = appNameHidden
        row["地址"] = appAddrHidden
        row["邮编"] = appZipHidden
        row["申请人/专利权人所在国代码"] = appCountryHidden

        for a in patent.select("p"):
            dict_data = "".join(a.stripped_strings).split(":")
            row[dict_data[0].strip()] = dict_data[1].strip()

        rows.append(row)
        # for key in row:
        #     print key, "-----", row[key]
        # break
    form_data = {}
    try:
        form = soup.find_all(attrs={"name": "resultlistForm"})[0]

        for input in form.find_all("input"):
            form_data[input["name"].strip()] = input["value"].strip()
    except IndexError:
        # print "no data!!!"
        pass
    return rows, form_data


def parse_index(company):
    import requests
    url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeSmartSearch1207-executeSmartSearch.shtml'
    d = {
        "searchCondition.searchExp": company,
        "searchCondition.dbId": "VDB",
        "resultPagination.limit": "12",
        "searchCondition.searchType": "Sino_foreign",
        "wee.bizlog.modulelevel": "0200101"

    }
    r = requests.post(url, data=d, cookies=get_cookies(),
                      headers={'User-Agent': random.choice(user_agents)})
    time.sleep(5)
    # open("content.html", "w").write(r.content)
    return r.content


def parse_turn_page(form_data):
    import requests

    url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml'

    company_name = form_data["searchCondition.searchExp"]
    searchKeywords = ""
    for i in range(0, len(company_name)):
        searchKeywords += "[" + company_name[i] + "][ ]{0,}"

    d = {
        "resultPagination.limit": "12",
        "resultPagination.sumLimit": "10",
        "resultPagination.start": form_data["resultPagination.start"],
        "resultPagination.totalCount": form_data["resultPagination.totalCount"],
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.dbId": "",
        "searchCondition.strategy": "",
        "searchCondition.literatureSF": "复合申请人与发明人=(" + company_name + ")",
        "search_scope": "",
        "searchCondition.searchKeywords": searchKeywords,
        "searchCondition.searchExp": company_name,
        "searchCondition.executableSearchExp": "VDB:(IBI=" + company_name + ")",
        "wee.bizlog.modulelevel": "0200101",
    }

    r = requests.post(url, data=d, cookies=get_cookies(),
                      headers={'User-Agent': random.choice(user_agents)})
    time.sleep(10)
    # r = requests.post(url, data=d, cookies=get_cookies(), proxies={'http': random.choice(pros)},
    #                   headers={'User-Agent': random.choice(user_agents)})
    return r.content


def file_to_list(path, filename):
    with open(path + filename, "rb") as f:
        lines = f.readlines()
    txtList = []
    for line in lines:
        line = line.replace('\r', '').replace('\n', '')
        tokens = re.split(",| ", line)
        txtList.append(tokens[0])
    return txtList


def file_to_json(filename):
    lines = open(filename).readlines()

    colums = set()
    rows = []
    for i in range(0, len(lines), 2):
        row = {}

        print len(lines[i].split(":")), len(lines[i + 1].split(":"))
        for key, value in zip(lines[i].split(":"), lines[i + 1].split(":")):
            row[key.replace('\n', '')] = value.replace('\n', '')
            colums.add(key.replace('\n', ''))
        rows.append(row)

    f = open("patent_all.csv", "a")
    f.write(",".join(colums) + "\n")

    print len(rows)
    for row in rows:
        line = []
        for key in colums:
            if key not in row.keys():
                line.append("")
            else:
                line.append(row[key])

        f.write(",".join(line) + "\n")


def check_post_num(post_num, content, f):
    post_num += 1
    rows, form_data = extract_data(content)
    for row in rows:
        # print row
        f.write(":".join(row.keys()) + "\n")
        f.write(":".join(row.values()) + "\n")
    if post_num > 500:
        return -1
    if len(form_data) == 0:
        return 0
    else:
        return form_data


def get_patent_num(company):
    import requests
    url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeSmartSearch1207-executeSmartSearch.shtml'
    d = {
        "searchCondition.searchExp": company,
        "searchCondition.dbId": "VDB",
        "resultPagination.limit": "12",
        "searchCondition.searchType": "Sino_foreign",
        "wee.bizlog.modulelevel": "0200101"
    }
    r = requests.post(url, data=d, cookies=get_cookies(),
                      headers={'User-Agent': random.choice(user_agents)})
    time.sleep(10)
    # open("content.html", "w").write(r.content)
    rows, form_data = extract_data(r.content)
    # form_data = {}
    if "resultPagination.totalCount" not in form_data:
        form_data["resultPagination.totalCount"] = 0
    return form_data["resultPagination.totalCount"]


def process():
    f = open("patent_all.txt", "a")
    f_log = open("log", "a")

    companys = file_to_list("", "company")
    companys_log = file_to_list("", "log")

    post_num = 0
    stop_page = 311

    for company in companys:

        if company in companys_log:
            print "skip"
            continue
        page = 1
        if stop_page != 0:
            result = {}
            result["resultPagination.start"] = 12 * stop_page
            result["searchCondition.searchExp"] = company
            result["resultPagination.totalCount"] = 5204
            page = stop_page
            stop_page = 0
        else:
            content = parse_index(company)
            result = check_post_num(post_num, content, f)

        if not isinstance(result, int):
            print result["resultPagination.totalCount"]
            print company, "page ", page
            while (int(result["resultPagination.start"]) != int(result["resultPagination.totalCount"]) / 12 * 12):
                page += 1
                result["resultPagination.start"] = int(result["resultPagination.start"]) + 12
                print company, "page ", page
                content = parse_turn_page(result)

                result = check_post_num(post_num, content, f)
                if isinstance(result, int):
                    if result == 0:
                        break
                    else:
                        print company, "page ", page
                        print 1 / 0
        else:
            if result == -1:
                print company, "page 1"
                break

        f_log.write(company + "\n")


def post_test():
    result = {}
    result["resultPagination.start"] = 12 * 311
    result["searchCondition.searchExp"] = "康佳集团股份有限公司"
    result["resultPagination.totalCount"] = 5204
    print parse_turn_page(result)


def fitter_useful_ip():
    for pro in pros:
        if not test_useful(pro):
            print pro


if __name__ == "__main__":

    # fitter_useful_ip()

    f = open("patent_all.txt", "a")
    f_log = open("patent_num.csv", "a")

    companys = file_to_list("", "company")
    companys_log = file_to_list("", "patent_num.csv")
    post_num = 0
    for company in companys:
        if company not in companys_log:
            num = get_patent_num(company)
            print company, num
            f_log.write(company + "," + str(num) + "\n")
            post_num += 1
            if post_num > 400:
                break
        else:
            print company
    f.close()
    f_log.close()

    # process()
    # file_to_json("patent_all.txt")
