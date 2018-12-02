# -*- coding: utf-8 -*-
"""
更新cdn证书(可配合let's encrypt 等完成自动证书更新)
"""
import qiniu
from qiniu import DomainManager
import os
import time

# 账户ak，sk
access_key = os.getenv('ACCESS_KEY', '')
secret_key = os.getenv('SECRET_KEY', '')
domain_name = os.getenv('DOMAIN', '')

auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
domain_manager = DomainManager(auth)

privatekey = "/ssl/{}/privkey.pem".format(domain_name)
ca = "/ssl/{}/fullchain.pem".format(domain_name)

with open(privatekey, 'r') as f:
    privatekey_str = f.read()

with open(ca, 'r') as f:
    ca_str = f.read()

ret, info = domain_manager.create_sslcert("{}/{}".format(domain_name, time.strftime("%Y-%m-%d", time.localtime())),
                                          domain_name, privatekey_str, ca_str)
print(ret['certID'])

if domain_name.startswith("*"):
    domain_name = domain_name[1:]
ret, info = domain_manager.put_httpsconf(domain_name, ret['certID'], False)
print(info)
