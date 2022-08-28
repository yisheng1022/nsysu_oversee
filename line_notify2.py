# ciLJ9xlsXP3Vj2AVGfyGecGmjkTMIy5IrSUUeGFcMR1
# https://nsysuoversee.herokuapp.com/callback/notify
# https://nsysuoversee.herokuapp.com/auth
# K3QsmFxxbSvUzHkUEiIrjYj6mWHzgkWNCVPy3N7RCeB
from bs4 import BeautifulSoup as BS
import random,time,os,pickle,json,requests,re,gc,cloudscraper
import pandas as pd

def Get_50(key_list,first = True,run_all_day = True):
	headers = {"Authorization": "Bearer " + "ciLJ9xlsXP3Vj2AVGfyGecGmjkTMIy5IrSUUeGFcMR1","Content-Type": "application/x-www-form-urlencoded"}
	art_title = []; art_urll = []; art_exc = []
	old_id = ""
	if first:
		art_url = "https://www.dcard.tw/service/api/v2/forums/nsysu/posts?limit=50"
	else:
		art_url = "https://www.dcard.tw/service/api/v2/forums/nsysu/posts?limit=50&after={}".format()
	
	art_req = cloudscraper.create_scraper().get(art_url)
	art_req.encoding = 'utf-8'
	print(art_req.text)
	art_json = art_req.json()

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
Get_50(key_words,first = True,run_all_day = True)
