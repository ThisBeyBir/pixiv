from email import header
from email.header import Header
import re
from time import sleep
from turtle import title
from urllib import request

import requests
import os
from lxml import etree
import jieba
import json
import pprint

PixivHeaders={
    'authority':'i.pximg.net',
    'method':'GET',
    #s'path': '/video/BV1NY4y1E7Dd',
    'scheme':'https',
    'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    #'cookie':'buvid3=C6FA7D37-BDAB-8A98-F46C-F74DCCD9E1E590619infoc; _uuid=611AEF8F-FA10A-F25E-63B1-7C6851A3E69C92883infoc; buvid4=A0BF7CAD-00E0-291D-0057-8C4CC946B8DF91548-022012618-yPTK2yRnbGG1AbZfVzPX2Q%3D%3D; rpdid=|(kRJkkRmJ~0J\'uYRJumJumJ; buvid_fp_plain=undefined; blackside_state=0; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO9316494943737456; is-2022-channel=1; nostalgia_conf=-1; hit-dyn-v2=1; go_old_video=-1; theme_style=light; bsource=search_baidu; fingerprint3=b91abfafa0dabad6a036f1b9b0f4c5f3; fingerprint=e5690504a7252e22c88daa209cce9049; CURRENT_FNVAL=4048; b_lsid=B49FD875_182861848B2; b_timer=%7B%22ffp%22%3A%7B%22333.788.fp.risk_C6FA7D37%22%3A%221828618A9AA%22%2C%22333.1193.fp.risk_C6FA7D37%22%3A%221828189D702%22%2C%22333.999.fp.risk_C6FA7D37%22%3A%2218286187503%22%2C%22888.2421.fp.risk_C6FA7D37%22%3A%221828193B951%22%2C%22666.25.fp.risk_C6FA7D37%22%3A%22182859DCF3D%22%2C%22333.976.fp.risk_C6FA7D37%22%3A%2218272FE2BEE%22%2C%22444.41.fp.risk_C6FA7D37%22%3A%221827BA2EEE0%22%2C%22333.937.fp.risk_C6FA7D37%22%3A%22182731D8041%22%2C%22333.337.fp.risk_C6FA7D37%22%3A%221828596C0EF%22%2C%22777.5.0.0.fp.risk_C6FA7D37%22%3A%221828193925D%22%2C%22666.19.fp.risk_C6FA7D37%22%3A%2218276C82C19%22%2C%22333.967.fp.risk_C6FA7D37%22%3A%22182818AB45E%22%2C%22333.880.fp.risk_C6FA7D37%22%3A%221828193B897%22%2C%22333.42.fp.risk_C6FA7D37%22%3A%22182861C7407%22%7D%7D; SESSDATA=e20c69d7%2C1675659396%2C09715%2A81; bili_jct=54992fbb96d8876b46cc8abb37df1a57; DedeUserID=35671002; DedeUserID__ckMd5=d69f732e9248e565; buvid_fp=e5690504a7252e22c88daa209cce9049; CURRENT_QUALITY=116; bp_video_offset_35671002=692641245482188900; sid=7p2ab96c; PVID=11',
    'referer':'https://www.pixiv.net/',
    'sec-ch-ua':'"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'image',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-mode':'no-cors',
    'sec-fetch-site':'cross-site',
    #'sec-fetch-user':'?1',
    #'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'    
}
def getPic(id):
    model="https://www.pixiv.net/ajax/user/{}/profile/all?lang=en".format(id)
    res=requests.get(model)
    dirt1=json.loads(res.text)
    ls=list(dirt1['body']['illusts'].keys())
    model = "https://www.pixiv.net/ajax/user/{}/profile/illusts?".format(id)
    url=model
    ls2=[]
    for i in range(len(ls)):
        url+='ids[]='+ls[i]+'&'
        if((i+1)%40==0):
            try:
                url+='work_category=illustManga&is_first_page=0&lang=en'
                res=requests.get(url)
                res.close()
                dirt2=json.loads(res.text)
                pprint.pprint(dirt2['body']['works'])
                for j in range(i-39,i+1):
                    #pprint.pprint(dirt2['body']['works'][ls[j]]['url'])
                    ls2.append(dirt2['body']['works'][ls[j]]['url'])
                url=model
            except:
                pass
            pass
        if(i==len(ls)-1):
            try:
                url+='work_category=illustManga&is_first_page=0&lang=en'
                res=requests.get(url)
                dirt2=json.loads(res.text)
                for j in range(1+int((i/40))*40,i+1):
                    ls2.append(dirt2['body']['works'][ls[j]]['url'])
                url=model
                res.close()
            except:
                pass
        pass
    for i in range(len(ls2)):
        ls2[i]=ls2[i].replace('c/250x250_80_a2/','')
        ls2[i]=ls2[i].replace('custom-thumb','img-master')
        ls2[i]=ls2[i].replace('custom','master')
        ls2[i]=ls2[i].replace('square','master')
        pass
    pprint.pprint(ls2)
    for i in range(len(ls2)):
        sleep(1)
        try:
            res=requests.get(ls2[i],headers=PixivHeaders)
            res.close()
            byte=res.content
            with open(str(i)+'.png',"wb") as f:
                f.write(byte)
        except:
            pass
    pass
id=input()
getPic(id)
