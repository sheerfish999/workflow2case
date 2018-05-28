# -*- coding: utf-8 -*-


import os
import shutil

import sys
if sys.version_info.major==2:   #python2
	import HTMLParser  #pip install HTMLParser
	import urllib2 

if sys.version_info.major==3:   #python3
	from html import parser as HTMLParser
	from urllib import request as urllib2  

from doxml import *
from doxmind import *


#####  由处理后的 list 中 id 转 title、 type

def id2title(id,lists):

	for x in range(len(lists)):
		if id==lists[x][1]:
			title=lists[x][0].strip()
			types=lists[x][3]
			break

	return title,types


################################# list 生成带有结构的 xml

def list2xml(lists,endtitle):

	## 创建起始节点
	filename="null.xml"

	start_node_id=lists[0][1]
	start_node_value=lists[0][0]

	f=open(filename,"w")
	#f.write(r"<start></start>")
	f.write(r"<node_" + start_node_id + "></node_" + start_node_id + ">")
	f.close()
	#xpath='//start'
	xpath='//node_' + start_node_id

	xmldoc=XmlDocment(filename)	
	ele_lists=xmldoc.ele_list(xpath)
	start_node=ele_lists[0]

	xmldoc.set_attr(start_node,start_node_id,attr="id")
	xmldoc.set_attr(start_node,start_node_value)
	xmldoc.set_attr(start_node,"start",attr="type")


	## 按list成员遍历

	hasadd=True  ## 本次是否成员添加

	while True:

		if hasadd==False:   ## 已经没有成员再次被添加
			break
		else:
			hasadd=False


		for i in range(len(lists)):

			list_id=lists[i][1]
			xpath="//*[@id='" + list_id + "']"

			## xml树中有该 id 特征的所有节点
			ele_lists=xmldoc.ele_list(xpath)
			#print(xpath)
			#print(len(ele_lists))
			for node in ele_lists:  ## 逐个查现有的子节点是否完整

				xml_id=xmldoc.get_attr(node,"id")

				## 找到对应的节点
				if xml_id==list_id:

					## list中该特征的子节点与xml mode列举子节点进行比较，不存在则添加，并进行标记，直到完全没有需要标记的节点则退出

					for ii in range(len(lists[i][2])):

						if 	lists[i][2][ii]=="":
							continue

						childid_fromlist=lists[i][2][ii]  ## list中的子节点
						childtitle_fromlist,childtype_fromlist=id2title(childid_fromlist,lists)  ## list中的子节点标题

						childnode_list=xmldoc.getchildren_list_byele(node)

						## 结束标记
						if endtitle==childtitle_fromlist:
							childtype_fromlist="end"

						hasnode=False

						for childnode_xml in childnode_list:  ## xml中的子节点

							childid_fromxml=xmldoc.get_attr(childnode_xml,"id")  

							if childid_fromxml==childid_fromlist:

								hasnode=True
								break

						## 不存在则添加并标记

						if hasnode==False:


							#child_node=xmldoc.insert_node(node,"node")
							child_node=xmldoc.insert_node(node,"node_" + childid_fromlist)  # 名称规则首不能为数字
							xmldoc.set_attr(child_node,childid_fromlist,attr="id")										
							
							xmldoc.set_attr(child_node,childtitle_fromlist)
							xmldoc.set_attr(child_node,childtype_fromlist,attr="type")

							hasadd=True  ## 本次有成员添加



	xml_str=xmldoc.gettext().decode("utf-8")

	## 输出进行调试

	filename="fina.xml"
	f=open(filename,"w")
	f.write(xml_str)
	f.close


	return xml_str
	


################################# xml 遍历所有 xpath , 返回 xpath list

path_list=[]
tagstack = []

class ShowStructure(HTMLParser.HTMLParser):


	def handle_endtag(self, tag): tagstack.pop()

	def handle_starttag(self, tag, attrs):

		tagstack.append(tag)

		this_path="/"

		for tags in tagstack:
			
			this_path=this_path+"/"+tags

		path_list.append(this_path)


def xpath_all_from_tree(xml_str):

	ShowStructure().feed(xml_str)  


################################# xpath list 转换成 可用路径


## 格式整理
def xpathlist2_pathlist(xpathlist):

	for i in range(len(xpathlist)):

		path=xpathlist[i].replace("//","")
		path=path.replace("node_","")
		path=path.replace("/",",")

		xpathlist[i]=path


	return xpathlist


##  路径 id_list id 转为 title 及类型的 list 
def pathlist2_titlepathlist(pathlist,lists):

	for ii in range(len(pathlist)):

		path_list=pathlist[ii].split(",")

		for i in range(len(path_list)):

			title,types=id2title(path_list[i],lists)

			path_list[i]= ([title,types])

		pathlist[ii]=path_list


	return pathlist



