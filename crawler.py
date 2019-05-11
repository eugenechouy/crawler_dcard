#encoding: utf-8
import requests
from bs4 import BeautifulSoup
import json

def find(url):
    ret = ""
    for i in range(len(url)):
        if url[i] >= '0' and url[i] <= '9':
            for j in range(i, i+9):
                ret += url[j]
            break
    return ret
        

main_url = "https://www.dcard.tw/f"
api_url = "https://www.dcard.tw/_api/posts"

file = open("result.txt", "w", encoding="UTF-8")

p = requests.Session()
resp = requests.get(main_url)
soup = BeautifulSoup(resp.text, "html.parser")
sel = soup.select("div.PostList_entry_1rq5Lf a.PostEntry_root_V6g0rd")
a = []

for s in sel:
    a.append(s["href"])

for k in range(0, 10):
    serial = find(a[-1])
    post_data = {
        "before": serial,
        "limit": "30",
        "popular": "true"
    }
    r = p.get(api_url, params=post_data, headers={ "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0" })
    data = json.loads(r.text)
    for u in range(len(data)):
        temp = "/f/pet/p/" + str(data[u]["id"]) + "-" + str(data[u]["title"].replace(" ", "-"))
        a.append(temp)

j = 0
for i in a:
    url = "http://www.dcard.tw" + i
    j += 1
    file.write("第 {} 篇, URL為: {} \n".format(j,url))
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.select("div.Post_meta_MVFsOq h1.Post_title_2O-1el")
    file.write(title[0].string + "\n")
    content = soup.select("div.Post_content_NKEl9d div div div")
    for s in content:
        if s.string:
            file.write(s.string + "\n")    
    file.write("-------------------------------------------------------\n\n")

file.close()
print("爬蟲結束")

