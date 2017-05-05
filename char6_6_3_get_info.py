import spynner
import glob
import xlwt3

#1
def get_instruction(html):
    l_tag = '<td align="left" valign="top" class="line_h24 f12_grey pad_t20 pad_bot20"><p>'
    r_tag = '</p>'
    instruction = '----'
    try:
        instruction = html.split(l_tag)[1].split(r_tag)[0]
    except Exception as e:
        print('instruction:', e)
    return instruction

def get_val_from_dict(d,k):
    try:
        return d[k]
    except Exception as e:
        print(k,e)
        return '----'

#2
browser = spynner.Browser()
browser.show()
#3
files_list = glob.glob('./htmls/*.html')
key_names = ['书名','作译者','出版时间','千字数','版次','页数','开本','价格','内容简介']
all_recs = []
all_recs.append(key_names)

#4
for file_name in files_list:
    book_name = file_name.split('.html')[0].replace('./htmls/','')
    f = open(file_name, 'r')
    html_str = f.read()
    f.close()
    #5
    browser.webview.setHtml(html_str)
    browser.wait(1)
    #6
    try:
        td_list = browser.webframe.findAllElements('td')
        d = {}
        d['书名'] = book_name
        print(file_name)
        for td in td_list:
            if td.attribute('height') == '20':
                txt = td.toPlainText().replace('\xa0', '').replace(' ','').replace('\t','')
                if '：' in txt:
                    k = txt.split('：')[0]
                    v = txt.split('：')[1]
                    d[k] = v
        d['价格'] = html_str.split('纸质书定价：￥')[1].split('<span class="f12_red">会员价')[0].replace('&nbsp;&nbsp;&nbsp;','')
        instruction = get_instruction(html_str)
        d['内容简介']=instruction
        all_recs.append([get_val_from_dict(d,kname) for kname in key_names])
    except Exception as e:
        print(e)
        continue
#7
wb=xlwt3.Workbook()
sheet=wb.add_sheet("图书信息")
for i in range(0,len(all_recs)):
    for j in range(0, len(all_recs[i])):
        sheet.write(i, j, all_recs[i][j])
wb.save("图书信息_04_16.xls")
browser.close()





# import spynner
# import glob
# import xlwt3
#
# #1
# def get_instruction(html):
#     l_tag = '<td align="left" valign="top" class="line_h24 f12_grey pad_t20 pad_bot20"><p>'
#     r_tag = '</p>'
#     instruction = '----'
#     try:
#         instruction = html.split(l_tag)[1].split(r_tag)[0]
#     except Exception as e:
#         print('instruction:', e)
#     return instruction
#
# def get_val_from_dict(d,k):
#     try:
#         return d[k]
#     except Exception as e:
#         print(k,e)
#         return '----'
#
# #2
# browser = spynner.Browser()
# browser.show()
# #3
# files_list = glob.glob('./htmls/*.html')
# key_names = ['书名','作译者','出版时间','千字数','版次','页数','开本','价格','内容简介']
# all_recs = []
# all_recs.append(key_names)
#
# #4
# for file_name in files_list:
#     book_name = file_name.split('.html')[0].replace('./htmls/','')
#     f = open(file_name, 'r')
#     html_str = f.read()
#     f.close()
#     #5
#     browser.webview.setHtml(html_str)
#     browser.wait(1)
#     #6
#
#     try:
#
#         td_list = browser.webframe.findAllElements('td')
#         d = {}
#         d['书名'] = book_name
#         print(file_name)
#         for td in td_list:
#             if td.attribute('height') == '20':
#                 txt = td.toPlainText().replace('\xa0', '').replace(' ','').replace('\t','')
#                 if '：' in txt:
#                     k = txt.split('：')[0]
#                     v = txt.split('：')[1]
#                     d[k] = v
#         # 纸质书定价：￥36.8
#         # <span class="f12_red">会员价：￥29.44
#         d['价格'] = html_str.split('纸质书定价：￥')[1].split('<span class="f12_red">会员价')[0].replace('&nbsp;&nbsp;&nbsp;','')
#         instruction = get_instruction(html_str)
#         d['内容简介']=instruction
#         all_recs.append([get_val_from_dict(d,kname) for kname in key_names])
#     except Exception as e:
#         print(e)
#         continue
# #7
# wb=xlwt3.Workbook()
# sheet=wb.add_sheet("图书信息")
# for i in range(0,len(all_recs)):
#     for j in range(0,len(all_recs[i])):
#         sheet.write(i,j,all_recs[i][j])
# wb.save("图书信息_04_16.xls")
# browser.close()