## 去掉最后一个元素不为出口的 所有节点路径,   end_str 为最后字符串特征;  并进行其它必要处理

def only_start2end_path(titlelist,end_str):

	## 只保留最后一个元素不为出口的 所有节点路径

	lastlist=[]

	for i in range(len(titlelist)):

		if titlelist[i][len(titlelist[i])-1][0] == end_str:

			lastlist.append(titlelist[i])


	## 去掉所有 list 中的头尾

	lastlist_2=[]

	for i in range(len(lastlist)):

		templist=[]

		for ii in range(1,len(lastlist[i])-1):

			templist.append(lastlist[i][ii])

		lastlist_2.append(templist)

	return lastlist_2

#################################  转换为 python 脚本


 ####  路径类脚本

def pathlist2_scipts(pathlist):

	casepath="case"

	if os.path.exists(casepath)==True:

		shutil.rmtree(casepath)

	os.mkdir(casepath)

	casetitle="case"

	##### 生成 按照路径拆分逻辑脚本   ----- 一般用不到

	"""

	for i in range(len(pathlist)):

		filepath=casepath+"/" + casetitle + str(i) + ".py"

		script=""
		tab=""  # 前置缩进记忆

		for ii in range(len(pathlist[i])):

			cmd_name=pathlist[i][ii][0]
			cmd_type=pathlist[i][ii][1]

			## 过程
			if cmd_type=="sub":
				if cmd_name[-1:]!=")":
					cmd_name=cmd_name+"()"
				script=script+ tab +cmd_name + "\n"


			## 函数
			if cmd_type=="func":
				if cmd_name[-1:]!=")":
					cmd_name=cmd_name+"()"
				script=script+ tab + cmd_name + "\n"
			
			## 判断
			if cmd_type=="select":

				if cmd_name=="else":
					cmd_name="else:"
				else:
					## = 换 ==
					if cmd_name.find("=")>=0 and  cmd_name.find(">")<0 and  cmd_name.find("<")<0 and  cmd_name.find("==")<0:
						cmd_name=cmd_name.replace("=","==")

					cmd_name="if " + cmd_name +":"


				script=script+ "\n" + tab + cmd_name + "\n"
				tab=tab+"\t"  # 增加一次缩进


		f=open(filepath,"w")
		f.writelines(script)
		f.close()	


	"""

	###### 生成 完全遍历的各个脚本 及手工测试用例， 前者可用于自动化遍历，后者可用于手工遍历

	csv=""

	for i in range(len(pathlist)):

		filepath=casepath+"/" + casetitle + str(i) + "_path.py"
		script=""

		csv=csv + str(i+1)

		for ii in range(len(pathlist[i])):

			cmd_name=pathlist[i][ii][0]
			cmd_type=pathlist[i][ii][1]

			## 过程
			if cmd_type=="sub":
				if cmd_name[-1:]!=")":
					cmd_name=cmd_name+"()"
				script=script +cmd_name + "\n"
				csv=csv + "," + cmd_name


			## 函数
			if cmd_type=="func":
				if cmd_name[-1:]!=")":
					cmd_name=cmd_name+"()"
				script=script  + cmd_name + "\n"
				csv=csv + "," + cmd_name

			## 判断
			if cmd_type=="select":
				csv=csv + "," + "如果/前置 "  + cmd_name
				pass

		## 路径脚本
		f=open(filepath,"w")
		f.writelines(script)
		f.close()

		csv=csv + "\n"


	## CSV 手工用例
	csvpath=casepath+"/" + casetitle + ".csv"

	f=open(csvpath,"w")
	f.writelines(csv)
	f.close()	



##### 全逻辑脚本,  利用 xml 文件结构和特征  可用于可视化编程

