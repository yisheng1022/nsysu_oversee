from bs4 import BeautifulSoup as BS
import random,time,os,pickle,json,requests,re,gc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd

def Get_50(key_list,first = True,run_all_day = True):
	headers = {"Authorization": "Bearer " + "Q1NjshykrHWJVXOCLWCMOSjyKY6TPefqRZmxEiYGKPp","Content-Type": "application/x-www-form-urlencoded"}
	while run_all_day:
		art_title = []; art_urll = []; art_exc = []
		old_id = ""
		if first:
			art_url = "https://www.dcard.tw/service/api/v2/forums/nsysu/posts?limit=50"
		else:
			art_url = "https://www.dcard.tw/service/api/v2/forums/nsysu/posts?limit=50&after={}".format()
		open_page = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
		open_page.get(art_url)
		while ((open_page.title == "Attention Required! | Cloudflare") | (open_page.title == "Just a moment...")):
			open_page.close()
			print("Too frequent visit when getting 100 article. Wait for retry.")
			time.sleep(random.randint(300,420))
			open_page = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
			open_page.get(art_url)

		html_source = open_page.page_source
		page_html=BS(html_source,"html.parser")
		art_json = json.loads(page_html.text)
		open_page.close()

		for one_art in art_json:
			art_title.append(one_art["title"])
			art_urll.append("https://www.dcard.tw/service/api/v2/posts/{}".format(one_art["id"]))
			art_exc.append(one_art["excerpt"])

		for i in range(0,len(art_title)):
			print(art_title[i])
			if (any(key_w in art_exc[i] for key_w in key_list) | any(key_w in art_title[i] for key_w in key_list)):
				params = {"message": "Dcard_中山大學版出現可能是您正在關注的貼文。\n標題：{}\n網址如下：{}".format(art_title[i],art_urll[i])}
				r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
		old_id = art_json[49]["id"]
		first = False
		time.sleep(1800)

key_words = ["課程","請教","涼課","初選"]
params = {"message": "Dcard_中山大學版出現可能是您正在關注的貼文。\n標題：{}\n網址如下：{}"}
r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
Get_50(key_words,first = True,run_all_day = True)




