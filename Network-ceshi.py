import requests
import json
import os
import time
import gzip
import random
import uuid
import datetime
import threading

def random_str():
    device_id = str(uuid.uuid1())
    return device_id


def time_data(day_num):
    temp_date = datetime.datetime.now()   # 获取当前时间 年月日时分秒
    date3 = (temp_date + datetime.timedelta(days=-day_num)).strftime("%Y-%m-%d %H:%M:%S")
    datetime_obj = datetime.datetime.strptime(date3, "%Y-%m-%d %H:%M:%S")
    # obj_stamp1 = int((time.mktime(datetime_obj.timetuple())) * 1000.0 * 1000)
    obj_stamp1 = int((time.mktime(datetime_obj.timetuple())-160) * 1000.0 * 1000)

    # obj_stamp1 = int(1688266816 * 1000.0 * 1000)  #此处是为了验证旧数据
    return obj_stamp1


def send_config_request(device_id, MD5, app):
    with open(Base_dir+"/"+cfjsonname+"_config_request.json", mode="r", encoding="utf-8") as f:
        json_data = json.load(f)
        # print(json_data)
    # 修改请求数据--------------------

    json_data['ai']['ai'] = MD5
    # json_data['ai']['ci'] = qqudao
    json_data['ai']['av'] = 18
    json_data['di']['di'] = device_id
    json_data['di']['ot'] = ot
    json_data['ai']['at'] = at

    headers = {'X-Real-IP': '39.144.248.200'}
    configurl = url + 'config' + '?v=5110' + '&a=' + MD5 + '&d=' + device_id      # 创建url 可以通过修改内容更换url
    print(configurl)
    data_bytes = json.dumps(json_data)
    print(data_bytes)
    config_response = requests.post(url=configurl,   headers=headers, data=data_bytes)

    global session
    global config_cmt
    session = config_response.json().get("s")
    # session = '9'
    config_cmt = config_response.json().get("st")
    print("config响应:",config_response.json())
    # ----------------------------------------------------
    return config_response.json()

