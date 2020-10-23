# -*- coding: utf-8 -*-
# 作者: 肖凯旋
# 日期：2020/10/17

import bs4
import csv
import os

paths = "./HTML_encryption_2/"
paths_list = os.listdir(paths)

csv_file = open('大众点评评论数据1.csv', 'w+', newline='', encoding='utf-8-sig')
writer = csv.writer(csv_file)
writer.writerow(["User comments"])

for path in paths_list:

    html_path = paths + path

    # './HTML_decrypt_2/04 网页数据_解密.html'

    with open(html_path, mode='r', encoding='utf-8') as f:
        html = f.read()
    print(type(html))

    bs_html = bs4.BeautifulSoup(html, "html.parser")
    print(type(bs_html))

    find_div = bs_html.find_all('div', class_="review-words Hide")

    for i in find_div:
        print(i.text.replace(" ", "").replace("\n", " "))
        writer.writerow([i.text.replace(" ", "").replace("\n", " ")])

csv_file.close()
