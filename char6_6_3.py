__author__ = 'pqh'

import spynner
#
browser = spynner.Browser()

browser.show()
#http://www.phei.com.cn/module/goods/searchkey.jsp?Page=1&Page=2&searchKey=计算机

urls = []

for i in range(1, 86):
    urls.append('http://www.phei.com.cn/module/goods/searchkey.jsp?Page='
                +str(i)+
                '&Page=2&searchKey=计算机')
print(urls)
all_href_list = []
for url in urls:
    browser.load(url, load_timeout=60)
    a_list = browser.webframe.findAllElements('a')
    needed_list = []
    for a in a_list:
        href_val = a.attribute('href')
        title = a.toPlainText()
        if 'bookid' in href_val and 'shopcar0.jsp' not in href_val and title != '':
            if [title, href_val] not in needed_list:
                needed_list.append([title, href_val])
    all_href_list += needed_list

all_href_file = open('all_hrefs.txt', 'w')

for href in all_href_list:
    all_href_file.write('\t'.join(href)+'\n')

all_href_file.close()

for href_ in all_href_list:
    print(href_)

browser.close()

# urls = []
#
# for i in range(1, 86):
#     urls.append('http://www.phei.com.cn/module/goods/searchkey.jsp?Page='
#                 +str(i)+
#                 '&Page=2&searchKey=计算机')




#print(urls)
