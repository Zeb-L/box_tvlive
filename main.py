import os
import urllib.request
import urllib.error
import urllib.parse
import datetime
import re
import requests
import json
import base64

def gdpd():
    with open("./name.txt",'r',encoding='UTF-8') as filecont:    
        datalists = filecont.readlines()
        filecont.close()
        data=[]
        for i in range(len(datalists)):
            data.append(datalists[i].replace("\n",""))
        return data

def getsttings(num):
    setting_str=[]
    with open("./settings.txt",'r',encoding='UTF-8') as filecont:
        contents=filecont.readlines()
    filecont.close()
    for i in range(len(contents)):
        setting_str.append(contents[i].split("=")[1].replace("\n",""))
    return setting_str[num]

ys_str = ["cctv"]
ws_str = ["卫视"]
ty_str = ["体育","體育","cctv5","cctv-5"]
dy_str = ["影视","影院","电影","cctv6","cctv-6"]
yy_str = ["音乐","cctv15","cctv-15"]
xw_str = ["新闻","新聞","cctv13","cctv-13"]
se_str = ["少儿","卡通","动画","cctv14","cctv-14"]
xq_str = ["戏曲","戏剧"]
gd_str = gdpd()
alldata_lists=[]
keep_lists=[]
owner=getsttings(0)
repo=getsttings(1)
branch=getsttings(2)
token = os.environ['BFtoken']
def get_ua():
    import random
    user_agents = [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
		"Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
		"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"
    ]
    user_agent = random.choice(user_agents)
    return user_agent


def printlog(logstr):
	with open("log.txt","a") as file:
		timeNow = datetime.datetime.now()
		timeN= timeNow.strftime('%Y/%m/%d %H:%M:%S')
		file.write("\n "+timeN+": ")
		file.write("\n 》》》"+logstr+"\n")
		print("\n "+timeN+": ")
		print("\n          "+logstr+"\n")
		file.close()


def downloadfile(dlurl,i,utype):
	global alldata_lists
	global keep_lists
	reconnect = 3
	for rc in range(reconnect):
		if rc < reconnect:
			ua = get_ua()
			headers = {'User-Agent': ua}
			try:
				_url = urllib.request.Request(dlurl,headers=headers)
				response = urllib.request.urlopen(_url, None, 10)
				data=response.read().decode('utf-8')
				if utype == "m":
					datalists=data.split("\n")
					mdata=[]
					for i in range(len(datalists)):
						if datalists[i].startswith('#EXTINF'):
							if datalists[i+1] == "\n" or datalists[i+1] == "" or datalists[i+1] == "\r":
								name = datalists[i+2]
							else:
								name = datalists[i+1]
							renameurl = str(datalists[i].split(",")[1].replace("\n","").replace("\r",""))+","+str(name.replace("\n","").replace("\r",""))
							mdata.append(renameurl)
					# # f.write(mdata)
					# print(mdata)
					for m in range(len(mdata)):
						alldata_lists.append(mdata[m])
					printlog("【Success】: "+dlurl)
				elif utype == "t":
					# f.write(data)
					tdata = data.split("\n")
					for item in range(len(tdata)):
						t = tdata[item].replace("\uFEFF", "").replace("\r", "")
						t_temp = t.find(",")
						if t_temp != -1:
							alldata_lists.append(t)
					printlog("【Success】: "+dlurl)
				elif utype == "k":
					# f.write(data)
					kdata = data.split("\n")
					for item in range(len(kdata)):
						k = kdata[item].replace("\uFEFF", "").replace("\r", "")
						k_temp = k.find(",")
						if k_temp != -1:
							keep_lists.append(k)
					printlog("【Success】: "+dlurl)
				break
			except:
				printlog("Error:【连接超时】 "+dlurl)
				printlog("重试第"+str(rc+1)+"次")
				if str(rc+1) == "3":
					printlog("Error:【链接失效】 "+dlurl)
				continue


def dl_file():
	with open("./data.txt",'r',encoding='UTF-8') as filecont:    
		datalists = filecont.readlines()
		filecont.close()
	for i in range(len(datalists)):
		urldata=datalists[i].split("@=")
		if urldata[0] == "m3u":
			downloadfile(urldata[1],i,"m")
		elif urldata[0] == "txt":
			downloadfile(urldata[1],i,"t")
		elif urldata[0] == "keep":
			downloadfile(urldata[1],i,"k")


def checkM3U8(m_url):
	try:
		ua = get_ua()
		headers = {'User-Agent': ua}
		r=urllib.request.Request(url=m_url,headers=headers)
		response=urllib.request.urlopen(r,timeout=2)
		if str(response.status) == '200':
			return "ok"
	except:
		return "no"
	response.close()


