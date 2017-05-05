#引入requests模块
import requests

#定义get_content函数
def get_content(url):
    resp = requests.get(url)
    return resp.text

if __name__ == '__main__':

    #定义url，值为要抓取的目标网站网址
    url = "http://www.phei.com.cn"

    #调用函数返回值赋值给content
    content = get_content(url)

    #打印输出content的前50个字符
    print("前50个字符为: ", content[0:50])

    #得到content的长度
    content_len = len(content)
    print("内容的长度为: ", content_len)

    #判断内容长度是否大于40KB
    if content_len >= 40*1024:
        print("内容的长度大于等于40KB.")
    else:
        print("内容的长度小于等于40KB.")

    # 方式1
    #文件的写入
    print('-'*20)
    print('方式1:', '文件写入')
    f1 = open('home_page.html', 'w', encoding='utf8')
    f1.write(content)
    f1.close()

    #文件的读取
    print('方式1:', '文件读取')
    f2 = open('home_page.html', 'r', encoding='utf8')
    content_read = f2.read()
    print("方式1读取的前50个字符为: ", content_read[0:50])
    f2.close()

    # 方式2
    # 文件的写入
    print('-' * 20)
    print('方式2:', '文件写入')
    with open('home_page_2.html', 'w', encoding='utf8') as f3:
        f3.write(content)
    # 文件的读取
    print('方式2:', '文件读取')
    with open('home_page_2.html', 'r', encoding='utf8') as f4:
        content_read_2 = f4.read()
        print("方式2读取的前50个字符为: ", content_read_2[0:50])

