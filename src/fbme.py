from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from logger import logger
import os
import pyotp
import time
import fbtool
import createads

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--start-maximized")
user_data_dir = Path(r"{}\UserData".format(os.path.dirname(__file__)))
chrome_options.add_argument('--user-data-dir={}'.format(user_data_dir))
chrome_options.add_argument('--lang=en-US')
chrome_options.add_argument('--disable-notifications')

JS_QUERY_STATUS3 = """
var reseller_name = arguments[0]
function query() {
    return new Promise(function(resolve, reject) {
        new(require("AsyncTypedRequest"))("https://www.facebook.com/china_businesses/onboarding/pre_flow_fetch/?reseller_name=${reseller_name}").setPayloadHandler(function(b) {
            resolve(b)
        }).send();
    }).then(function(b) {
        return b;
    });
};

return await query()
"""

def get_recent_apply(driver):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='x9f619 x78zum5 x2lah0s xh8yej3 xyamay9 x1l90r2v x1swvt13 x1pi30zi']")))
        if element is not None:
            status = driver.execute_script(JS_QUERY_STATUS3, "awaiting_reseller_selection")
            return status["vettingRequestSpec"]["ResellerName"], str(status["vettingRequestSpec"]["VettingRequestID"])
    except Exception as e:
        logger.info(e)
        return "", ""

def get_apply_status(driver, ids):
    ret_data = []
    try:
        element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='x9f619 x78zum5 x2lah0s xh8yej3 xyamay9 x1l90r2v x1swvt13 x1pi30zi']")))
        if element is not None:
            status = driver.execute_script(JS_QUERY_STATUS3, "awaiting_reseller_selection")
            for item in status["historicalRequests"]:
                req_id = str(item["vetting_request"]["VettingRequestID"])
                if req_id in ids and item["vetting_request"]["Status"] == "approved":
                    ret_data.append(req_id)
            return ret_data
    except Exception as e:
        logger.info(e)
        return ret_data

def facebooklogin(account):
    #获取个人账号
    account, password, secretkey = fbtool.getActInfo(account)
    chrome_options.add_argument('--profile-directory={}'.format(account))
    driver = webdriver.Chrome(options=chrome_options)

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

    return  driver, password

def language_switch(driver):
    driver.get('https://www.facebook.com/settings/?tab=language_and_region')

    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']")))
        if element is not None:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, ".//div[@class='x9f619 x1n2onr6 x1ja2u2z x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld xwib8y2 x1sxyh0 xurb0ha']")))
            elements = element.find_elements(By.XPATH, ".//div[@class='x9f619 x1n2onr6 x1ja2u2z x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld xwib8y2 x1sxyh0 xurb0ha']")
            if elements is not None:
                element = elements[0]
                lang_btn = element.find_element(By.XPATH, ".//div[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3']")
                if lang_btn is not None:
                    time.sleep(1)
                    lang_btn.click()
                    lang_dlg = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xyamay9 x1l90r2v']"))
                    )
                    if lang_dlg is not None:
                        input_element = WebDriverWait(lang_dlg, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                                              ".//input[@class='x1i10hfl xggy1nq x1s07b3s x1kdt53j x1yc453h xhb22t3 xb5gni xcj1dhv x2s2ed0 xq33zhf xjyslct xjbqb8w xnwf7zb x40j3uw x1s7lred x15gyhx8 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u xdl72j9 x1iyjqo2 xs83m0k xjb2p0i x6prxxf xeuugli x1a2a7pz x1n2onr6 x15h3p50 xm7lytj x1sxyh0 xdvlbce xurb0ha x1vqgdyp']")))

                        if input_element is not None:
                            input_element.send_keys("US")
                            input_radio = WebDriverWait(lang_dlg, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                                                          ".//div[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']")))
                            if input_radio is not None:
                                time.sleep(1)
                                input_radio.click()
    except:
        logger.info("跳过语言切换")

