from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os
import pyotp
import time

import json
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
                    filename='log.txt',
                    filemode='a')

logger = logging.getLogger('fb_logger')

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--start-maximized")
user_data_dir = Path(r"{}\UserData".format(os.path.dirname(__file__)))
chrome_options.add_argument('--user-data-dir={}'.format(user_data_dir))
chrome_options.add_argument('--lang=en-US')
chrome_options.add_argument('--disable-notifications')

hostname = "https://xxxxxxxxxxxxx"

def http_taskList():
    url = hostname + '/updateToken/taskList'
    headers = {
        'accept': 'application/json',
        'Auth': '***********'
    }
    params = {
        'page': '1',
        'size': '1'
    }

    response = requests.get(url, headers=headers, params=params)
    parsed_data = json.loads(response.text)
    print(response.text)
    return parsed_data

def http_updateToken(update): 
    url = hostname + '/updateToken/updateToken'

    headers = {
        'accept': 'application/json',
        'Auth': 'xxxxxxxxxxxxxxx',
        'Content-Type': 'application/json'
    }
    data = {
        "update": update
    }

    json_data = json.dumps(data)
    logger.info(json_data)
    response = requests.post(url, headers=headers, data=json_data)
    logger.info(response.text)

def facebooklogin(account, password, secretkey, driver):
    driver.get('https://www.facebook.com/')
    try:
        time.sleep(2)
        email_input = driver.find_element(By.ID, "email")
        if email_input is not None:
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='login_form_container']"))
                )
                if element is not None:
                    # 登录facebook
                    element = driver.find_element(By.XPATH, "//input[@class='inputtext _55r1 inputtext _1kbt inputtext _1kbt']")
                    element.clear()
                    element.send_keys(account)
                    time.sleep(2)

                    element = driver.find_element(By.XPATH, "//input[@class='inputtext _55r1 inputtext _9npi inputtext _9npi']")
                    element.clear()
                    element.send_keys(password)
                    time.sleep(2)

                    element = driver.find_element(By.XPATH, "//button[@class='_42ft _4jy0 _52e0 _4jy6 _4jy1 selected _51sy']")
                    element.click()
                    time.sleep(2)
                    logger.info("登录facebook")

                    try:
                        #选择新设备
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x193iq5w xeuugli x6s0dn4 x78zum5 x2lah0s x185m5pd xmly5ks']")))
                        if element is not None:
                            element.click()
                            time.sleep(2)

                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@class='x1n2onr6 x19cbwz6 x79zeqe xgugjxj x2oemzd']")))
                        if element is not None:
                            element_items = driver.find_elements(By.XPATH, "//label[@class='x1n2onr6 x19cbwz6 x79zeqe xgugjxj x2oemzd']")
                            if element_items is not None:
                                item = element_items[1]
                                item.click()
                                time.sleep(2)

                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='xlp1x4z x1ey2m1c xds687c x10l6tqk x17qophe xv7j57z']")))
                        if element is not None:
                            element = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.XPATH, ".//div[@class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xi112ho x17zwfj4 x585lrc x1403ito xtvsq51 x1fq8qgq x1ghtduv x1oktzhs']")))
                            if element is not None:
                                element.click()
                                time.sleep(2)
                    except:
                        print('')

                    try:
                        # google验证页面1
                        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_4-u2 _5x_7 _p0k _5x_9 _4-u8']")))
                        if element is not None:
                            time.sleep(2)
                            secret_key = secretkey
                            totp = pyotp.TOTP(secret_key)

                            element = driver.find_element(By.XPATH, "//input[@class='inputtext']")
                            element.clear()
                            current_otp = totp.now()
                            logger.info("OTP: %s", current_otp)
                            element.send_keys(current_otp)

                            element = driver.find_element(By.XPATH, "//button[@class='_42ft _4jy0 _2kak _4jy4 _4jy1 selected _51sy']")
                            element.click()
                            logger.info("google验证页面1")

                            # Cooke页面
                            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_4-u2 _5x_7 _p0k _5x_9 _4-u8']")))
                            if element is not None:
                                time.sleep(2)
                                element = driver.find_element(By.XPATH, "//button[@class='_42ft _4jy0 _2kak _4jy4 _4jy1 selected _51sy']")
                                element.click()
                                logger.info("Cooke页面")
                    except:
                        print('')

                    try:
                        # google验证页面2
                        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x6s0dn4 x78zum5 x1qughib xh8yej3']")))
                        if element is not None:
                            element = WebDriverWait(element, 10).until(EC.element_to_be_clickable((By.XPATH, ".//input")))
                            if element is not None:
                                secret_key = secretkey
                                totp = pyotp.TOTP(secret_key)

                                element.clear()
                                current_otp = totp.now()
                                logger.info("OTP : %s", current_otp)
                                element.send_keys(current_otp)

                                element = driver.find_element(By.XPATH, "//div[@class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xi112ho x17zwfj4 x585lrc x1403ito xtvsq51 x1fq8qgq x1ghtduv x1oktzhs']")
                                element.click()
                                logger.info("google验证页面2")

                                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xi112ho x17zwfj4 x585lrc x1403ito xtvsq51 x1fq8qgq x1ghtduv x1oktzhs']")))
                                if element is not None:
                                    time.sleep(1)
                                    element.click()
                                    logger.info('信任这个设备')
                    except:
                        print('')
            except:
                logger.info("login facebook error...")
    except:
        print("已经登录facebook")

