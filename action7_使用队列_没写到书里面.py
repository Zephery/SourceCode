__author__ = 'pqh'

from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import queue
import os
from glob import glob
import xlwt3
import xlrd
#from threading import Thread, Lock


categories = {
    '计算机基础':('1096',31),
    '图形图像':('1097',80),
    '编程语言':('1098',68),
    '网络与互联网':('1099',33),
    '办公软件':('1100',22),
    '计算机科学':('1101',27),
    '辅助设计':('1102', 13),
    '操作系统':('1103',19),
    '计算机硬件':('1104',6),
    '多媒体技术':('1105',8),
    '信息安全':('1106',9),
    '数据库':('1107',10),
}

#http://www.phei.com.cn/module/goods/jsjts_list.jsp?Page=2&Page=2&btid=1107&desc=0&desc1=0&desc2=0&sort=&goodtypename=计算机
url_part_1 = 'http://www.phei.com.cn/module/goods/jsjts_list.jsp?Page='
url_part_2 = '&Page=2&btid='
url_part_3 = '&desc=0&desc1=0&desc2=0&sort=&goodtypename=计算机'

base_url = 'http://www.phei.com.cn/'

my_lock = threading.Lock()

def init_webdriver(webdriver):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("permissions.default.stylesheet", 2)
        firefox_profile.set_preference("permissions.default.image", 2)
        firefox_profile.set_preference("permissions.default.script", 2)
        firefox_profile.set_preference("permissions.default.subdocument", 2)
        firefox_profile.set_preference("javascript.enabled", False)
        firefox_profile.update_preferences()

        with my_lock:
            #init this driver
            #driver = webdriver.Firefox()

            #browser = webdriver.Remote(browser_profile=firefox_profile, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX, command_executor=remote)
            webdriver = webdriver.Firefox(firefox_profile=firefox_profile)
        webdriver.set_page_load_timeout(300)

        return webdriver

# def get(key_name):
#
#     tid,pnum = categories[key_name]
#
#     #生成urls列表
#
#     urls = []
#
#     for i in range(1,pnum+1):
#         url = url_part_1+str(i)+url_part_2+tid+url_part_3
#         urls.append(url)

def get_val_by_name(bs, name):

    name_node= bs.find(name)

    val_node = name_node.nextSibling

    val = ''

    if val_node is not None:

        val = val_node.get_text()


    return val

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
        print(k, e)
        return '----'

class Crawler(threading.Thread):

    # def __init__(self,urls_queue,urls_dir,pages_queue,page_info_dir,webdriver):
    def __init__(self,urls_queue,urls_dir,pages_queue,webdriver):
        threading.Thread.__init__(self)
        self.urls_queue = urls_queue
        self.page_urls_dir = urls_dir
        #self.page_info_dir = page_info_dir
        self.pages_queue = pages_queue
        self.webdriver = init_webdriver(webdriver)
        self.cnt = 0

    # def init_webdriver(self,webdriver):
    #     firefox_profile = webdriver.FirefoxProfile()
    #     firefox_profile.set_preference("permissions.default.stylesheet", 2)
    #     firefox_profile.set_preference("permissions.default.image", 2)
    #     firefox_profile.set_preference("permissions.default.script", 2)
    #     firefox_profile.set_preference("permissions.default.subdocument", 2)
    #     firefox_profile.set_preference("javascript.enabled", False)
    #     firefox_profile.update_preferences()
    #
    #     with my_lock:
    #         #init this driver
    #         #driver = webdriver.Firefox()
    #
    #         #browser = webdriver.Remote(browser_profile=firefox_profile, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX, command_executor=remote)
    #         webdriver = webdriver.Firefox(firefox_profile=firefox_profile)
    #     webdriver.set_page_load_timeout(60)
    #     return webdriver

    def run(self):

        while True:

            url = self.urls_queue.get()

            self.webdriver.get(url)

            fname = url.split(url_part_1)[1].split(url_part_2)[0]

            with open(self.page_urls_dir+'/'+fname+'.html','w') as f:
                f.write(self.webdriver.page_source)



            #grabs urls of hosts and then grabs chunk of webpage
            # url = urllib2.urlopen(host)
            # chunk = url.read()

            #place chunk into out queue
            self.pages_queue.put(self.webdriver.page_source)

            #signals to queue job is done
            self.urls_queue.task_done()

            self.cnt +=1

    def quit(self):

        self.webdriver.quit()

class Analyst(threading.Thread):

    def __init__(self,pages_queue,page_content_dir,webdriver):
        threading.Thread.__init__(self)
        self.pages_queue = pages_queue
        self.webdriver = init_webdriver(webdriver)
        self.page_content_dir = page_content_dir
        self.cnt = 1



    def get_hrefs(self,html_str):

        bs = BeautifulSoup(html_str)

        urls_lst = []

        divs = bs.find_all('div')

        for div in divs:

            a_lst = div.find_all('a')

            for a in a_lst:

                if a['href'] not in urls_lst and 'bookid=' in a['href'] and 'num=1' not in a['href']:

                    urls_lst.append(a['href'])


        print(str(len(urls_lst)))

        return urls_lst


    def run(self):

        while True:

            page_source = self.pages_queue.get()

            href_lst = self.get_hrefs(page_source)

            for href in href_lst:

                url = base_url + href

                self.webdriver.get(url)

                fname = url.split('bookid=')[1]

                with open(self.page_content_dir+'/'+fname+'.html','w') as f:
                    f.write(self.webdriver.page_source)

                #self.cnt

            self.pages_queue.task_done()



    def quit(self):

        self.webdriver.quit()




