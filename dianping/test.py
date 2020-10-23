# -*- coding: utf-8 -*-
# 作者: 肖凯旋
# 日期：2020/10/18

import parsel
import re
import os

msg = r"""
                                                          _ooOoo_
                                                         o8888888o
                                                         88" . "88
                                                         (| -_- |)
                                                          O\ = /O
                                                      ____/`---'\____
                                                    .   ' \\| |// `.
                                                     / \\||| : |||// \
                                                   / _||||| -:- |||||- \
                                                     | | \\\ - /// | |
                                                   | \_| ''\---/'' | |
                                                    \ .-\__ `-` ___/-. /
                                                 ___`. .' /--.--\ `. . __
                                              ."" '< `.___\_<|>_/___.' >'"".
                                             | | : `- \`.;`\ _ /`;.`/ - ` : | |
                                               \ \ `-. \_ __\ /__ _/ .-` / /
                                       ======`-.____`-.___\_____/___.-`____.-'======
                                                          `=---='

                                       .............................................
                                              佛祖保佑             永无BUG
                                       .............................................
                                           Everything is ok，No bugs in the code.

"""

print(msg)

with open('./HTML_encryption_2/svg映射表.svg', mode='r', encoding='utf-8') as f:
    svg_html = f.read()


path_lines = re.findall('<path id="(.*?)" d="M0 (.*?) H600"/>', svg_html)
path_lines = [(int(id_), int(d)) for id_, d in path_lines]
print("id与d:", path_lines)

lines = []
id_to_text = re.findall('<textPath xlink:href="#(\\d+)" textLength=".*?">(.*?)</textPath>', svg_html)
for x in id_to_text:
    lines.append(list(x))

print("textPath id 与 数据:", lines)


# 获取所有的类名与位置
with open('./HTML_encryption_2/css样式.css', mode='r', encoding='utf-8') as f:
    css_text = f.read()

class_map = re.findall('\\.(xfh\\w+){background:-(\\d+).0px -(\\d+)\\.0px;\\}', css_text)
class_map = [(cls_name, int(x), int(y)) for cls_name, x, y in class_map]
print("类名，x坐标，y坐标：", class_map)

d_map = {}

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

paths = "./HTML_encryption_2/"
paths_list = os.listdir(paths)

for path in paths_list:

    if '.html' in path:
        html_path = paths + path

        with open(html_path, mode='r', encoding='utf-8') as f:
            html = f.read()

        for key, value in d_map.items():
            html = html.replace('<svgmtsi class="' + key + '"></svgmtsi>', value)

        with open('./HTML_decrypt_2/' + path.replace("加", "解"), mode='w', encoding='utf-8') as f:
            f.write(html)
