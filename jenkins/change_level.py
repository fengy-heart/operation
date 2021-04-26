# -*- coding: utf-8 -*-
'''
@File    :   change_level.py
@Time    :   2020/10/23
@Author  :   lemon-tea
@Desc    :   
'''
import jenkins
from xml.dom.minidom import parseString


# 初始化，连接jenkins
auto_jenkins = jenkins.Jenkins('https://192.168.11.100:443', username='admin', password='admin@2020')

# view列表
list_view = ["UAT发布", "TEST发布"]


# 获取指定view下的job
def get_job_name(list_view):
    job_list =  []
    for view in list_view:
        jobs = auto_jenkins.get_jobs(view_name=view)
        for job in jobs:
            job_list.append(job["name"])
    return job_list

# get_job_name(list_view)

def main():
    list_len = []
    for job_name in get_job_name(list_view):
        try:
            print("=============", job_name, "=============")
            # 获取job配置xml格式
            end = auto_jenkins.get_job_config(job_name)
            end = parseString(end)
            collection = end.documentElement
            all = collection.getElementsByTagName("permission")
            # 修改数据
            for i in range(len(all)):
                info = all[i].childNodes[0].data.replace("kaifa", "uat")
                all[i].childNodes[0].data = info
            # 写入文件
            try:
                with open('dom_write.xml','w',encoding='UTF-8') as fh:
                    end.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
                    print('OK')
            except Exception as err:
                print('错误：{err}'.format(err=err))
            configxml = open("./dom_write.xml", encoding='utf-8').read()
            # 更新配置
            auto_jenkins.reconfig_job(job_name, configxml)
        except:
            print("###############", job_name)


if __name__ == "__main__":
    main()