class ExtractInfo(threading.Thread):

    def __init__(self, page_content_dir):
        threading.Thread.__init__(self)

        self.page_content_dir = page_content_dir


    def run(self):

        files_list = glob(self.page_content_dir+'/'+'*.html')
        key_names = ['书名','作译者','出版时间','千字数','版次','页数','开本','价格','内容简介']
        all_recs = []
        all_recs.append(key_names)

        #4
        for file_name in files_list:
            book_name = file_name.split('.html')[0].replace('./'+self.page_content_dir+'/','')

            f = open(file_name, 'r')
            #print(file_name)
            html_str = f.read()
            f.close()
            #5
            # browser.webview.setHtml(html_str)
            # browser.wait(1)
            #6
            try:
                # td_list = browser.webframe.findAllElements('td')
                td_list = BeautifulSoup(html_str).find_all('td')
                #print(td_list)
                d = {}
                d['书名'] = book_name
                #print(file_name)
                for td in td_list:
                    if 'height' in td.attrs:
                        if td['height'] == '20':
                            txt = td.get_text().replace('\xa0', '').replace(' ','').replace('\t','')
                            if '：' in txt:
                                k = txt.split('：')[0]
                                v = txt.split('：')[1]
                                d[k] = v
                                #print(k,v)
                d['价格'] = html_str.split('纸质书定价：￥')[1].split('<span class="f12_red">会员价')[0].replace('&nbsp;&nbsp;&nbsp;','')
                #print(book_name, d['价格'])
                #instruction = get_instruction(html_str)
                instruction = BeautifulSoup(html_str).find('div', attrs = {'id': 'neirong'}).get_text()
                d['内容简介'] = instruction.replace('\t','').replace('\n','').replace(' ','')
                #print(d['内容简介'])
                #print([get_val_from_dict(d, kname) for kname in key_names])
                all_recs.append([get_val_from_dict(d, kname) for kname in key_names])
            except Exception as e:
                print(book_name, e)
                continue
        #7
        wb=xlwt3.Workbook()
        sheet=wb.add_sheet("图书信息")
        for i in range(0, len(all_recs)):
            for j in range(0, len(all_recs[i])):
                sheet.write(i, j, all_recs[i][j])
                #print(all_recs[i][j])
        #wb.save("图书信息_04_16.xls")
        print('save:'+self.page_content_dir,' '+str(len(all_recs)))
        wb.save(self.page_content_dir+".xls")

class ThreadSchedule(threading.Thread):

    def __init__(self, category_name):
        threading.Thread.__init__(self)
        self.urls_queue = queue.Queue()
        self.pages_queue = queue.Queue()
        self.url_lst = self.get_urls_lst(category_name)
        self.category = category_name
        self.urls_dir = category_name+'_urls'
        self.pages_dir = category_name+'_pages'
        os.makedirs(category_name+'_urls', exist_ok = True)
        os.makedirs(category_name+'_pages', exist_ok = True)

        self.crawler = Crawler(self.urls_queue, self.urls_dir, self.pages_queue, webdriver)
        self.analyst = Analyst(self.pages_queue, self.pages_dir, webdriver)

    def get_urls_lst(self,name):

        tid,pnum = categories[name]

        #生成urls列表

        urls = []

        for i in range(1,pnum+1):
            url = url_part_1+str(i)+url_part_2+tid+url_part_3
            urls.append(url)

        return urls

    def run(self):

        self.crawler.setDaemon(True)
        self.crawler.start()

        for url in self.url_lst:
            self.urls_queue.put(url)

        self.analyst.setDaemon(True)
        self.analyst.start()

        self.urls_queue.join()
        self.pages_queue.join()

        self.crawler.quit()
        self.analyst.quit()

        print(self.category+':Urls 数量:', self.crawler.cnt)
        print(self.category+':Pages 数量:', self.analyst.cnt)


'''
    抓取
'''

# threads_lst = []
#
# for key in categories.keys():
#     thread = ThreadSchedule(key).start()
#     #threads_lst.append(thread)


#
#
'''
    抽取信息
'''

# threads_lst = []
#
# # for key in categories.keys():
# #     thread = ThreadSchedule(key).start()
#     #threads_lst.append(thread)
#
# for key in categories.keys():
#     thread = ExtractInfo(key+'_pages').start()

'''
    合并 _pages.xls
'''

def combine_xls():

    all_lines = []

    xls_files = glob('./'+'*.xls')

    for file_name in xls_files:
        if '_pages' in file_name:
            info = xlrd.open_workbook(file_name)

            content = info.sheets()[0]

            nrows = content.nrows
            ncols = content.ncols



            for i in range(1, nrows):
                row_lst = []
                for j in range(0, ncols-1):
                    row_lst.append(str(content.cell(i, j).value))

                all_lines.append([row_lst[0].split('_')[0]]+ row_lst[2:])

    wb=xlwt3.Workbook()
    sheet=wb.add_sheet("计算机类图书信息")
    for i in range(0,len(all_lines)):
        for j in range(0,len(all_lines[i])):
            sheet.write(i, j, all_lines[i][j])
    #wb.save("图书信息_04_16.xls")
    wb.save("计算机类图书信息"+".xls")

combine_xls()









