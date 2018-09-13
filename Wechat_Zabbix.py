#!/usr/bin/env python
#coding=utf-8

import requests
import sys
import json
import urllib3

urllib3.disable_warnings()

def GetToken(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid":Corpid,
        "corpsecret":Secret
    }
    req = requests.get(url=Url,params=Data,verify=False)
    print req.json()
    Token = req.json()['access_token']
    return Token

def SendMessage(Token,User,Agentid,Title,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送
        #"totag": Tagid,                                # 企业号中的标签id，群发使用（推荐）
        #"toparty": Partyid                             # 企业号中的部门id，群发时使用
        "msgtype": "text",                              # 消息类型
        "agentid": Agentid,                             # 企业号中的应用id
        "text": {
            "content": Title + '\n' + Content
        },
        "safe": "0"
    }
    req = requests.post(url=Url,data=json.dumps(Data),verify=False)
    return req.text


if __name__ == '__main__':
    User = sys.argv[1]                                                              # zabbix传过来的第一个参数
    Title = sys.argv[2]                                                             # zabbix传过来的第二个参数
    Content = sys.argv[3]                                                           # zabbix传过来的第三个参数

    Corpid = "ww02946fb9034b5649"                                                   # CorpID是企业号的标识
    Secret = "X56RLPUFZYyoaEBCNaZecSkWN-s3_ZRdKMYlK2KJuCA"                          # Secret是管理组凭证密钥
    #Tagid = "1"                                                                    # 通讯录标签ID
    Agentid = "1000003"                                                             # 应用ID
    #Partyid = "1"                                                                  # 部门ID

    Token = GetToken(Corpid, Secret)
    Status = SendMessage(Token,User,Agentid,Title,Content)
    print Status
