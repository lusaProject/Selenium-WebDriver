import requests
import json
import time
from logger import logger

def logins(account, password):
    url = "http://xxxxxxxxxxxxx/api/logins"
    params = {
        "username": account,
        "password": password
    }

    response = requests.get(url, params=params)
    logger.info(response.text)

    token = ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        token = parsed_data["token"]
    else:
        logger.info("请求失败，状态码：", response.status_code)
    return  token

def get_mobile(token, project_id):
    url = "http://xxxxxxxxxxxxxx/api/get_mobile"
    params = {
        "token": token,
        "project_id": project_id
    }

    response = requests.get(url, params=params)
    logger.info(response.text)

    mobile = ''
    if response.status_code == 200:
        parsed_data = json.loads(response.text)
        mobile = parsed_data["mobile"]
    else:
        logger.info("请求失败，状态码：", response.status_code)
    return mobile

def get_message(token, phone_num, project_id):
    url = "http://xxxxxxxxxxx/api/get_message"
    params = {
        "token": token,
        "project_id": project_id,
        "phone_num": phone_num
    }

    response = requests.get(url, params=params)
    print(response.text)

    code = -1
    if response.status_code == 200:
        parsed_data = json.loads(response.text)

        if 'code' in parsed_data:
            code = parsed_data["code"]
        else:
            return code
    else:
        logger.info("请求失败，状态码：", response.status_code)
    return code

if __name__ == '__main__':
    token = logins("xxxxxxx", "xxxxxxxxxxxx")

    phone_num = get_mobile(token, xxxxxx)

    code = get_message(token, phone_num, xxxxxxx)

    while code == -1:
        time.sleep(5)
        code = get_message(token, phone_num, xxxxxxxxxx)

    print("取到验证码是 : ", code)
