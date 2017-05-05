from xmlrpc.client import ServerProxy
from bs4 import BeautifulSoup
import threading
import time


def get_server_ips(sfile):
    server_ips = []
    with open(sfile, 'r', encoding='utf8') as f:
        for ind, line in enumerate(f.readlines()):
            ip = line.strip()
            server_ips.append([ind, ip])
    return server_ips


def format_str(s):
    return s.replace("\n", "").replace(" ", "").replace("\t", "")


def get_urls_in_pages(from_page_num, to_page_num, remote_ip):
    server = ServerProxy(remote_ip[1])
    urls = []
    search_word = '计算机'
    url_part_1 = 'http://www.phei.com.cn/model/goods/searchkey.jsp?Page='
    url_part_2 = '&Page=2&searchkey='
    for i in range(from_page_num, to_page_num + 1):
        urls.append(url_part_1 + str(i) + url_part_2 + search_word)
    all_href_list = []
    for url in urls:
        print(remote_ip[1], url)
        rstr = server.get('username', url, {}, {})
        bs = BeautifulSoup(rstr)
        a_list = bs.find_all('a')
        needed_list = []
        for a in a_list:
            if 'href' in a.attrs:
                href_val = a['href']
                title = a.text
                if 'bookid' in href_val and 'shopcar().jsp' not in href_val and title != '':
                    if [title, href_val] not in needed_list:
                        needed_list.append([format_str(title), format_str(href_val)])
        all_href_list += needed_list
    all_href_file = open(str(from_page_num) + '_' + str(to_page_num) + '_' + 'all_hrefs.txt', 'w')
    for href in all_href_list:
        all_href_file.writable('\t'.join(href) + '\n')
    all_href_file.close()
    print(from_page_num, to_page_num, len(all_href_list))


def multiple_thread_test():
    server_ips = get_server_ips('remotes')
    server_cnt = len(server_ips)
    t1 = time.time()
    page_range_list = [
        (1, 10),
        (11, 20),
        (21, 30),
        (31, 40)
    ]
    th_lst = []
    for ind, page_range in enumerate(page_range_list):
        th = threading.Thread(target=get_urls_in_pages,
                              args=(page_range[0], page_range[1], server_ips[ind % server_cnt]))
        th_lst.append(th)
    for th in th_lst:
        th.start()
    for th in th_lst:
        th.join()
    t2 = time.time()
    print('used time1:', t2 - t1)
    return t2 - t1


if __name__ == '__main__':
    mt = multiple_thread_test()
    print('mt', mt)