def send_upload_request(upjsonname, MD5, device_id, app, s,c):
    # url1 = Base_dir + "/" + upjsonname + "_upload5_request.json"
    list1 = ["_upload_request.json", "_upload1_request.json", "_upload2_request.json", "_upload3_request.json",
             "_upload4_request.json", "_upload5_request.json", "_upload6_request.json", "_upload7_request.json"]

    url1 = Base_dir + "/" + upjsonname + random.choice(list1)
    print('====================', url1)

    with open(url1 , mode="r", encoding="utf-8") as f:

        json_data = json.load(f)
        json_data['ai']['ai'] = MD5

        # json_data['ai']['ci'] = qqudao
        json_data['ai']['av'] = app
        json_data['di']['di'] = device_id
        json_data['di']['ot'] = ot
        json_data['ai']['at'] = at
        if pt == "b":
            json_data['s'] = device_id
        else:
            json_data['s'] = s
            print('session_id', json_data['s'])
            json_data['cmt'] =config_cmt #str(c+9000000) #config_cmt
        print("--------------------",json_data['ai'])
        print("--------------------",json_data['di'])
        print("--------------------",json_data['s'])
        User_Agent = random.choice(['Mozilla/5.0 (iPad; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15',
                                                      'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57 QQ/6.5.5.0 TIM/2.3.0.401 V1_IPH_SQ_6.5.5_1_TIM_D Pixel/1080 Core/UIWebView Device/Apple(iPhone 8Plus) NetType/WIFI ',
                                                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                                                      'Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; WebView/2.0; rv:11.0; IEMobile/11.0; NOKIA; Lumia 525) like Gecko',
                                                      'Mozilla/5.0 (iPhone; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15',
                                                      'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57 QQ/6.5.5.0 TIM/2.3.0.401 V1_IPH_SQ_6.5.5_1_TIM_D Pixel/1080 Core/UIWebView Device/Apple(iPhone 8Plus) NetType/WIFI',
                                                      'Mozilla/5.0 (iPhone; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15',
                                                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
                                                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
                                                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                                                       "Mozilla/5.0 (iPhone; CPU?iPhone?OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34?Weibo(iPhone8,1__weibo__6.8.1__iphone__os9.3.3) AliApp(BC/2.1) tae_sdk_ios_2.1 havana",
                                                       "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
                                                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
                                                       "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; HTC U-1w Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.2.992 Mobile Safari/537.36",
                                                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36",
                                                       "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
                                                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Shuame; InfoPath.3; Tablet PC 2.0)",
                                                       "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
                                                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
                                                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                                                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
                                                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.3000 Chrome/47.0.2526.73 Safari/537.36",
                                                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
                                                       "Mozilla/5.0 (Linux; Android 8.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044409 Mobile Safari/537.36",
                                                       "Mozilla/5.0 (Linux; Android 6.0; VIE-AL10 Build/HUAWEIVIE-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044504 Mobile Safari/537.36 wxwork/1.3.2 wwlocal/1.3.2 wxworklocal/1.3.2 MicroMessenger/6.3.22",
                                                       "Mozilla/5.0 (Linux; Android 9.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044409 Mobile Safari/537.36 V1_AND_SQ_7.9.8_999_YYB_D QQ/7.9.8.3935 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/72",
                                                       "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57 QQ/6.5.5.0 TIM/2.3.0.401 V1_IPH_SQ_6.5.5_1_TIM_D Pixel/1080 Core/UIWebView Device/Apple(iPhone 8Plus) NetType/WIFI",
                                                       "Mozilla/5.0 (Linux; Android 8.0.0; SM-A9200 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 PPDWebUI/3.0.2 PPDLoanApp/7.1.0 (AppID/10080004; qq)",
                                                       "Mozilla/4.0 (compatible; MSIE 4.0; Windows 95; Trident/4.0; InfoPath.1; SV1; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705)",
                                                       "Mozilla/5.0 (Linux; U; Android 9; zh-cn; STF-AL10 Build/HUAWEISTF-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/9.9 Mobile Safari/537.36",
                                                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
                                                       "Mozilla/5.0 (X11; Linux x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.83",
                                                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0",
                                                       "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
                                                       "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                                                       "Mozilla/5.0 (linux; android 5.1.1; mi note pro build/lmy47v) applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/37.0.0.0 mobile mqqbrowser/6.2 tbs/036215 safari/537.36 micromessenger/6.3.16.49_r03ae324.780 nettype/wifi language/zh_cn",
                                                       "Mozilla/5.0 (iPhone; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15",
                                                       "Mozilla/5.0 (iPhone; CPU?iPhone?OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34?Weibo(iPhone8,1__weibo__6.8.1__iphone__os9.3.3) AliApp(BC/2.1) tae_sdk_ios_2.1 havana",
                                                       "Mozilla/5.0 (X11; Linux x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.111110.3683.103 Safari/537.36"])

        json_data['mt'] = c


        # json_data['mt'] = int(1688266816 * 1000.0 * 1000)   #此处是为了验旧数据
        ip = random.choice(["110.53.72.159", "61.154.187.242", "61.154.131.242", "180.149.130.16",
                            "36.6.215.20", "60.174.35.94", "59.59.48.70", "59.60.183.198", "59.60.10.194",
                            "219.159.239.25", "220.173.239.13", "61.139.250.104", "218.86.254.148", "36.101.188.11",
                            "112.66.142.15", "124.66.124.201", "61.159.10.9", "60.7.236.112", "39.165.68.167",
                            "42.239.5.251", "182.132.79.105", "61.188.114.183", "223.85.82.75", "60.250.12.48",
                            "58.16.147.17", "61.159.140.181", "59.51.197.22", "58.42.187.55", "120.70.15.147",
                            "223.104.187.55", "117.20.113.161", "36.156.77.51", "115.164.77.59","60.250.12.48", "115.164.77.59", "117.20.113.161"])

        net=random.choice(["eth","ctradioaccesstechnologynr", "wifi","iwlan", "ctradioaccesstechnologycdma1x", "gprs"  ])
        "ctradioaccesstechnologynr"  "5G"
        'eth'  "wifi"
        "iwlan" "4G"
        "ctradioaccesstechnologycdma1x" "3G"
        "gprs"  "3G以下"
        print("net------------", net)

        # 构造的rn同批量基线数据
        json_array = [];
        for i in json_data['e']:
            global k
            i['ent'] = c
            # i['ent'] = int(1688266816 * 1000.0 * 1000)   #此处是为了验旧数据
            if i["k"] =="jserror":
                i["v"]["pct"]=c


        data_bytes = json.dumps(json_data)
        data_bytes_last = bytes(data_bytes, encoding='utf8')
        data_gzip = gzip.compress(data_bytes_last) # 创建一个zip请求体
        if pt == "b":
            session = device_id
            print("browser-session：",session)
        else:
            session = s
        uploadurl = url + 'upload' + '?v=5110' + '&a=' + MD5 + '&d=' + device_id+"&s=" + session + "&mt=" + str(c+8000000)+"&if=1"+"&cmt="+str(c+9000000)
        brkey = str(uuid.uuid1()) + '_' + curenttiem  # 创建请求头brkey值
        # brkey ='d01be1ed-bc42-476c-a1f0-83b51d0ff240'
        print("upurl", uploadurl)  # 'X-Real-IP': ip   "User-Agent": User_Agent1
        headers = {"brkey": brkey, "Br-Content-Encoding": "gzip", "User-Agent": User_Agent }
        upload_response = requests.post(url=uploadurl, headers=headers, data=data_gzip)  # 发请求
        r_data = upload_response.content.decode()  # 获取请求内容
        print(r_data)
        return "qw"

