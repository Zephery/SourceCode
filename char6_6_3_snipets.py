_author__ = 'pqh'
import spynner

browser = spynner.Browser()
browser.show()
browser.load('http://www.phei.com.cn/module/goods/wssd_content.jsp?bookid=42345',
             load_timeout=60, tries=3)
td_list = browser.webframe.findAllElements('td')

for td in td_list:
    td_text = td.toPlainText()
    if ':' in td_text:
        print(td_text)

browser.close()


import time

#td = browser.search_element_text('著')

begin_index = 0

begin_td = None

#td index = 0
# for td in td_list:
#
#     # if td.attribute('height') == '20':
#     #     txt = td.toPlainText()
#     #     print(td.attribute('height'),txt)
#
#     txt = td.toPlainText()
#     if '著    者：Peter J.Bentley' in txt:
#          print(txt)
#     #print(txt)
#     #print('aaaa')
#     # if '著    者' in txt:
#     #     print('bbbb'+txt)
#     #     begin_td = td
#     #     begin_index = td_list.toList().index(begin_td)
#     #     #print(text,begin_index,'OK')
#     #     break

d = {}
for td in td_list:
    if td.attribute('height') == '20':
        txt = td.toPlainText().replace('\xa0', '')
        if '：' in txt:
            print(txt)
            k = txt.split('：')[0]
            v = txt.split('：')[1]
            d[k] = v
print(d)


def get_instruction(html):
    l_tag = '<td align="left" valign="top" class="line_h24 f12_grey pad_t20 pad_bot20"><p>'
    r_tag = '</p>'
    instruction = ''
    try:
        instruction = html.split(l_tag)[1].split(r_tag)[0]
    except Exception as e:
        print(e)
    return instruction

s = get_instruction(browser.html)
print(s)
#time.sleep(4)
#
# if td != []:
#     begin_index = td_list.index(td[0])

#print(begin_index)
# for i in range(begin_index, begin_index+10):
#     td_text = td_list[i].toPlainText()
#     if '：' in td_text:
#         print(td_text)
browser.close()


