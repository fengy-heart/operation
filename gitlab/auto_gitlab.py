#! -*- coding: utf-8 -*-
'''
@File    : auto_gitlab.py
@Time    : 2020/08/01 22:25
@Author  : lemon 
@Desc    : 
'''
import gitlab
import json
import time


# 初始化
url='https://192.168.11.100'
private_token='TSHDJshaskjgfsfjfkaf'
auto_git = gitlab.Gitlab(url=url, private_token=private_token)

# 获取所有项目的列表
def get_all_project():
    all_project = auto_git.projects.list(all=True)
    for project in all_project:
        # print(project.name, project.last_activity_at)
        print("=====================")
        if project.last_activity_at > "2020-02-01":
            print(project.name, project.last_activity_at)
            try:
                tree_all = project.repository_tree()
                for tree in tree_all:
                    print(tree)
            except:
                pass


# 获取所有用户的列表
def get_all_user():
    all_user = auto_git.users.list(all=True)
    for user in all_user:
        print(user)
        print(user.username)


# 获取所有组的列表
user_list = []
def get_all_group():
    all_group = auto_git.groups.list(all=True)
    for group in all_group:
        # print("=================================")
        print(group.id, group.name)
        # print("#################################")
        mem_all = group.members.list(all=True)
        for mem in mem_all:
            # print(mem)
            if mem.state == "active":
                if mem.username not in user_list:
                    user_list.append(mem.username)
                    print(mem.username, mem.id, mem.state, mem.access_level)
            else:
                pass
    print(len(user_list))


# 创建组
def create_group(group_info):
    '''
    group_info = {'name': 'group1', 'path': 'group1'}
    '''
    group = auto_git.groups.create(group_info)

# 获取project信息
def get_project_info():
    project_all = auto_git.projects.list(all=True)
    app_list = []
    app_info_list = []
    for project in project_all:
        appinfo = {
            "app_id": project.id,
            "app_name": project.name
        }
        app_info_list.append(appinfo)
        app_list.append(project.name)
    app = {
        'app_list': app_list,
        'app_info_list': app_info_list
    }
    return app

# 获取group_id
def get_group_id(group_name):
    try:
        group = auto_git.groups.get(group_name)
        group_id = group.id
        # print(group_id)
        return group_id
    except Exception as e:
        group_id = ""
        # print(e, group_id)
        group_info = {'name': group_name, 'path': group_name}
        create_group(group_info)
        time.sleep(3)
        get_group_id()

# 创建项目
def create_project(project_info):
    '''
    project_info = {'name': 'cloud-test', 'namespace_id': group_id}
    '''
    try:
        app = get_project_info()
        app_list = app["app_list"]
        if project_info['name'] in app_list :
            return project_info['name']
        else:
            pro_resp = auto_git.projects.create(project_info)
            # print(pro_resp)
            time.sleep(3)
            create_project(project_info)               
    except Exception as e:
        print(e)


# 创建分支
def create_branch(project):
    '''
    默认创建 dev、test
    '''
    try:
        project.branches.create({'branch': 'dev', 'ref': 'master'})
        project.branches.create({'branch': 'test', 'ref': 'master'})
        print("branches create is ok")
    except Exception as e:
        print(e)



def create(project_init):
    group_id = get_group_id(project_init["group_name"])
    project_info = {'name': project_init["app_name"], 'namespace_id': group_id}
    create_project(project_info)
    # print("++++++++")
    app = get_project_info()
    # print(app)
    for app_info in app["app_info_list"]:
        if project_init['app_name'] == app_info["app_name"]:
            # print(app_info)
            end_info = app_info
        else:
            pass
    project = auto_git.projects.get(end_info["app_id"])
    create_branch(project)
    response_json = {
        "app_name": project.name,
        "group_name": project.namespace["name"],
        "ssh_url_to_repo": project.ssh_url_to_repo
    }
    return response_json



# if __name__ == "__main__":
#     project_init = {'app_name': 'test-app-2007', 'group_name': 'cloud-test'}

#     create(project_init)

