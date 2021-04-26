#! _*_coding: utf-8 _*_

import jenkins
from xml.dom.minidom import parseString

# 初始化，连接jenkins
auto_jenkins = jenkins.Jenkins('https://192.168.11.100:443', username='admin', password='admin@2020')
# user = auto_jenkins.get_whoami()
# version = auto_jenkins.get_version()
# print(version)

list_view = ["test", "uat"]


# 获取指定view的job
def get_job_name(view):
    job_list = []
    jobs = auto_jenkins.get_jobs(view_name=view)
    for job in jobs:
        job_list.append(job["name"])
    return job_list

# 读取文件，返回结果列表
def get_file_info():
    with open("file.sh") as fp:
        text = fp.readlines()
        fp.close()
    return text

for view in list_view:
    job_list = get_job_name(view)
    for job in job_list:
        config_info = auto_jenkins.get_job_config(job)
        # 解析配置
        config_info = parseString(config_info)
        collection = config_info.documentElement
        all = collection.getElementsByTagName("hudson.tasks.Shell")
        for i in range(len(all)):
            end = all[0].getElementsByTagName("command")[0].childNodes[0].data
            for j in get_file_info():
                end = end + "\n" + j
            all[0].getElementsByTagName("command")[0].childNodes[0].data = end
        # 修改后的配置写入文件
        try:
            with open("file.xml", "w", encoding="UTF-8") as fh:
                config_info.writexml(fh, indent="", addindent="\t", newl="\n", encoding="UTF-8")
                print("ok")
        except:
            pass
        # 重新加载配置
        try:
            config_xml = open('file.xml', encoding="utf-8").read()
            auto_jenkins.reconfig_job(job_name, config_xml)
        except:
            pass


# if __name__ == "__main__":
#     main()