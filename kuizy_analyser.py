#!/usr/bin/python
# -*- coding: <encoding utf-8> -*-

import requests
from bs4 import BeautifulSoup

import itertools
import json


def get_choice_list(url):
    
    print("[+] HTTPreq to kuizy...")
    print(url)
    res = requests.get(url)
    
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find("title")
    print("*"*60)
    print(title.text)
    print("*"*60)
    
    secs = soup.find_all("section" ,class_="quiz box-container")
    for sec in secs:
        print(sec.text.strip())
        print("*"*60)

    lis = soup.find_all("li")
    choice_list=[]
    for li in lis:
        if not li.get("onclick") == None:
            if li.get("onclick").startswith("selected"):
                choice_list.append(li.get("onclick"))

    for s in res.text.split("\n"):
        if "var options =" in s:
            s = s.split("[")[1]
            s = s.split("]")[0]
            s = "["+s+"]"
            pick_list = json.loads(s)

    print("診断結果候補")
    for pick in pick_list:
        print("index:",pick["index"],pick["title"])
    print("*"*60)

    choice_list = beautify_choice_list(choice_list)
    
    return choice_list,pick_list


def beautify_choice_list(choice_list):
    bea_lis=[]
    for i in range(len(choice_list)):
        s = choice_list[i].replace("selected(","")
        s = s.split("]")[0]
        scores = s.split("[")[1]
        q_pa = s.split("[")[0].split(",")[0].strip()
        q_ch = s.split("[")[0].split(",")[1].strip()
        q_id = q_pa + "-" + q_ch
        bea_lis.append({"id":q_id, "parent":q_pa, "child":q_ch, "scores":scores})
        
    return bea_lis


def calc_scores(q_ids):
    ret = []
    for q_id in q_ids:
        sc = id2score(q_id,choice_list)
        if ret == []:
            ret = sc.split(",")
        else:
            # a = '0, 0, 0, 1, 1, 0, 1, 0, 1, 0'
            # b = '0, 0, 0, 1, 1, 0, 1, 0, 1, 0'
            # c=a+b
            temp = []
            sc = sc.split(",")

            for i in range(len(ret)):
                temp.append(str(int(ret[i].strip()) + int(sc[i].strip())))
            ret = temp

    max_score = max(ret)
    max_index = ret.index(max(ret))
    
    return max_score, max_index


def id2score(q_id,choice_list):
    ret=""
    for l in choice_list:
        if l["id"] == q_id:
            ret = l["scores"]
    return ret
    

def kuizy_roundrobin(choice_list, pick_list):
    roundrobin = []
    q_id = 1
    li = []
    first = True

    while True:
        temp=[]
        for a in choice_list:
            if a["parent"] ==  str(q_id):
                temp.append(a["id"])
        if first == True:
            li = temp
            first = False
        else:
            li = itertools.product(li, temp)

        q_id += 1
        
        flag = False
        for a in choice_list:
            if a["parent"] == str(q_id):
                flag = True
        if flag == False:
            break

    result = []
    for i,v in enumerate(li):
        v = str(v).replace("(","")
        v = v.replace(")","")
        v = v.replace("'","")
        v = v.replace(" ","")
        score,index = calc_scores(v.split(","))
        result.append([v,score,index])

    for i in range(len(choice_list[0]["scores"].split(","))):
        num = 0
        for r in result:
            if r[2] == i:
                num += 1
        print("index:",i,"パターン数",num)

    ind = int(input("[?] どの結果になりたい？:"))
    for pick in pick_list:
        if pick["index"] == ind :
            print(pick["title"])

    i = 0
    cat = 20
    for r in result:
        if r[2] == ind:
            print(r[0])
            i += 1
            if i > cat:
                print("[!]",cat,"件まで表示")
                break

if __name__ == '__main__':
    url = input("[?] 解析したいkuizyの診断URL? (例 https://kuizy.net/analysis/4034/6) :")
    choice_list,pick_list = get_choice_list(url)
    kuizy_roundrobin(choice_list,pick_list)

