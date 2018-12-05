from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import names
import time
from pyfiglet import figlet_format
import random
from termcolor import cprint
import zipfile
from threading import Thread

from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

cprint(figlet_format(('thebotsmith'), font='doom'), attrs=['bold'])

chromepath = "c:\chromedriver"
# set your chrome driver path here ^

proxy_list = []
with open("proxylist.txt","r") as file:
    for line in file:
        proxy_list.append(str(line).replace("\n",""))

def my_proxy(PROXY_HOST,PROXY_PORT, username, password):
  if username:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: '%s',
                port: parseInt('%s')
              },
              bypassList: ["foobar.com"]
            }
          };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: '%s',
                password: '%s'
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """% (PROXY_HOST, PROXY_PORT, username, password)
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    co = Options()
    co.add_argument("--incognito")
    co.add_extension(pluginfile)
  else:
    co = webdriver.ChromeOptions()
    co.add_argument('--proxy-server=%s' % PROXY_HOST+":"+PROXY_PORT)
  co.add_argument('--disable-gpu')
  co.add_argument('--log-level=3')
  co.add_argument("--incognito")
  co.add_argument('--window-size=880x880')
  #co.add_argument('--headless')
  co.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})
  driver = webdriver.Chrome(chrome_options=co)
  return driver

def cycle_config(list):
    q = list[0]
    list.append(q)
    list.pop(0)
    return q

def cycle_file(filex):
    list = []
    with open(filex,'r+') as file:
        for line in file:
            list.append(line)
        q = list[0]
        list.append(q)
        list.pop(0)
    with open(filex,'w') as file:
        for item in list:
            file.write(item)

def run_account():
    with open('accounts.txt') as f:
        credentials = map(lambda r: tuple(r.split(':')), [row for row in f.read().splitlines()])
        cycle_file('accounts.txt')
    for credential in credentials:
        import random

        if len(proxy_list) > 0:
            proxy = random.choice(proxy_list) # random choice of proxy
            split = proxy.split(':')
            proxy_host, proxy_port = split[0], split[1]
            if len(split) != 2:
                username, password = split[2], split[3]
            else:
                username, password = False, False
            driver = my_proxy(proxy_host, proxy_port, username, password)
        print('Started instance with proxy',proxy)
        #driver = webdriver.Chrome()
        actions = ActionChains(driver)

        username, password = credential
        url = "https://www.google.com/"
        driver.get(url)

        button1 = driver.find_element_by_xpath('//*[@id="gb_70"]')
        button1.click()
        email = "email"

        login = driver.find_element_by_xpath('//*[@id="identifierId"]')
        login.send_keys(username)
        next0 = driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span')
        next0.click()

        passw = WebDriverWait(driver, 5).until(
           EC.presence_of_element_located(('xpath','//*[@id="password"]/div[1]/div/div[1]/input')))


        time.sleep(5)
        passw.send_keys(password)
        time.sleep(5)
        final = driver.find_element_by_xpath('//*[@id="passwordNext"]/content/span')
        final.click()
        print(" ")
        print(Fore.GREEN + ("Logged in to google!"))
        print(" ")
        time.sleep(1)
        yt = "https://www.youtube.com/watch?v=YBqDATEltNE"

        driver.get(yt)
        print(Fore.GREEN + ("started youtube video"))
        print(" ")
        time.sleep(300)
        driver.get(url)

        print(Fore.GREEN + ("starting google searches"))
        print(" ")

        search = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')
        search.send_keys('cook')
        actions.send_keys(Keys.ENTER)



        for i in range(10):
            random = names.get_full_name()
            searchurl = "https://www.google.com/search?source=hp&ei=IrI6W_e4EMnn5gLloKzgDQ&q={}&oq={}&gs_l=psy-ab.12..0j0i131k1j0l4j0i131k1l2j0l2.1514.155452.0.177155.20.5.15.0.0.0.110.250.4j1.5.0....0...1c.1.64.psy-ab..0.20.340...0i10k1.0.wl_aQzdHSe4".format(random,random)

            time.sleep(10)
            driver.get(searchurl)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(10)



        driver.get(url)
        print(Fore.GREEN + ("completed google searches"))
        print(" ")
        print(Fore.GREEN + ("{} Done!!").format(username))
        print(" ")
        driver.delete_all_cookies()
        driver.close()

threads = []
for thread in range(3):
    thread_id = thread+1
    t = Thread(target=run_account,)
    t.start()
    threads.append(t)
    time.sleep(2)
for thread in threads:
    thread.join()

print(Fore.GREEN + "All account done")
