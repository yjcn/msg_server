# -*- coding: utf8 -*-
import os
import json
import requests
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 从环境变量获取相关id
CORPID = os.environ['corpid']
AGENTID = os.environ['agentid']
CORPSECRET = os.environ['corpsecret']
# 相关id设置 
# corpid = 'xxx'  # 企业id
# agentid = 'xxx'   # 应用id
# corpsecret = 'xxx' # 企业secret

# 企业微信 api url
MSG_URL = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'

# text_card template
text_card_dict = {
       "touser" : "@all",
       # "toparty" : "PartyID1 | PartyID2",
       # "totag" : "TagID1 | TagID2",
       "msgtype" : "textcard",
       "agentid" : AGENTID,
       "textcard" : {
                "title" : "领奖通知",
                "description" : "<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">恭喜你抽中iPhone 7一台，领奖码：xxxx</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>",
                "url" : "URL",
                            "btntxt":"更多"
       },
       "enable_id_trans": 0,
       "enable_duplicate_check": 0,
       "duplicate_check_interval": 1800
    }

def get_access_token():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(CORPID, CORPSECRET)
    resp = requests.get(url=url)
    resp_dict = resp.json()
    access_token = None
    if resp.status_code == 200:
        access_token = resp_dict['access_token']
    return access_token
def main_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent = 2))
    logger.info("Received context: " + str(context))
    # 解析请求参数
    queryString = event['queryString']
    msg_title = queryString.get('text',None)
    msg_desp = queryString.get('desp', msg_title)
    text_card_dict['textcard']['title'] = msg_title
    text_card_dict['textcard']['description'] = msg_desp
    # logger.info(str(text_card_dict))
    # 获取access_token
    access_token = get_access_token() if msg_title is not None else None
    resp_status = 400
    resp_json = dict()
    if access_token is not None:
        resp = requests.post(url=MSG_URL.format(access_token),json=text_card_dict)
        resp_status = resp.status_code
        resp_json = resp.json()
    return {
        "isBase64Encoded": False,
        "statusCode": resp_status,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(resp_json)
    }
