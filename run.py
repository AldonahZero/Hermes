from email.mime import text
import requests
from bs4 import BeautifulSoup
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import time
import smtplib


import random


import os

def playmucis (path):
    os.system("ffplay  %s"%(path))


def send_server(seckey, tittle, content):
    data = {
        "text": tittle,
        "desp": content
    }
    req = requests.post(f"https://sc.ftqq.com/{seckey}.send", data=data)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(text, link):
    print("send_email()", text, link)
    print(text)
    # 输入Email地址和口令:
    config = [line.strip() for line in open("email_config")]
    from_addr = config[0]
    password = config[1]

    msg = MIMEText(
        f"YY，您好！\n\n监测到您关注的爱马仕商品有上新！\n详细信息：{text}\n商品链接：{link} \n\n 祝好，\nMM",
        'plain', 'utf-8')
    msg["From"] = "毛小毛~"
    msg['To'] = "YY"
    msg['Subject'] = Header('爱马仕上新！').encode()

    # 输入收件人地址:
    to_addr = config[2]

    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    try:
        server.sendmail(from_addr, to_addr, msg.as_string())
    except Exception as e:
        print('邮件发送失败--' + str(e))
    print('邮件发送成功')
    server.quit()


def crawl_item(url):
    # 商品关注列表
    r = requests.get(url)
    if r.status_code == 403:
        print('没上')
        return -1
    if r.status_code == 404:
        print('错误url')
        return -1

    content = r.content
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.title.text)
    txt = soup.find_all(
        "form", {"class": "simple-product-selector"})[0].text.split()
    info = soup.title.text

    # print(soup.find_all("span", {"class": "message-error"}))  
    sorry = soup.find_all(
        "span", {"class": "message-error"})[0].text.startswith("抱歉！")
    if(sorry):
        print('没货')
        return -1
    # 爬到的颜色
    color = [t for t in txt if t.endswith("色")][1]
    error_info = soup.find_all("span", {"class": "message-error"})
    if len(error_info) > 0:
        if "抱歉" in error_info[0].text:
            print(error_info[0].text)
            return 0
    else:
        sendtext = info + " " + color
        # playmucis('./music/qhc.mp3')
        send_email(sendtext, url)
        send_server("SCT77362TUgoMEyQjQBq6YQu1XGMjl6is", "爱马仕上新!",
                    f"YY，您好！\n\n监测到您关注的爱马仕商品有上新！\n详细信息：{sendtext}\n商品链接：{url} \n\n 祝好，\nMM")
        send_server("SCT78377T2usG8PkSBrnTDLsxK4PzM0A9", "爱马仕上新!",
                    f"YY，您好！\n\n监测到您关注的爱马仕商品有上新！\n详细信息：{sendtext}\n商品链接：{url} \n\n 祝好，\nMM")
        return 1


def crawl(url, type):
    # 商品关注列表
    I_want_them = {
        "手提包": ["pico"]
    }

    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content, 'lxml')

    for li in soup.find_all('a'):
        text = li.text.lower()
        if "¥" in text:
            print(text)
            for th in I_want_them[type]:
                if th in text:
                    print("监测内容：", type, th)
                    print(li.text)
                    link = li.get("href")
                    link = "https://www.hermes.cn" + link
                    # playmucis('./music/qhc.mp3')
                    send_email(li.text, link)
                    send_server("SCT77362TUgoMEyQjQBq6YQu1XGMjl6is", "爱马仕上新!",
                                f"YY，您好！\n\n监测到您关注的爱马仕商品有上新！\n详细信息：{li.text}\n商品链接：{link} \n\n 祝好，\nMM")
                    send_server("SCT78377T2usG8PkSBrnTDLsxK4PzM0A9", "爱马仕上新!",
                                f"YY，您好！\n\n监测到您关注的爱马仕商品有上新！\n详细信息：{li.text}\n商品链接：{link} \n\n 祝好，\nMM")
                    # break
                    return 1
    print(f'还没上 {I_want_them[type]}')
    return 0


if __name__ == "__main__":
       # cnt = 0
    # while True:
    #     crawl("https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E6%97%B6%E5%B0%9A%E9%A6%96%E9%A5%B0/%E9%A1%B9%E9%93%BE%E5%9D%A0%E9%A5%B0/#||%E7%B1%BB%E5%88%AB", "项链")
    #     # crawl("https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E6%97%B6%E5%B0%9A%E9%A6%96%E9%A5%B0/%E8%80%B3%E7%8E%AF/#||%E6%9D%90%E8%B4%A8", "耳钉")
    #     cnt += 1
    #     print(f"执行中 ... 循环爬取{cnt}次 ...")
    #     time.sleep(20)
    caturls = [
        "https://www.hermes.cn/cn/zh/category/%E5%A5%B3%E5%A3%AB/%E7%AE%B1%E5%8C%85%E5%B0%8F%E7%9A%AE%E5%85%B7/%E7%AE%B1%E5%8C%85%E6%99%9A%E5%AE%B4%E5%8C%85/#||%E4%BA%A7%E5%93%81%E7%B3%BB%E5%88%97",
    ]
    urls = [
        # "https://www.hermes.cn/cn/zh/product/herbag-zip-31%E5%8F%8C%E8%89%B2%E6%89%8B%E6%8F%90%E5%8C%85-H082270CKAC/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H056289CK08/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H056289CCK1/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18-casaque-%E6%89%8B%E6%8F%90%E5%8C%85-H082321CCAD/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H073597CCD0/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H056289CC08/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H056289CC18/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H056289CK12/",
        "https://www.hermes.cn/cn/zh/product/picotin-lock-18%E6%89%8B%E6%8F%90%E5%8C%85-H056289CK3Q/",
        # 测试项链
        "https://www.hermes.cn/cn/zh/product/pop-h%E8%80%B3%E7%8E%AF-H608001FO55/",
        "https://www.hermes.cn/cn/zh/product/rodeo-pegase%E5%B0%8F%E5%8F%B7%E5%90%8A%E9%A5%B0-H083010CAAB/",
    ]
    cnt = 0
    while True:
        for url in urls:
            print(url)
            crawl_item(url)
            time.sleep(random.randint(2, 4))
        for caturl in caturls:
            print(caturl)
            crawl(caturl, "手提包")
            time.sleep(random.randint(2, 4))
        cnt += 1
        print(f"执行中 ... 循环爬取{cnt}次 ...")