if __name__ == "__main__":
    curenttiem = str(int(time.time()))
    Base_dir = os.path.dirname(__file__)  # 获取当前文件路径

    #SDK
    #url = "http://10.241.131.14:39999/"

    #rum_controller 地址
    url = "http://10.241.211.40:58897/RUM/"

    upload_num = 0
    di = str(uuid.uuid1())
    d = 0
    us = [6000000, 240000000]

    pt = random.choice(["a", "l", "m", "z", "h", "w"])
    #pt = 'w'
    print("pt****************", pt)

    # 通过pt来区分不同的应用类型
    # web
    if pt == "z":
        ot = 1  # 「0:iOS,1:Android,2:Windows,3:HarmonyOS,4:Mac」
        at = 4  # 「0:iOS,1:Android,2:Windows,3:HarmonyOS,4:H5,5:小程序」
        cfjsonname = "configios"
        upjsonname = "cc_crash"  # "cc_crash"
        # MD5 = "82ae2983313642698c9be42f43e0e713"
        MD5 = "6f0bb2da45d54ceda454170c4fd5046a"

    # 小程序
    elif pt == "m":
        ot = 1
        at = 5
        cfjsonname = "configios"
        upjsonname = "cc_crash"
        # MD5 = "2eb37f2ff13a424794b10e01f8f9554a"
        MD5 = "e1c39f31d0884c1a87aca677ecb6bb7e"

    # ios
    elif pt == "l":
        ot = 0
        at = 0
        cfjsonname = "configios"
        upjsonname = "cc_crash"
        # MD5 = "dc8b0d25e68d4ebca9add406069c5a52"
        MD5 = "932dc54b02d44b0d8a1bfaeb7bd98080"


    # 安卓
    elif pt == "a":
        ot = 0
        at = 1
        cfjsonname = "configios"
        upjsonname = "cc_crash"
        # MD5 = "d30df7dc7fa74b74aa25a3f180433f42"
        MD5 = "26261c3401634497a0bf00bcc051f5de"

    # 鸿蒙系统
    elif pt == "h":
        ot = 0
        at = 3
        cfjsonname = "configios"
        upjsonname = "cc_crash"
        # MD5 = "a912198e1a9e4b708bc625534bf32963"
        MD5 = "a2addd3297e6438b8474baaf7d875048"

    # windows
    elif pt == "w":
        ot = 1
        at = 2
        cfjsonname = "configios"
        upjsonname = "cc_crash"
        # MD5 = "6f97297943d8477c977e5f7f1c81bb4a"
        MD5 = "0c6c178021984496b010a86243e0024f"


    for i in range(0, 100000000000000000000000000000000000000000000000000000000000000):
        di = "41d02d0756f7d428"#random_str()# ## # #""  "lrz-androiddevice"
        c = time_data(0)
        kk = i
        u = 3000000
        print('config次数：', i)
        time.sleep(1)
        d = i
        # 为什么改app版本的时候要在脚本中改而不是json中改
        app = "18"
        qqudao = "a-41"
        print("设备id：", di)
        n1 = i
        upload_num += 1
        if pt != "b":
            c_response = send_config_request(di, MD5, app)
            json_str = json.dumps(c_response);
        else:
            c_response = {"rc": 10000}
        if c_response.get("rc") == 10000:
            s = c_response.get("s")
            u_response = send_upload_request(upjsonname, MD5, di, app, s, c)

    print('发数据的时间：', time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()-160)))
    print("历史时间", c)
