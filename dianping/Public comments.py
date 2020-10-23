import requests
import re
import time
import os

"""
    1.获取评论主页源码
    2.获取css文件
    3.请求svg内容
"""


def homepage_source(url, i):

    session = requests.session()

    print(i, type(i))
    """
    1、首页请求
    p1,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL
    p2,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all
    p3,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p2
    """

    if i == 1:

        header = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "__mta=45470491.1602546510796.1602546510796.1602546510810.2; _lxsdk_cuid=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _lxsdk=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _hc.v=4667963d-25b1-a84e-ae36-6fad1cad6ebb.1600040734; ctu=ddca3145ab4ce75a1cc6e4e7a3e7e337587a7bd7ff22c3de065575127fa015b3; s_ViewType=10; cityid=4481; switchcityflashtoast=1; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1602546487; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1602494163,1602857094; ua=15119738935; cy=4; cye=guangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; fspop=test; dper=d6718e4e8b874dfc9826c7e36e062d395ffb3b8f461071521651f42e8770e3e2c6cfc0150a276d03b92f5de747a8bfd6bae744be72127e13f8a8e0481d099546b63083d3bf37262de2a664488cdeef91a7cf91ab674ed9d1f0d46cde46ea0b5e; dplet=e29fb570c3ed66ed58b188efc69a5d5b",
            "Host": "www.dianping.com",
            "Referer": "http://www.dianping.com/shop/H1gftYnAbRCu9zzL",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }

    elif i == 2:

        header = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "__mta=45470491.1602546510796.1602546510796.1602546510810.2; _lxsdk_cuid=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _lxsdk=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _hc.v=4667963d-25b1-a84e-ae36-6fad1cad6ebb.1600040734; ctu=ddca3145ab4ce75a1cc6e4e7a3e7e337587a7bd7ff22c3de065575127fa015b3; s_ViewType=10; cityid=4481; switchcityflashtoast=1; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1602546487; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1602494163,1602857094; ua=15119738935; cy=4; cye=guangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; fspop=test; dper=d6718e4e8b874dfc9826c7e36e062d395ffb3b8f461071521651f42e8770e3e2c6cfc0150a276d03b92f5de747a8bfd6bae744be72127e13f8a8e0481d099546b63083d3bf37262de2a664488cdeef91a7cf91ab674ed9d1f0d46cde46ea0b5e; dplet=e29fb570c3ed66ed58b188efc69a5d5b",
            "Host": "www.dianping.com",
            "Referer": "http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }

    else:
        Referer = "http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p" + str(i - 1)
        print(Referer)

        header = {
            "Connection": "keep-alive",
            "Cookie": "__mta=45470491.1602546510796.1602546510796.1602546510810.2; _lxsdk_cuid=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _lxsdk=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _hc.v=4667963d-25b1-a84e-ae36-6fad1cad6ebb.1600040734; ctu=ddca3145ab4ce75a1cc6e4e7a3e7e337587a7bd7ff22c3de065575127fa015b3; s_ViewType=10; cityid=4481; switchcityflashtoast=1; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1602546487; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1602494163,1602857094; ua=15119738935; cy=4; cye=guangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; fspop=test; dper=d6718e4e8b874dfc9826c7e36e062d395ffb3b8f461071521651f42e8770e3e2c6cfc0150a276d03b92f5de747a8bfd6bae744be72127e13f8a8e0481d099546b63083d3bf37262de2a664488cdeef91a7cf91ab674ed9d1f0d46cde46ea0b5e; dplet=e29fb570c3ed66ed58b188efc69a5d5b",
            "Host": "www.dianping.com",
            "Referer": Referer,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }

    response = session.get(url, headers=header)
    print("----抓包中----\t", response.status_code)

    # 保存源码，避免IP被封
    with open("./HTML_encryption_2/%.2d 网页数据_加密.html" % i, mode="w", encoding="utf-8") as f:
        f.write(response.text)


def css_requests():

    path = "./HTML_encryption_2/"
    path_list = os.listdir(path)

    for html in path_list:

        html_path = path + html

        if ".html" not in html:
            continue

        # 再次读取源码
        with open(html_path, mode="r", encoding="utf-8") as f:
            response = f.read()

        try:
            css_url = re.findall('<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.*?)">', response)
            css_url = 'http:' + css_url[0]
            print(css_url)

        except Exception as e:
            print(html_path)

        f.close()

    # css样式数据获取
    css_response = requests.get(css_url)

    # 保存
    with open("./HTML_encryption_2/css样式.css", mode="w", encoding="utf-8") as f:
        f.write(css_response.text)


def css_to_svg():

    """3.svg数据请求"""

    # 读取
    with open("./HTML_encryption_2/css样式.css", mode="r", encoding="utf-8") as f:
        css_response = f.read()

    svg_url = re.findall(r'svgmtsi\[class\^="xfh"\].*?background-image: url\((.*?)\);', css_response)
    # svg_url_1 = re.findall(r'svgmtsi\[class\^="xfh"\].*?background-image: url\((.*?)\);', css_response)
    svg_url = 'http:' + svg_url[0]

    print(svg_url)

    # 3、svg数据请求
    svg_response = requests.get(svg_url)

    with open('./HTML_encryption_2/svg映射表.svg', mode="w", encoding="utf-8") as f:
        f.write(svg_response.text)


if __name__ == "__main__":

    """
    评论主页的源码请求
    p1,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL
    p2,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all
    p3,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p2
    ...
    """
    # url = "http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p"
    # for i in range(1, 371):
    #     url_1 = url + str(i)
    #     homepage_source(url_1, i)
    #     time.sleep(5)

    """
    读取源码找到css文件
    """
    # css_requests()
    """
    3.svg数据请求
    """
    css_to_svg()