def xml2_script():

	casepath="case"

	if os.path.exists(casepath)==False:

		os.mkdir(casepath)

	xmlfile="fina.xml"
	filepath="case/case_code.py"

	#################

	f=open(xmlfile,"r")
	xml=f.read()
	f.close()

	## 分割成行
	xml=xml.replace("<node_","\n<node_")
	xml=xml.replace("</node_","\n</node_")
	xml=xml.replace("\">","\">\n")


	########### 根据逻辑生成 tab 缩进


	lastsctipt=[]
	cell=0


	## 先生成xml结构层次标号
	xmllist=xml.split("\n")
	for line in xmllist:

		if line!="":

			if line.find("<node_")>=0 or line.find("</node_")>=0:

				if line.find("<node_")>=0:
					cell=cell+1
				elif line.find("</node_")>=0:
					cell=cell-1

				lastsctipt.append([line,cell])

			else:

				lastsctipt.append([line])
	
	"""
	for lists in lastsctipt:
		print(lists)
	"""

	## 预处理

	for i in range(len(lastsctipt)):

		if len(lastsctipt[i])==2:

			## 过程
			if lastsctipt[i][0].find("type=\"sub\"")>0:
				if lastsctipt[i+1][0][-1:]!=")":
					lastsctipt[i+1][0]=lastsctipt[i+1][0]+"()"
				lastsctipt[i+1][0]=lastsctipt[i+1][0]+"\n"

			## 函数
			if lastsctipt[i][0].find("type=\"func\"")>0:
				if lastsctipt[i+1][0][-1:]!=")":
					lastsctipt[i+1][0]=lastsctipt[i+1][0]+"()"
				lastsctipt[i+1][0]=lastsctipt[i+1][0]+"\n"

			## 判断
			if lastsctipt[i][0].find("type=\"select\"")>0:
				lastsctipt[i+1][0]=htmldecode(lastsctipt[i+1][0])   # 逻辑中的各类字符

				## = 换 ==
				strs=lastsctipt[i+1][0]
				if strs.find("=")>=0 and  strs.find(">")<0 and  strs.find("<")<0 and  strs.find("==")<0:
					lastsctipt[i+1][0]=strs.replace("=","==")


				lastsctipt[i+1][0]="if " + lastsctipt[i+1][0] + ":"




	## 产生缩进  直到同级的结构层次标号

	tab=""

	for i in range(len(lastsctipt)):

		if len(lastsctipt[i])==2:

			if lastsctipt[i][0].find("type=\"select\"")>0:

				cell=lastsctipt[i][1]  ## 增加一个缩进  记录逻辑层次
				tab=tab+"\t"

				for ii in range(i+2,len(lastsctipt)):
					
					if len(lastsctipt[ii])==2:
						if lastsctipt[ii][1]==cell:  ##减少一个缩进
							tab=tab[:-1]
							break
					
					lastsctipt[ii][0]=tab + lastsctipt[ii][0]


	"""
	for lists in lastsctipt:
		print(lists)
	"""


	## 去掉头尾 只能最后去掉  避免影响层次关系

	xmllist=[]

	for i in range(len(lastsctipt)):

		if lastsctipt[i][0].find("type=\"start\"")>=0 or lastsctipt[i][0].find("type=\"end\"")>=0:
			lastsctipt[i+1][0]=""  ## python for 循环是迭代器，因此不能直接操作  不必删除 直接置空就行了
			continue
		else:
			xmllist.append(lastsctipt[i])



	"""
	for lists in xmllist:
		print(lists)
	"""



	## 去掉 xml 节点

	lastsctipt=[]

	for i in range(len(xmllist)):

		if len(xmllist[i])==2:
			continue
		else:
			lastsctipt.append(xmllist[i])


	"""
	for lists in lastsctipt:
		print(lists)
	"""


	#################

	lastsctipt_str=""


	for line in lastsctipt:
		if line[0]!="":
			lastsctipt_str=lastsctipt_str+ line[0] +"\n"

	f=open(filepath,"w")
	f.writelines(lastsctipt_str)
	f.close()	




###########################################  完整处理过程

# xmind 文件名，终点特征

def xmind2path(xmindfile, endtitle):

	# 解压出其中的 xml
	xml,stylexml=read_xmind(xmindfile)

	# 根据 xmind 中的 xml 资源前后关系生成类似list结构：
	# 下级各个节点, 最后结构类似： ['Valid', '76q1ecqiei4u494hnsu4a9cl0i', ['6690se63nn0agpf9u043icvmc4', '1je2u1g9ghg60eu0g41668akej'], type]
	lists=xml2list(xml,stylexml)
	"""
	for ele in lists:
		print(ele)
	"""

	# 根据list 生成 xml 结构树
	xml_str=list2xml(lists,endtitle)

	# 根据xml结构树 生成所有 xpath 到 list
	xpath_all_from_tree(xml_str)
	#print(path_list)

	# 整理 xpath list 到 路径 list
	pathlist=xpathlist2_pathlist(path_list)
	#print(pathlist)

	titlelist=pathlist2_titlepathlist(pathlist,lists)
	#print(titlelist)

	# 得到出口为终点的路径 并进行处理
	lastpath=only_start2end_path(titlelist,endtitle)
	"""
	for ele in lastpath:
		print(ele)
	"""

	# 将所有路径转换为 python 遍历脚本
	pathlist2_scipts(lastpath)

	# 根据xml得到逻辑伪代码
	xml2_script()


	return lastpath



###########################################

# 用法：

if __name__ == '__main__':


	## xmind 文件名
	xmindfile="test.xmind"

	## 结束节点的文本标记
	endtitle="Stop"

	lastpath=xmind2path(xmindfile, endtitle)







