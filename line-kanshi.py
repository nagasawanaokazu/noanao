# -*- coding: utf-8 -*-
import cv2
import os
import datetime
import time
import numpy as np
import requests,os
 
# os.chdir("./photo") #画像保存先に移動
line_notify_token = 'HGS2DPJT5NQN4NRFNqAMlRMQTbkcVzhJ2tTqtosXKHP'
line_notify_api = 'https://notify-api.line.me/api/notify'
message = '動体検知しました'

def main():
    cam = cv2.VideoCapture(0)
    img1 = img2 = img3 = get_image(cam)
    th = 400
    num = 1
    new_dir_path = 'data'
    save_flg = 0
    #Create a saving folder
    try:
        os.makedirs(new_dir_path)
    except FileExistsError:
        pass
    start = time.time()
    while True:
        #Enterキーが押されたら終了
        if cv2.waitKey(1) == 13: break
        im_fs = check_image(img1,img2,img3)
        cnt = cv2.countNonZero(im_fs)
 
        time_lag = time.time() - start
        if cnt > th:
            start = time.time()
            save_path = new_dir_path+'/'+str('{0:%Y%m%d%H%S}'.format(datetime.datetime.now())) + '.jpg'
            cv2.imwrite(save_path,img3)
            num += 1
            #line
            payload = {'message': message}
            headers = {'Authorization': 'Bearer ' + line_notify_token}
            files = {'imageFile': open(save_path, "rb")} #バイナリファイルを開く
            line_notify = requests.post(line_notify_api, data=payload, headers=headers, files=files)
        else:
            cv2.imshow('PUSH ENTER KEY', im_fs)
        img1,img2,img3 = (img2,img3,get_image(cam))
    cam.release()
    cv2.destroyAllWindows()

# 画像に動きがあったか調べる関数
def check_image(img1, img2, img3):
    # グレイスケール画像に変換 --- (*6)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)
    # 絶対差分を調べる --- (*7)
    diff1 = cv2.absdiff(gray1, gray2)
    diff2 = cv2.absdiff(gray2, gray3)
    # 論理積を調べる --- (*8)
    diff_and = cv2.bitwise_and(diff1, diff2)
    # 白黒二値化 --- (*9)
    _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)
    # ノイズの除去 --- (*10)
    diff = cv2.medianBlur(diff_wb, 5)
    return diff
            
def get_image(cam):
    img = cam.read()[1]
    img = cv2.resize(img,(600,400))
    return img
main()