from selenium import webdriver
import time
url_ip = 'http://jsonip.com/'

profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9150)
profile.set_preference('network.proxy.socks_version', 5)
profile.update_preferences()

browser = webdriver.Firefox(profile)

while True:
    time.sleep(5)
    browser.get(url_ip)

browser.quit()