def jdt(start,end):
    one = end / 20
    bfb = round(start/end * 100, 2)
    if start < one:
        pt=" 进度条"+" [--------------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*2:
        pt=" 进度条"+" [#-------------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*3:
        pt=" 进度条"+" [##------------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*4:
        pt=" 进度条"+" [###-----------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*5:
        pt=" 进度条"+" [####----------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*6:
        pt=" 进度条"+" [#####---------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*7:
        pt=" 进度条"+" [######--------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*8:
        pt=" 进度条"+" [#######-------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*9:
        pt=" 进度条"+" [########------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*10:
        pt=" 进度条"+" [#########-----------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*11:
        pt=" 进度条"+" [##########----------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*12:
        pt=" 进度条"+" [###########---------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*13:
        pt=" 进度条"+" [############--------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*14:
        pt=" 进度条"+" [#############-------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*15:
        pt=" 进度条"+" [##############------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*16:
        pt=" 进度条"+" [###############-----] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*17:
        pt=" 进度条"+" [################----] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*18:
        pt=" 进度条"+" [#################---] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*19:
        pt=" 进度条"+" [##################--] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*20:
        pt=" 进度条"+" [###################-] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif start >= one*20:
        pt=" 进度条"+" [####################] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt


def checkLists(lists):
    onlineList=[]
    for i in range(len(lists)):
        jdt2 = jdt(i+1,len(lists))
        print('\r',"【直播源检查】 "+str(jdt2),end=' ')
        # print("【直播源检查】 "+str(i)+" / "+str(len(lists)),end='\r')
        url=lists[i].split(",")[1]
        check_url = checkM3U8(url)
        if check_url == "ok":
            onlineList.append(lists[i])
    return onlineList


def reset_url_lists(allLists,string):
    data_lists=[]
    for i in range(len(string)):
        for j in range(len(allLists)):
            cont = allLists[j].split(",")
            searchitem = re.compile(string[i],re.IGNORECASE)
            item = searchitem.search(cont[0])
            if str(item) != "None":
                rename = cont[0].split("[")[0]
                if len(rename) < 10:
                # print(cont[0].replace(" ","").replace('\uFEFF', '')+","+cont[1])
                    searchttp = re.compile(r"#http",re.IGNORECASE)
                    searchttp2 = searchttp.search(cont[1])
                    m3u8url=[]
                    if str(searchttp2) == "None":
                        m3u8url.append(cont[1])
                    else:
                        m3u8urllist = cont[1].replace("#http","http").split("http")
                        for li in range(len(m3u8urllist)):
                            if m3u8urllist[li] != "":
                                m3u8url.append("http"+m3u8urllist[li])
                                # print(m3u8url)
                    if len(m3u8url) == 1:
                        data_lists.append(cont[0].replace(" ","").replace("\n","").replace("\t","").replace("\uFEFF", "")+","+m3u8url[0].replace("\n","").replace("\t","").replace(" ",""))
                    else:
                        for y in range(len(m3u8url)):
                            data_lists.append(cont[0].replace(" ","").replace("\n","").replace("\t","").replace("\uFEFF", "")+","+m3u8url[y].replace("\n","").replace("\t","").replace(" ",""))
    return data_lists


def rd(lists,title):
    tem=[]
    relists=[]
    for item in range(len(lists)):
        reitem = lists[item].split(",")
        if reitem[1] != "#genre#":
            if reitem[1] not in tem:
                tem.append(reitem[1])
                relists.append(lists[item])
    tem=[]
    printlog(title+" 源数量:"+str(len(lists))+"  去重后: "+str(len(relists)))
    return relists

def px(lists):
    str2=lists
    pxmc = []
    for i in range(len(str2)):
        str3 = str2[i].split(",")[0]
        str0 = re.findall(r"\d+\.?\d*",str3)
        if len(str0) == 0:
            pxmc.append("999")
        else:
            pxmc.append(int(float(str0[0])))
    # print("\n源数据")
    # print(pxmc)
    index=[]
    pxh=sorted(pxmc, key=int, reverse=False)
    # print("排序后")
    # print(pxh)
    # print("排序前位置")
    tem=[]
    wz=[]
    for y in range(len(pxmc)):
        index = [i for i,val in enumerate(pxmc) if val==pxh[y]]
        # print(index)
        if index != tem:
            wz=wz+index
        tem=index
    # return wz
    tem=[]
    index=[]
    pxmc=[]
    pxlist=[]
    for bf in range(len(wz)):
        z=int(wz[bf])
        pxlist.append(str2[z])
    return pxlist

