import base64
import json
from typing import Any
import requests
from faker import Faker
from logger import logger

hostname = "http://xxxxxxxxxxxxxx"

def getActAndCommonPages():
    url = hostname + "/fb/getActAndCommonPages"
    response = requests.get(url)
    logger.info(response.text)
    account, profile = '', ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]
        if code == 0:
            account = parsed_data['data']['act']
            profile = parsed_data['data']['common_pages']
    return account, profile

def getNoUserPageAct():
    url =  hostname + "/fb/getNoUserPageAct"
    response = requests.get(url)
    logger.info(response.text)
    act, act_pwd, secret = '', '', ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]
        if code == 0:
            act = parsed_data['data']['act']
            act_pwd = parsed_data['data']['act_pwd']
            secret = parsed_data['data']['secret']
    return act, act_pwd, secret

def getActInfo(account):
    url = hostname + "/fb/getActInfo"
    params = {"act": account}
    response = requests.get(url, params=params)
    logger.info(response.text)
    act, act_pwd, secret = '', '', ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]
        if code == 0:
            act = parsed_data['data']['act']
            act_pwd = parsed_data['data']['act_pwd']
            secret = parsed_data['data']['secret']
    return act, act_pwd, secret

def getDevAct():
    url =  hostname + "/fb/getDevAct"
    response = requests.get(url)
    logger.info(response.text)
    act, act_pwd, secret = '', '', ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]
        if code == 0:
            act = parsed_data['data']['act']
            act_pwd = parsed_data['data']['act_pwd']
            secret = parsed_data['data']['secret']
    return act, act_pwd, secret

def getBmUrls():
    url = hostname + "/fb/getBmUrls"
    response = requests.get(url)
    logger.info(response.text)

    account, bmUrls = '', ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data['code']
        if code == 0:
            account = parsed_data['data']['act']
            bmUrls = parsed_data['data']['bm_info']
    return account, bmUrls

def getApplyAdActTask():
    url = hostname + "/fb/getApplyAdActTask"
    response = requests.get(url)
    parsed_data : Any = None
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
    return parsed_data

def getAdActTaskApplying():
    url = hostname + "/fb/getAdActTaskApplying"
    response = requests.get(url)
    logger.info(response.text)
    data : Any = None
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        data = parsed_data['data']
    return data

def save_base64_image(base64_string, filename):
    try:
        # 检查并修复base64字符串
        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += '=' * (4 - missing_padding)

        # 解码base64字符串并保存图片
        image_data = base64.b64decode(base64_string)
        with open(filename, 'wb') as f:
            f.write(image_data)

        logger.info("Image saved successfully: %s", filename)
    except Exception as e:
        logger.error("Error saving image: %s", str(e))

def saveUserPage(act, userPage):
    url = hostname + "/fb/saveUserPage"

    data = {
        "act": act,
        "user_page": userPage
    }
    response = requests.post(url, json=data)
    # print(response.text)
    logger.info(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]

    return code

def saveCommonPageResult(act, common_page, result):
    url = hostname + "/fb/saveCommonPageResult"

    data = {
        "act": act,
        "common_page": common_page,
        "result": result
    }
    response = requests.post(url, json=data)
    logger.info(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]

    return code

def saveBm(act, bm_id, bm_name):
    url = hostname + "/fb/saveBm"

    data = {
        "act": act,
        "bm_id": bm_id,
        "bm_name": bm_name
    }

    response = requests.post(url, json=data)
    logger.info(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]
    return code

def saveDevApp(app_id, dev_id, token):
    url = hostname + "/fb/saveDevApp"

    data = {
        "app_id": app_id,
        "dev_id": dev_id,
        "token": token
    }

    response = requests.post(url, json=data)
    logger.info(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]

    return code

def saveApplyAdActTaskId(fb_id, id, supplier):
    url = hostname + "/fb/saveApplyAdActTaskId"

    data = {
        "fb_id": fb_id,
        "id": id,
        "supplier": supplier
    }

    response = requests.post(url, json=data)
    logger.info(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]

    return code

def saveApplyAdActTaskResult(ad_act, fb_id, result):
    url = hostname + "/fb/saveApplyAdActTaskResult"

    data = {
        "ad_act": ad_act,
        "fb_id": fb_id,
        "result": result
    }

    response = requests.post(url, json=data)
    logger.info(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        code = parsed_data["code"]

    return code

def faker():
    fake = Faker()
    return fake

def confirm():
    user_input = input("Do you want to continue? (yes/no): ").strip().lower()
    if user_input == "yes":
        print("Continuing...")
    elif user_input == "no":
        print("Exiting...")
        exit()
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == '__main__':

    getAdActTaskApplying()