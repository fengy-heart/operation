#! -*- coding: utf-8 -*-
'''
@File    : auto_jenkins.py
@Time    : 2020/08/01 13:03
@Author  : lemon 
@Desc    : 
'''
import jenkins
import json
import time
import asyncio


# 初始化，连接jenkins
auto_jenkins = jenkins.Jenkins('https://192.168.11.100:443', username='admin', password='admin@2020')
# user = auto_jenkins.get_whoami()
# version = auto_jenkins.get_version()
# print(version)


# 获取configxml
def get_configxml(job_new_name):
    if "h5" in job_new_name:
        configxml = open("./config-h5.xml", encoding='utf-8').read()
    elif "nodejs" in job_new_name:
        configxml = open("./config-nodejs.xml", encoding='utf-8').read()
    else:
        configxml = open("./config-app.xml", encoding='utf-8').read()
    return configxml


# 创建job并判断是否存在
def create_judge_job(job_new_name):
    configxml = get_configxml(job_new_name)
    end = auto_jenkins.job_exists(job_new_name)
    if end is None:
        # copy_end = auto_jenkins.copy_job(job_name_init, job_new_name)
        copy_end = auto_jenkins.create_job(job_new_name, configxml)
        time.sleep(5)
        create_judge_job(job_new_name)
    elif end is True:
        print("job is exist")
        return end


# if __name__ == "__main__": 
#     # job_new_name = "test-0729"
#     create_judge_job()