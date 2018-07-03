# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 16:14:04 2018

@author: HP
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 09:15:11 2018

@author: HP
"""
#多次试验，发现并不适合用requests，谨记！！！！！！！！！！！！！！！！
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import requests
from urllib.request import urlopen,Request
from os import mkdir,listdir
import time
chrome_options = Options()
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
#    chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('--headless')#采用无头模式，不显示Chrome浏览器
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
browser = webdriver.Chrome(chrome_options=chrome_options)
headers = {
           'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}    
def get_url_list(url):
    browser.get(url)
    selenium_url_list = browser.find_elements_by_xpath('//*[@id="play_0"]/ul/li/a')
    url_list = []
    for i in selenium_url_list:
        ur = i.get_attribute("href")
        url_list.append(ur)
    return url_list
def get_pic_url(url):
    browser.get(url)
    get_url_len = browser.find_elements_by_xpath('//*[@id="selectpage1"]/select/option')
    name = browser.find_element_by_xpath('//*[@id="position-common"]/a[4]').text
#    cookies = browser.get_cookies()#从selenium中获取cookie
#    cookie_list = []
#    for i in cookies:
#        cookie = i['name']+'='+i['value']
#        cookie_list.append(cookie)
#    cookie_str = ';'.join(cookie_list)#获得cookie
#    headers['Cookie'] = cookie_str
    name1 = './一人之下/'+name
    if name not in listdir('./一人之下/'):
        mkdir(name1)
    print(name)
    pic_url = []
    for i in range(len(get_url_len)):
        selenium_picture = browser.find_element_by_xpath('//*[@id="viewimg"]')
        picture_url = selenium_picture.get_attribute('src')
        name2 = name+'/'+name+"_"+str(i)
        write_file(picture_url,name2,headers)
        pic_url.append(picture_url)
        if i != len(get_url_len)-1:
            selenium_picture.click()
        time.sleep(1)#加入线程歇息，也是为对方服务器考虑，爬虫不宜对对方服务器，负载过大
#    print(pic_url)
def write_file(url,name,headers):
    req = Request(url,headers=headers)
    pic_req = urlopen(req)
    pic = pic_req.read()
    with open('./一人之下/'+name+'.jpg', 'wb') as file:
        file.write(pic) # data相当于一块一块数据写入到我们的图片文件中

#    with open('./一人之下/'+name+'.jpg', 'wb') as f:
#        f.write(pic.content)
if __name__=="__main__":
    url = 'http://www.taduo.net/manhua/2/'
    urllist = get_url_list(url)
    for i in urllist[60:]:
        print('爬取的网址：',i)
        get_pic_url(i)
        time.sleep(5)
    print("所有爬取完成！！！")