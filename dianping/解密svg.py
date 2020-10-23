# -*- coding: utf-8 -*-
# 作者: 肖凯旋
# 日期：2020/10/17

import parsel
import re

with open('03 svg映射表.svg', mode='r', encoding='utf-8') as f:
    svg_html = f.read()

sel = parsel.Selector(svg_html)


# 加载映射规则表
texts = sel.css('text')
print(texts)
lines = []
for text in texts:
    # print(text.css('text::text').get())
    # print(text.css('text::attr(y)').get())
    lines.append([text.css('text::attr(y)').get(), text.css('text::text').get()])


# 获取所有的类名与位置
with open('02 css样式.css', mode='r', encoding='utf-8') as f:
    css_text = f.read()

class_map = re.findall('\\.(fg\\w+){background:-(\\d+).0px -(\\d+)\\.0px;\\}', css_text)
# print(class_map)

class_map = [(cls_name, int(x), int(y)) for cls_name, x, y in class_map]
print(class_map)
print(lines)

d_map = {}

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

with open('./HTML_encryption/02 网页数据_加密.html', mode='r', encoding='utf-8') as f:
    html = f.read()

for key, value, in d_map.items():
    html = html.replace('<svgmtsi class="' + key + '"></svgmtsi>', value)

with open('./HTML解密/02 网页数据_解密.html', mode='w', encoding='utf-8') as f:
    f.write(html)

