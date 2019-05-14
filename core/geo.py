# coding:UTF-8
import requests
from datetime import datetime
import time
import urllib
import re
import os
import sys
import json
import random

from random import choice
from bs4 import BeautifulSoup

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)", 
]

FILE_PATH= "/"
file = open('./data/data.json', 'w')
year = "2018"
data = {}
province_data = {}
city_data = {}
area_data = {}

def httpGet(url):
    session= requests.Session()
    session.headers= {
        'User-Agent': choice(UA_LIST),
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.stats.gov.cn'
    }

    page = session.get(url,timeout=30000)
    page.encoding='GBK'

    soup = BeautifulSoup(page.text, features="html.parser")

    # 如果遇到报错，建议开启延时执行
    # try:
    #     time.sleep(1)
    # except:
    #     print('error')

    return soup;

def getProvince(year):
    url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'+year+'/index.html'
    http_text = httpGet(url)
    for item in http_text.select('.provincetr'):
        for item_a in item.find_all('a'):
            province_name = item_a.get_text()
            province_code = item_a['href'].replace(".html", "")
            code = int(province_code) * 10000

            print(province_name)

            province_data[code] = {
                'name':province_name,
                'parent_code':''
            }

    return province_data;

def getCity(year,provinceCode):
    f_provinceCode = str(round(provinceCode/10000))
    url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'+year+'/'+f_provinceCode+'.html'
    http_text = httpGet(url)
    for item in http_text.select('.citytr'):
        info = item.find_all('td')[1].find('a')
        city_name = info.get_text()
        city_code = info['href'].replace(f_provinceCode + "/", "").replace(".html", "")
        code = int(city_code) * 100
        
        print(city_name)

        city_data[code] = {
            'name':city_name,
            'parent_code':provinceCode
        }
            

    return city_data;


def getArea(year,provinceCode,cityCode):
    f_provinceCode = str(round(provinceCode/10000))
    f_cityCode = str(round(cityCode/100))
    url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'+year+'/'+f_provinceCode+'/'+f_cityCode+'.html'
    http_text = httpGet(url)
    for item in http_text.select('.countytr'):
        rst = {}

        # code
        code = item.find_all('td')[0]
        if len(code.find_all('a'))>0 :
            rst["code"] = round(int(code.find('a').get_text()) / 1000000)
        else:
            rst["code"] = round(int(code.get_text()) / 1000000)

        #name
        name = item.find_all('td')[1]
        if len(name.find_all('a'))>0 :
            rst["name"] = name.find('a').get_text()
        else:
            rst["name"] = name.get_text()

        print(rst["name"])

        city_data[rst["code"]] = {
            'name':rst["name"],
            'parent_code':cityCode
        }

    return area_data;
    


if __name__ == '__main__':
    print("======开始获取省数据======")
    getProvince(year)

    print("======开始获取城市数据======")
    for item in list(province_data.keys()):
        getCity(year,item)

    print("======开始获取区数据======")
    for item in list(city_data.keys()):
        getArea(year,city_data[item]['parent_code'],item)

    data.update(province_data)
    data.update(city_data)
    data.update(area_data)
    file.write(json.dumps(data,ensure_ascii=False, indent=4, separators=(',', ':')))
    file.close();

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
