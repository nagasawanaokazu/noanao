import datetime
import numpy as np
import subprocess
import os
import cv2
import time
import requests
 
token = 'HGS2DPJT5NQN4NRFNqAMlRMQTbkcVzhJ2tTqtosXKHP' 
motion_th = 1000 #動体検知の閾値
 
while True:
    #時刻取得
    time = datetime.datetime.now()
    strtime = time.strftime('%Y%m%d_%H:%M:%S')
    FileName = strtime + ".jpg"
 
    #image1 capture
    print("e1開始　%s" %(strtime))
    cmd1 = 'fswebcam -r 640x480 --no-banner e1.jpg'
    ps1 = subprocess.run(cmd1.split(),stdout=subprocess.PIPE)
 
    #image2 capture
    print("e2開始")
    cmd2 = 'fswebcam -r 640x480 --no-banner e2.jpg'
    ps2 = subprocess.run(cmd2.split(),stdout=subprocess.PIPE)
 
    #動体検知
    img1 = cv2.imread("e1.jpg")
    img2 = cv2.imread("e2.jpg")
 
    #背景差分の設定
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()          # 背景オブジェクトを作成
 
    fgmask = fgbg.apply(img1)
    fgmask = fgbg.apply(img2)
 
    motion = cv2.countNonZero(fgmask)
    print("動体検知：%d"%(motion))
 
    if (motion > motion_th):
        cv2.imwrite(FileName,img2)
        print("----Captured!----")
       
        payload = {'message': '動体検知しました'}  # 送信メッセージ
        url = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': 'Bearer ' + token}
 
        files={"imageFile":open(FileName,"rb")}
        res = requests.post(url, data=payload, headers=headers,files=files,)  # LINE NotifyへPOST
        print(res)
        
        #検出画像
        cv2.imwrite('./diff.jpg',fgmask)
 
        time.sleep(60)
    else:
        pass
 
    # 表示
    #cv2.imshow('frame',fgmask)
cv2.waitKey(0) 
cv2.destroyAllWindows()