# __author__ = 'pqh'
# import spynner
# import time
# import glob
# import xlwt3
# def get_instruction(html):
#     l_tag = '<td align="left" valign="top" class="line_h24 f12_grey pad_t20 pad_bot20"><p>'
#     r_tag = '</p>'
#     instruction = '----'
#     try:
#         instruction = html.split(l_tag)[1].split(r_tag)[0]
#     except Exception as e:
#         print('instruction:', e)
#     return instruction
#
# def get_val_from_dict(d,k):
#     try:
#         return d[k]
#     except Exception as e:
#         print(k,e)
#         return '----'
#
# #作译者,出版时间,千字数,版次,页数,开本,装帧,ISBN
#
# files_list = glob.glob('./htmls/*.html')
# print(len(files_list))
# browser = spynner.Browser()
# browser.show()
# key_names = ['书名', '作译者', '出版时间', '千字数', '版次', '页数', '开本', '内容简介']
# all_recs = []
# all_recs.append(key_names)
# i = 1
# for file_name in files_list[0:1]:
#     book_name = file_name.split('.html')[0].replace('./htmls/','')
#     f = open(file_name, 'r')
#     html_str = f.read()
#     f.close()
#     #browser.webview.show()
#     browser.webview.setHtml(html_str)
#     browser.wait(1)
#     #
#     td_list = browser.webframe.findAllElements('td')
#     d = {}
#     d['书名'] = book_name
#     print(file_name)
#     for td in td_list:
#         if td.attribute('height') == '20':
#             txt = td.toPlainText().replace('\xa0', '').replace(' ','').replace('\t','')
#             print(txt)
#             if '：' in txt:
#                 #print(txt)
#                 k = txt.split('：')[0]
#                 v = txt.split('：')[1]
#                 d[k] = v
#
#     instruction = get_instruction(html_str)
#     d['内容简介']=instruction
#     print(d.keys())
#     all_recs.append([get_val_from_dict(d,kname) for kname in key_names])
#     #print(d)
#     print(all_recs[i])
#     ##print(all_recs)
#     #print(book_name)
#
# wb=xlwt3.Workbook()
# sheet=wb.add_sheet("图书信息")
# for i in range(0,len(all_recs)):
#     for j in range(0,len(all_recs[i])):
#         sheet.write(i,j,all_recs[i][j])
# wb.save("图书信息.xls")
#
# print(all_recs[1])
#
# browser.close()

#browser.load('http://www.phei.com.cn/module/goods/wssd_content.jsp?bookid=42345', load_timeout=60, tries=3)
# td_list = browser.webframe.findAllElements('td')
#
#
#
# d = {}
# for td in td_list:
#     if td.attribute('height') == '20':
#         txt = td.toPlainText().replace('\xa0', '')
#         if '：' in txt:
#             print(txt)
#             k = txt.split('：')[0]
#             v = txt.split('：')[1]
#             d[k] = v

# __author__ = 'pqh'
# import spynner
# import time
# import glob
# def get_instruction(html):
#     l_tag = '<td align="left" valign="top" class="line_h24 f12_grey pad_t20 pad_bot20"><p>'
#     r_tag = '</p>'
#     instruction = ''
#     try:
#         instruction = html.split(l_tag)[1].split(r_tag)[0]
#     except Exception as e:
#         print(e)
#     return instruction
#
# files_list = glob.glob('./htmls/*.html')
#
# browser = spynner.Browser()
#
# browser.show()
# from PyQt4 import QtCore
# from PyQt4.QtCore import SIGNAL, QUrl, Qt, QEvent
# for file_name in files_list:
#     f = open(file_name, 'r')
#     html_str = f.read()
#     #browser.load('file:///home/pqh/My_Study_Work/my_Research/book_code/book_code/htmls/3G%E6%99%BA%E8%83%BD%E6%89%8B%E6%9C%BA%E5%88%9B%E6%84%8F%E8%AE%BE%E8%AE%A1%E2%80%94%E2%80%94%E9%A6%96%E5%B1%8A%E5%8C%97%E4%BA%AC%E5%B8%82%E5%A4%A7%E5%AD%A6%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%BA%94%E7%94%A8%E5%A4%A7%E8%B5%9B%E8%8E%B7%E5%A5%96%E4%BD%9C%E5%93%81%E7%B2%BE%E9%80%89_22874.html', load_timeout=60, tries=3)
#     #url = 'file:///home/pqh/My_Study_Work/my_Research/book_code/book_code/htmls/3G%E6%99%BA%E8%83%BD%E6%89%8B%E6%9C%BA%E5%88%9B%E6%84%8F%E8%AE%BE%E8%AE%A1%E2%80%94%E2%80%94%E9%A6%96%E5%B1%8A%E5%8C%97%E4%BA%AC%E5%B8%82%E5%A4%A7%E5%AD%A6%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%BA%94%E7%94%A8%E5%A4%A7%E8%B5%9B%E8%8E%B7%E5%A5%96%E4%BD%9C%E5%93%81%E7%B2%BE%E9%80%89_22874.html'
#     #url = './htmls/3G%E6%99%BA%E8%83%BD%E6%89%8B%E6%9C%BA%E5%88%9B%E6%84%8F%E8%AE%BE%E8%AE%A1%E2%80%94%E2%80%94%E9%A6%96%E5%B1%8A%E5%8C%97%E4%BA%AC%E5%B8%82%E5%A4%A7%E5%AD%A6%E7%94%9F%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%BA%94%E7%94%A8%E5%A4%A7%E8%B5%9B%E8%8E%B7%E5%A5%96%E4%BD%9C%E5%93%81%E7%B2%BE%E9%80%89_22874.html'
#     #QtCore.QUrl(url)
#
#     #QtCore.QUrl("qrc:///"+url)
#
#     # browser.webview.load(QtCore.QUrl(url))
#     browser.webview.setHtml(html_str)
#     browser.webview.show()
#     td_list = browser.webframe.findAllElements('td')
#     d = {}
#     for td in td_list:
#         if td.attribute('height') == '20':
#             txt = td.toPlainText().replace('\xa0', '')
#             if '：' in txt:
#                 print(txt)
#                 k = txt.split('：')[0]
#                 v = txt.split('：')[1]
#                 d[k] = v
#     #print(browser.html)
#     print('ggg')
#     browser.wait(20)
#     f.close()
#
# browser.close()
#
# #browser.load('http://www.phei.com.cn/module/goods/wssd_content.jsp?bookid=42345', load_timeout=60, tries=3)
# # td_list = browser.webframe.findAllElements('td')
# #
# #
# #
# # d = {}
# # for td in td_list:
# #     if td.attribute('height') == '20':
# #         txt = td.toPlainText().replace('\xa0', '')
# #         if '：' in txt:
# #             print(txt)
# #             k = txt.split('：')[0]
# #             v = txt.split('：')[1]
# #             d[k] = v