def review_invitation(url, driver):
    result = False
    try:
        driver.get(url)
        elementArea = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x9f619 x193iq5w x1talbiv x1sltb1f x3fxtfs x1swvt13 x1pi30zi']"))
        )
        if elementArea is not None:
            element = elementArea.find_element(By.XPATH, ".//div[@class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou xtvsq51 x1r1pt67']")
            element.click()

        elementArea = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x9f619 x1ja2u2z x1k90msu x6o7n8i x1qfuztq x10l6tqk x17qophe x13vifvy x1hc1fzr x71s49j xh8yej3']"))
        )
        if elementArea is not None:
            element = elementArea.find_element(By.XPATH, ".//div[@class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xbxaen2 x1u72gb5 xtvsq51 x1r1pt67']")
            element.click()

        elementArea = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x9f619 x1ja2u2z x1k90msu x6o7n8i x1qfuztq x10l6tqk x17qophe x13vifvy x1hc1fzr x71s49j xh8yej3']"))
        )
        if elementArea is not None:
            element = elementArea.find_element(By.XPATH, ".//div[@class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xbxaen2 x1u72gb5 xtvsq51 x1r1pt67']")
            element.click()
            result = True
    except:
        print('')
    return  result

def business(url, passwd, driver):
    bm_name = ''
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x6s0dn4 x78zum5 xl56j7k x1608yet xljgi0e x1e0frkt']")))
        if element is not None:
            element_items = driver.find_elements(By.XPATH, "//div[@class='x6s0dn4 x78zum5 xl56j7k x1608yet xljgi0e x1e0frkt']")
            if element_items is not None:
                item = element_items[0]
                item.click()
                time.sleep(2)
    except:
        print('')

    try:
        elementArea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x1gzqxud x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1kmqopl x5yr21d xh8yej3']"))
        )
        if elementArea is not None:
            element = elementArea.find_element(By.XPATH,
                                               ".//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x16tdsg8 xggy1nq x1ja2u2z x1t137rt x6s0dn4 x1ejq31n xd10rxx x1sy0etr x17r0tee xdl72j9 x1q0g3np x193iq5w x1n2onr6 x1hl2dhg x87ps6o xxymvpz xlh3980 xvmahel x1lku1pv xhk9q7s x1otrzb0 x1i1ezom x1o6z2jb xo1l8bm x108nfp6 xas4zb2 x1y1aw1k xwib8y2 x1pi30zi x1ye3gou x78zum5 x1iyjqo2 xs83m0k']")
            element.click()
    except:
        print('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='_58al _aghb']"))
        )
        if element is not None:
            name = fbtool.faker().name()
            element.send_keys(name)

        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x8t9es0 x1fvot60 xxio538 x1heor9g xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1pd3egz xeuugli']"))
        )
        element.click()

        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x8t9es0 x1fvot60 xxio538 x1heor9g xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1pd3egz xeuugli']"))
        )
        element.click()

        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x8t9es0 x1fvot60 xxio538 x1heor9g xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1pd3egz xeuugli']"))
        )
        element.click()
    except:
        print('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='ajax_password']"))
        )
        element.send_keys(passwd)

        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='_42ft _4jy0 layerConfirm uiOverlayButton _4jy3 _4jy1 selected _51sy']"))
        )
        element.click()
        time.sleep(5)
    except:
        print('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x8t9es0 x1fvot60 xxio538 x1heor9g xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1pd3egz xeuugli']"))
        )
        element.click()
    except:
        print('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x8t9es0 x1fvot60 xo1l8bm xxio538 x108nfp6 xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj xeuugli']"))
        )
        element.click()
    except:
        print('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='xmi5d70 x1fvot60 xxio538 xbsr9hj xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj x1fcty0u']"))
        )
        element.click()
    except:
        print('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x1xqt7ti x1uxerd5 x1xlr1w8 xrohxju xbsr9hj x1yc453h xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj xeuugli xat24cr']"))
        )
        if element is not None:
            bm_name = element.text
    except:
        logger.info('')

    try:
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='x8t9es0 x1uxerd5 x1xlr1w8 xrohxju x4hq6eo x1yc453h xuxw1ft x6ikm8r x10wlt62 xlyipyv x1h4wwuj xeuugli']"))
        )
        if element is not None:
            bm_name = element.text
    except:
        logger.info('')

    return bm_name

