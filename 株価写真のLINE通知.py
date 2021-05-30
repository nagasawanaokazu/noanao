import time                            # スリープを使うために必要
from selenium import webdriver         # Webブラウザを自動操作する（python -m pip install selenium)
import pyautogui as pgui
import pytz
import os
import datetime
import pandas as pd
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import chromedriver_binary             # パスを通すためのコード
import requests

def get_photo(URL,CODE):
        
    """options = Options()
    #ヘッドレスモード(chromeを表示させないモード)
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)"""
    
    driver = webdriver.Chrome()# Chromeを準備

    # SBI証券のトップ画面を開く
    driver.get(URL)

    key_word = driver.find_element_by_id('codeSearch')
    #銘柄検索
    key_word.send_keys(CODE)

    # 検索ボタンをクリック
    driver.find_element_by_xpath('//*[@id="tabSearch1"]/a/input').click()
    time.sleep(3)

    #webのスクロール
    driver.execute_script("window.scrollTo(0,300)")
    time.sleep(3)
    
    date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    date = date.strftime('%Y年%m月%d日')

    #スクリーンショット
    photo = pgui.screenshot('/Users/nagasawanaokazu/Documents/python_cron/' + date + '.png',region=(310,360,1455,1350))
    time.sleep(3)# 5秒間待機
    
    # ブラウザーを閉じる
    driver.quit() 
    
    return photo
    
def line_notification(photo):
    
    date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    date = time.strftime('%Y年%m月%d日')

    TOKEN = '.............GY29NWlGM69q37'
    api_url = 'https://notify-api.line.me/api/notify'
    send_contents = '今日の株価データです' + date

    TOKEN_dic = {'Authorization':'Bearer' + ' ' + TOKEN}
    send_dic = {'message':send_contents}

    image_file = '/Users/nagasawanaokazu/Documents/python_cron/' + date + '.png'
    binary = open(image_file,mode='rb')
    image_dic = {'imageFile':binary}

    requests.post(api_url,headers=TOKEN_dic,data=send_dic,files=image_dic)

if __name__ == '__main__':
    URL = 'https://www.sbisec.co.jp/ETGate'
    CODE = '2635'
    
    photo = get_photo(URL,CODE)
    line_notification(photo)