def start(lists,str_list,title):
	data_lists = reset_url_lists(lists,str_list)
	rd_data_list = rd(data_lists,title)
	print("开始检查\n")
	ol_d_l = checkLists(rd_data_list)
	printlog(title+"  【全部源数量:  "+str(len(data_lists))+"  |  去重后源数量:  "+str(len(rd_data_list))+"  |  在线源数量:  "+str(len(ol_d_l))+" 】")
	print("\n")
	px_ol_d_l = px(ol_d_l)
	with open("live_lists.txt","a", encoding='utf-8') as file:
		file.write("\n")
		file.write(title+",#genre#\n")
		for line in range(len(px_ol_d_l)):
			file.write(px_ol_d_l[line]+"\n")
		file.close()


def start_keeplist():
	if keep_lists != []:
		with open("live_lists.txt","a", encoding='utf-8') as file:
			file.write("\n")
			file.write("自选频道,#genre#\n")
			for line in range(len(keep_lists)):
				file.write(keep_lists[line]+"\n")
			file.close()


def rep_text(old,new):
    with open(r'live_lists.txt', 'r',encoding='UTF-8') as file:
        data = file.read()
        data = data.replace(old, new)
        file.close()
    with open(r'live_lists.txt', 'w',encoding='UTF-8') as file:
        file.write(data)
        file.close()


def rep_lists():
	rep_list=[
		"央视频道,#genre#@📺央视频道,#genre#",
		"卫视频道,#genre#@📡卫视频道,#genre#",
		"体育频道,#genre#@🏀体育频道,#genre#",
		"影视频道,#genre#@📽️影视频道,#genre#",
		"音乐频道,#genre#@🎵音乐频道,#genre#",
		"新闻频道,#genre#@📰新闻频道,#genre#",
		"少儿频道,#genre#@🧒🏻少儿频道,#genre#",
		"戏曲频道,#genre#@📻戏曲频道,#genre#",
		"自选频道,#genre#@📹自选频道,#genre#",
		"更多频道,#genre#@🛰️更多频道,#genre#"
	]

	for r_l in range(len(rep_list)):
		title_name = rep_list[r_l].split("@")
		rep_text(title_name[0],title_name[1])

def tobase64(filename):
    filepath = './'+filename
    with open(filepath, 'rb') as base64_:
        base64_str = base64.b64encode(base64_.read())
        str0 = base64_str.decode('utf-8')
        return str0

def update_file(filename):
    global owner
    global repo
    global token
    content=tobase64(filename)
    url="https://api.github.com/repos/"+owner+"/"+repo+"/contents/"+filename
    branchurl="https://api.github.com/repos/"+owner+"/"+repo+"/branches/"+branch
    res=requests.get(branchurl)
    resp=json.loads(res.text)
    treeurl=resp["commit"]["commit"]["tree"]["url"]
    res2 =requests.get(treeurl)
    _cont = json.loads(res2.text)
    all_filename = _cont["tree"]
    sha_cont=""
    for i in range(len(all_filename)):
        lists_filename = all_filename[i]["path"]
        if lists_filename == filename:
            # print(all_filename[i]["sha"])
            sha_cont = all_filename[i]["sha"]
            break
    ua = get_ua()
    headers = {'User-Agent': ua,'Accept': 'application/vnd.github.v3+json','Authorization': 'token '+token}
    data = {"message":"actions update","content": content,"sha":sha_cont,"branch":branch}
    req = requests.put(url=url, data=json.dumps(data), headers=headers)
    print(req.text)
    return str(req).find("200")


dl_file()

alllists = rd(alldata_lists,"全部")
px_alllists=px(alllists)

with open("all_list.txt","a", encoding='utf-8') as file:
	for line in range(len(px_alllists)):
		file.write(px_alllists[line]+"\n")
	file.close()

up_alllists = update_file("all_list.txt")
if up_alllists != -1:
    printlog("all_list.txt 已经更新")
else:
    printlog("all_list.txt 更新失败")



start(alldata_lists,ys_str,"央视频道")

start(alldata_lists,ws_str,"卫视频道")

start(alldata_lists,ty_str,"体育频道")

start(alldata_lists,dy_str,"影视频道")

start(alldata_lists,yy_str,"音乐频道")

start(alldata_lists,xw_str,"新闻频道")

start(alldata_lists,se_str,"少儿频道")

start(alldata_lists,xq_str,"戏曲频道")

start_keeplist()

start(alldata_lists,gd_str,"更多频道")

rep_lists()

up_log = update_file("log.txt")
if up_log != -1:
    printlog("log.txt 已经更新")
else:
    printlog("log.txt 更新失败")

up_live_list = update_file("live_lists.txt")
if up_live_list != -1:
    printlog("live_lists.txt 已经更新")
else:
    printlog("live_lists.txt 更新失败")


printlog("All Done!")