def run_tasks():
    #上传个人主页
    # account = fbtool.getNoUserPageAct()[0]
    # if account != '':
    #     driver = facebooklogin(account)[0]
    #     time.sleep(2)
    #     driver.get('https://www.facebook.com/me')
    #     userPage = driver.current_url
    #     logger.info("account, userPage %s %s", account, userPage)
    #     fbtool.saveUserPage(account, userPage)
    #     language_switch(driver)

    #绑定公共主页
    # common_account, urls = fbtool.getActAndCommonPages()
    # if common_account != '':
    #     driver = facebooklogin(common_account)[0]
    #     time.sleep(2)
    #     language_switch(driver)
    #     for page in urls:
    #         if page != '':
    #             logger.info("common_account, page %s %s", common_account, page)
    #             result = review_invitation(page, driver)
    #             if result:
    #                 fbtool.saveCommonPageResult(common_account, page, 1)
    #             else:
    #                 print('CommonPage error...')
    #                 fbtool.confirm()
    #                 fbtool.saveCommonPageResult(common_account, page, 1)

    # 绑定bm地址
    # bm_act, bmUrls = fbtool.getBmUrls()
    # if bm_act != '':
    #     driver, password = facebooklogin(bm_act)
    #     time.sleep(2)
    #     for info in bmUrls:
    #         bm_id = info['id']
    #         bm_name = business(info['urls'][0], password, driver)
    #         if bm_name != '':
    #             logger.info("account, bm_id, bm_name %s %s %s", bm_act, bm_id, bm_name)
    #             fbtool.saveBm(bm_act, bm_id, bm_name)
    #         else:
    #             print('BmUrl error...')

    #创建广告户
    parsed_data = fbtool.getApplyAdActTask()
    if parsed_data["code"] == 0:
        data = parsed_data["data"]
        taskID = data["id"]
        supplier_url = data["supplier_url"]
        account = data["act"]

        common_page_url = data["common_page"]["url"]

        driver = facebooklogin(account)[0]
        language_switch(driver)
        time.sleep(5)

        driver.get('https://business.facebook.com')
        time.sleep(5)

        driver.get(supplier_url)

        createads.bind_phone(driver)
        fbtool.confirm()

        uscc = data["license"]["code"]

        company_name = data["license"]["name"]

        company_name_en = ""

        company_email = fbtool.faker().email()

        company_address = data["license"]["location"]

        company_zip_code = fbtool.faker().zipcode()

        company_city_en = data["license"]["city"]

        website_urls = data["urls"]
        company_website = website_urls[0]

        imgData = data["license"]["image"]
        fbtool.save_base64_image(imgData, 'license.png')
        time.sleep(5)
        company_license_path = r"{}\license.png".format(os.path.dirname(__file__))

        ads_account_names = []
        num = data["ad_act_num"]
        ad_act_name = data["ad_act_name"]

        for i in range(num):
            name = ad_act_name + '-' + str(i+1)
            ads_account_names.append(name)
        logger.info(ads_account_names)

        ads_target_websites = website_urls
        logger.info(ads_target_websites)
        bm_name = data["bm"]["name"]

        pp_names = []
        common_page_name = data["common_page"]["name"]
        pp_names.append(common_page_name)

        result = createads.create_ads(uscc, company_name, company_name_en, company_email, company_address, company_zip_code, company_city_en, company_website, company_license_path, ads_account_names, bm_name, pp_names, ads_target_websites, driver)
                   
        if result:
            time.sleep(5)
            driver.get('https://www.facebook.com/chinabusinesses/onboarding')
            fbtool.confirm()
            supplier, fb_id = get_recent_apply(driver)
            logger.info("fb_id, id, supplier %s %s %s", fb_id, taskID, supplier)
            fbtool.saveApplyAdActTaskId(fb_id, taskID, supplier)

if __name__ == '__main__':
    while True:
        run_tasks()
        print('sleep...')
        time.sleep(60 * 60)
