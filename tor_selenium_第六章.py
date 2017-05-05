from selenium import webdriver

url_pub = 'http://www.phei.com.cn/'

profile = webdriver.FirefoxProfile()

profile.set_preference("permissions.default.stylesheet", 2)
profile.set_preference("permissions.default.image", 2)
profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")

profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9150)
profile.set_preference('network.proxy.socks_version', 5)
profile.update_preferences()

browser = webdriver.Firefox(profile)

browser.get(url_pub)

with open('tor_selenium' + '.html', 'w', encoding='utf8') as f:
    f.write(browser.page_source)

browser.quit()