def continue_button(itemtext, driver):
    try:
        elementArea = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x78zum5 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd xdt5ytf xdm93yi']"))
        )
        if elementArea is not None:
            element_items = elementArea.find_elements(By.XPATH, ".//label[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk x78zum5 xdl72j9 xdt5ytf x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt']")
            if element_items is not None:
                for item in element_items:
                    item.click()
                    break
    except:
        print('')

    element_items = driver.find_elements(By.XPATH, "//div[@class='x8t9es0 x1fvot60 xxio538 x1heor9g xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1pd3egz xeuugli']")
    if element_items is not None:
        for item in element_items:
            if item.text == itemtext:
                item.click()

def adstoken(url, driver):
    driver.get(url)

    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='_271k _1qjd _3-8x _483s']")))
    if element is not None:
        element.click()
        element_listbox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='uiScrollableAreaContent']")))
        if element_listbox is not None:
            element_items = element_listbox.find_elements(By.XPATH, ".//a[@class='_3vsz _2eyk _4ck5']")
            if element_items is not None:
                for item in element_items:
                    # 检查是否该元素已展开
                    img_element = item.find_element(By.XPATH, ".//i[contains(@class, '_3vsv img sp_rcf0M71so1p')]")
                    if img_element is not None and img_element.get_attribute("class").split(" ").count("sx_7a696e") == 1:
                        item.click()
                    WebDriverWait(element_listbox, 20).until(EC.visibility_of_element_located((By.XPATH, ".//i[@class='_3vsv img sp_rcf0M71so1p sx_6346ee']")))
            element_items = element_listbox.find_elements(By.XPATH, ".//a[@class='_3vsz _2eyk _4ck5']")
            if element_items is not None:
                for item in element_items:
                    element_sub_items = item.find_elements(By.XPATH, "./..//div[@class='_2wpb _3v8w']")
                    if element_sub_items is not None:
                        for item_check in element_sub_items:
                            if item_check.get_attribute("aria-checked") != "true":
                                action = ActionChains(driver)
                                action.move_to_element(item_check).click().perform()

        element = driver.find_element(By.XPATH, "//button[@class='_271k _1qjd _ai7j _ai7k _ai7m']")
        element.click()

        # 切换窗口
        wait = WebDriverWait(driver, 20)
        wait.until(EC.number_of_windows_to_be(2))

        window_handles = driver.window_handles
        current_window = driver.current_window_handle

        for handle in window_handles:
            if handle != current_window:
                driver.switch_to.window(handle)
                break
        try:
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x16tdsg8 xggy1nq x1ja2u2z x1t137rt x6s0dn4 x1ejq31n xd10rxx x1sy0etr x17r0tee xdl72j9 x1q0g3np x193iq5w x1n2onr6 x1hl2dhg x87ps6o xxymvpz xlh3980 xvmahel x1lku1pv xhk9q7s x1otrzb0 x1i1ezom x1o6z2jb x1xlr1w8 x140t73q xb57al4 x1y1aw1k xwib8y2 x1swvt13 x1pi30zi x78zum5 x1iyjqo2 xs83m0k']")))
            if element is not None:
                element.click()

                continue_button('Continue', driver)
                time.sleep(2)
                continue_button('Continue', driver)
                time.sleep(2)
                continue_button('Continue', driver)
                time.sleep(2)
                continue_button('Continue', driver)
                time.sleep(2)
                continue_button('Continue', driver)
                time.sleep(2)
                continue_button('Save', driver)
                time.sleep(2)
                continue_button('Got it', driver)
                time.sleep(2)
        except:
            print('')

        window_handles = driver.window_handles
        for handle in window_handles:
            driver.switch_to.window(handle)
            time.sleep(3)
            break

def upload_token():
    parsed_data = http_taskList()
    code = parsed_data['code']
    msg = parsed_data['msg']
    data = parsed_data['data']
    if data['count'] > 0:
        item = data['list'][0]
        task_id = item['_id']
        AccountID = item['AccountID']
        account = item['user_id']
        google_secret = item['google_secret']
        user_pwd = item['user_pwd']
        dev_id = item['dev_id']
        email = item['email']
        app_ids = item['app_id']
        stats = item['stats']
        itime = item['itime']

        chrome_options.add_argument('--profile-directory={}'.format(account))
        driver = webdriver.Chrome(options=chrome_options)

        facebooklogin(account, user_pwd, google_secret, driver)
        time.sleep(2)

        try:
            driver.get('https://developers.facebook.com/settings/developer/requests/')
            element_items = driver.find_elements(By.XPATH, ".//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x16tdsg8 xggy1nq x1ja2u2z x1t137rt x6s0dn4 x1ejq31n xd10rxx x1sy0etr x17r0tee x3nfvp2 xdl72j9 x1q0g3np x2lah0s x193iq5w x1n2onr6 x1hl2dhg x87ps6o xxymvpz xlh3980 xvmahel x1lku1pv xhk9q7s x1otrzb0 x1i1ezom x1o6z2jb x1xlr1w8 x140t73q xb57al4 x1y1aw1k xwib8y2 x1swvt13 x1pi30zi']")
            if element_items is not None:
                for item in element_items:
                    time.sleep(2)
                    item.click()
        except:
            print('requests error ...')

        update_list = []
        token = ''
        for app_id in app_ids:
            try:
                app_url = "https://developers.facebook.com/tools/explorer/" + app_id

                logger.info('%s %s %s %s', account, user_pwd, google_secret, app_id)
                adstoken(app_url, driver)

                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='_4b7k _4b7k_big _53rs']")))
                if element is not None:
                    token = element.get_attribute('value')

            except:
                logger.info('update error...')

            item = {"app_id": app_id, "dev_id": account, "task_id": task_id, "token": token}
            update_list.append(item)
            http_updateToken(update_list)

if __name__ == '__main__':
    while True:
        upload_token()
        print('sleep...')
        time.sleep(60 * 60)
