#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import CleanUtils as cu
reload(sys)
sys.setdefaultencoding('utf-8')
import json, requests

#update your token here, https://github.com/settings/tokens
TOKEN = 'bf8c5276f4698c557d2cd7b15e29419e2fb0d9eb'
#query limit is 30 times per hour
MAX_PAGE = 4
#max is 100 record per page
ITEM_PER_PAGE = 10

TYPE = ['README.md','build.gradle','pom.xml']

#just for test
def mytest():
    page = '3'
    #url = "https://api.github.com/search/repositories?q=language:Java&per_page=10&page="+page#+"&access_token="+TOKEN
    payload = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    #url = 'https://api.github.com/repos/json-iterator/java/git/trees/master?recursive=1'
    url = 'https://api.github.com/repos/ReactiveX/RxJava/git/trees/master?recursive=1'
    a = requests.get(url,headers=payload)
    res = json.loads(a.content)
    for r in dict(res).get('tree'):
        r = dict(r)
        if(r.get('type')=='blob'):
            for type_choose in TYPE:
                if(type_choose in str(r.get('path'))):
                     blob_url = "https://raw.githubusercontent.com/json-iterator/java/"+'master/'+r.get('path') #'/'.join(r.get('url').split('/')[:-3])+'/'+'blob/master/'+r.get('path')
                     print blob_url


#extract information of single project
def get_information(item):

    dict_item = dict(item)
    project_name = dict_item.get("name")
    url =  dict_item.get("url")
    git_url = dict_item.get("git_url")

    #do another query for a specific project and modify GET header,query limits is 5000 per hour
    head = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    res = dict(json.loads(requests.get(url,headers=head).content))
    origin_id = res.get('id')
    topics = res.get('topics')
    description = res.get('description')
    full_name = res.get('full_name')
    file_urls = []

    get_file_url = url+'/git/trees/master?recursive=1'
    file_result = json.loads(requests.get(get_file_url).content)

    for r in dict(file_result).get('tree'):
        r = dict(r)
        if (r.get('type') == 'blob'):
            for type_choose in TYPE:
                if (type_choose in str(r.get('path'))):
                    blob_url = "https://raw.githubusercontent.com/"+full_name + '/master/' + r.get('path')
                    file_urls.append(blob_url)

    print project_name,git_url,topics,description,origin_id,file_urls
    print '************************************************************'
    return project_name,git_url,topics,description,origin_id,file_urls


#extract readme and dependency from url
def extract_info_from_file(urls):
    readme = ''
    # eg, com.android.tools.build:gradle:1.2.3, split by :
    dependency = []

    for url in urls:
        readme = cu.extract_markdown(readme)

    return readme,dependency


#main function
def crawl_url():
    id = 0
    #crawl according to pages
    for i in range(MAX_PAGE):
        id +=1
        url = "https://api.github.com/search/repositories?q=language:Java&per_page="+ str(ITEM_PER_PAGE)+"&page="+ str(i+1) + "&access_token=" + TOKEN
        request_result = requests.get(url)
        print request_result.headers.get('X-RateLimit-Remaining')
        res = json.loads(request_result.content)
        items = dict(res).get("items")
        #every page has several project
        for item in items:
            project_name, git_url, topics, description, origin_id, file_urls = get_information(item)
            readme, dependency = extract_info_from_file(file_urls)
            print readme
            print dependency


if __name__=="__main__":
    crawl_url()
    #mytest()