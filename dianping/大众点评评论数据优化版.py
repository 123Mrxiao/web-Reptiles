# -*- coding: utf-8 -*-
# 作者: 肖凯旋
# 日期：2020/10/22

import requests
import re
import time
import os
import parsel
import csv
import shutil
import bs4

"""
    1.获取评论主页源码
    2.获取css文件
    3.请求svg内容
"""


def css_requests(response):

    csv_file = open('大众点评评论数据2.csv', 'a+', newline='', encoding='utf-8-sig')
    writer = csv.writer(csv_file)

    s = re.findall(
        '<link rel="stylesheet" type="text/css" href="//s3plus.meituan.net/v1/.*?/svgtextcss/(.*?).css">',
        response)

    try:

        # CSS文件
        with open('./test/{0}_css样式.css'.format(s[0]), mode='r', encoding='utf-8') as f:
            css_html = f.read()
        f.close()

        # SVG文件
        with open('./test/{0}_svg样式.svg'.format(s[0]), mode='r', encoding='utf-8') as f:
            svg_html = f.read()
        f.close()

    except FileNotFoundError:

        shutil.rmtree('./test')
        os.mkdir('test')

        css_url = re.findall('<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.*?)">', response)
        css_url = 'http:' + css_url[0]
        css_response = requests.get(css_url)

        # svg的url是定时变换的，需要根据网页来修改 #
        # svg_url = re.findall(r'svgmtsi\[class\^="xfh"\].*?background-image: url\((.*?)\);', css_response.text)
        svg_url = re.findall(r'svgmtsi\[class\^="rp"\].*?background-image: url\((.*?)\);', css_response.text)
        svg_url = 'http:' + svg_url[0]
        svg_response = requests.get(svg_url)

        with open('./test/{0}_css样式.css'.format(s[0]), mode='w', encoding='utf-8') as f:
            f.write(css_response.text)
        f.close()

        with open('./test/{0}_svg样式.svg'.format(s[0]), mode='w', encoding='utf-8') as f:
            f.write(svg_response.text)
        f.close()

    except Exception as e:
        print(e)

    # CSS数据
    # svg的url是定时变换的，需要根据网页来修改 #
    class_map = re.findall('\\.(rp\\w+){background:-(\\d+).0px -(\\d+)\\.0px;\\}', css_html)
    class_map = [(cls_name, int(x), int(y)) for cls_name, x, y in class_map]
    print("类名，x坐标，y坐标：", class_map)

    # SVG数据

    d_map = {}

    if svg_html.find('textPath') != -1:
        path_lines = re.findall('<path id="(.*?)" d="M0 (.*?) H600"/>', svg_html)
        path_lines = [(int(id_), int(d)) for id_, d in path_lines]
        print("id与d:", path_lines)

        lines = []
        id_to_text = re.findall('<textPath xlink:href="#(\\d+)" textLength=".*?">(.*?)</textPath>', svg_html)
        for x in id_to_text:
            lines.append(list(x))

        print("textPath id 与 数据:", lines)

        for one_char in class_map:
            cls_name, x, y = one_char
            # print(cls_name, x, y)
            for path_line in path_lines:
                id_, d = path_line
                # print(id_, d)
                if d < y:
                    pass
                else:
                    # print(y, d, id_)
                    for line in lines:
                        text_id, text = line

                        if int(text_id) == int(id_):
                            # print(id_, text_id, text)

                            index = (x / 14)
                            char = text[int(index)]

                            # print("第%s行，Text为：%s" % (text_id, text))
                            # print("第%d个字符，char值为：%s\n" % (index, char))

                            d_map[cls_name] = char
                    break

        print(d_map)

    elif svg_html.find('text') != -1:
        sel = parsel.Selector(svg_html)

        # 加载映射规则表
        texts = sel.css('text')
        lines = []
        for text in texts:
            # print(text.css('text::text').get())
            # print(text.css('text::attr(y)').get())
            lines.append([text.css('text::attr(y)').get(), text.css('text::text').get()])

        print(lines)

        # 获取类名与汉字的对应关系
        for one_char in class_map:
            try:
                cls_name, x, y = one_char
                # print(one_char)
                for line in lines:
                    # print(line)

                    # char y > line y
                    if int(line[0]) < y:
                        pass

                    else:
                        index = int(x / 14)
                        char = line[1][index]
                        print("当前待匹配的字符串：", one_char)
                        print("当前待匹配的行：", line)
                        print(cls_name, char)
                        # 当匹配到一个字符后，结束当前循环，匹配下一个

                        d_map[cls_name] = char
                        break

            except Exception as e:
                print(e)

        print(d_map)

        for key, value, in d_map.items():
            html = response.replace('<svgmtsi class="' + key + '"></svgmtsi>', value)

        bs_html = bs4.BeautifulSoup(html, "html.parser")

        find_div = bs_html.find_all('div', class_="review-words Hide")

        for i in find_div:
            print(i.text.replace(" ", "").replace("\n", " "))
            writer.writerow([i.text.replace(" ", "").replace("\n", " ")])

    csv_file.close()


def homepage_source(url, header):

    session = requests.session()
    """
    1、首页请求
    p1,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL
    p2,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all
    p3,Referer: http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p2
    """

    response = session.get(url, headers=header)
    print("----抓包中----\t", response.status_code)

    # 保存源码，避免IP被封
    # with open("./HTML_encryption_2/%.2d 网页数据_加密.html" % i, mode="w", encoding="utf-8") as f:
    #     f.write(response.text)

    css_requests(response.text)


def headers_():

    url = "http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p"

    for i in range(3, 371):

        url_1 = url + str(i)

        if i == 1:

            Referer = "http://www.dianping.com/shop/H1gftYnAbRCu9zzL"

        elif i == 2:

            Referer = "http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all"

        else:

            Referer = "http://www.dianping.com/shop/H1gftYnAbRCu9zzL/review_all/p" + str(i - 1)

        header = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "__mta=45470491.1602546510796.1602546510796.1602546510810.2; _lxsdk_cuid=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _lxsdk=17489dc0c22c8-09fc718733c0ad-333769-1fa400-17489dc0c22c8; _hc.v=4667963d-25b1-a84e-ae36-6fad1cad6ebb.1600040734; ctu=ddca3145ab4ce75a1cc6e4e7a3e7e337587a7bd7ff22c3de065575127fa015b3; s_ViewType=10; cityid=4481; switchcityflashtoast=1; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1602546487; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1602494163,1602857094; ua=15119738935; cy=4; cye=guangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; fspop=test; lgtoken=062566c67-dda2-4dec-9b9b-fb8124081bc2; dper=d6718e4e8b874dfc9826c7e36e062d391892e4907c858a33a9b16e8080eaac06aa7b141b8ad493a1ab7c49343b3259f7eee1e281844912a9605a9fcb8fc14fe91cfaf7b6302e13e054763451fe9d42362afc91ab1177b9aabff93fe6cae7b47e; dplet=612898980ca36a87b20cc3853da10f79",
            "Host": "www.dianping.com",
            "Referer": Referer,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }

        homepage_source(url_1, header)
        time.sleep(5)


if __name__ == "__main__":

    headers_()
