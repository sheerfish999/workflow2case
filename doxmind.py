# -*- coding: utf-8 -*-

########### 本脚本用于解析 xmind, 并处理 xmind 导出的 xml 及其生成的  tree

import re
from xml.etree import ElementTree as  ET
from xml.etree.ElementTree import Element
from zipfile import ZipFile


content_xml = "content.xml"   # 主要数据
comments_xml = "comments.xml"
styles_xml="styles.xml"  # 样式


################################# xmind 提取 xml

def read_xmind(filename):

	cache = {}

	with ZipFile(filename) as xmind:
		for f in xmind.namelist():
			#print(f)  # 所有的数据
			for key in [content_xml, comments_xml, styles_xml]:
				if f == key:
					cache[key] = xmind.open(f).read().decode('utf-8')

	xml=cache[content_xml]
	stylexml=cache[styles_xml]


	## 生成供调试
	f=open(content_xml,"w")
	f.writelines(xml)
	f.close()

	f=open(styles_xml,"w")
	f.writelines(stylexml)
	f.close()


	return xml,stylexml



#################################  xmind 的xml 转 list  (非标准xml 先转 tree , 按tree处理)

def xml2list(xml,stylexml):

	lists=[]

	xml_content=xmind_content_to_etree(xml)
	
	## 起始节点
	start_node=xml_content.find('sheet').find('topic')

	ids,title,styleids=get_ele_attr(start_node)
	next_id=get_id_nextele(xml,ids)

	lists.append([title,ids,next_id])


	## 下级各个节点, 最后结构类似： ['	 Valid	 ', '76q1ecqiei4u494hnsu4a9cl0i', ['6690se63nn0agpf9u043icvmc4', '1je2u1g9ghg60eu0g41668akej'], type]

	children_nodes=xml_content.find('sheet').find('topic').find('children').find('topics')

	for children_node in children_nodes:

		ids,title,styleids=get_ele_attr(children_node)
		next_id=get_id_nextele(xml,ids)

		types=styleid2type(styleids,stylexml)  # 类型

		lists.append([title,ids,next_id,types])


	lists[0].append("start")   ### 起始节点类型
		
	return lists



# 转 etree
def xmind_content_to_etree(content):

	xml_content = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)

	return ET.fromstring(xml_content.encode('utf-8'))


#### 获取节点的 id 和  title

def get_ele_attr(ele):

	title=ele.find('title').text.strip()
	ids=ele.attrib['id']

	try:
		styleids=ele.attrib['style-id']
	except:
		#print(u"style-id取值错误,id:",ids)
		styleids=-1   # 默认的圆角矩形  没有这个key  "org.xmind.topicShape.roundedRect"  

	return ids,title,styleids

##### 获取节点的 指向的下一个元素的 id

def get_id_nextele(xml,first_id):

	xml_content=xmind_content_to_etree(xml)

	relationships=xml_content.find('sheet').find('relationships')

	## 遍历所有的 relationship

	next_id=[]
	for relationship in relationships:

		the_id=relationship.attrib['end1']

		if the_id==first_id:
			next_id.append(relationship.attrib['end2'])   # 可能有多个下一个

	if next_id==[]:
		next_id=[""]  ## 为空则置一个空

	return next_id



#####  根据 style id ，取得 style 样式，并进行转化   (非标准xml 先转 tree , 按tree处理)

def styleid2type(styleid,stylexml):

	### 查找 shape-class

	shape_class=""
	types=""

	if styleid==-1:  # 默认的圆角矩形  没有这个key
		shape_class="org.xmind.topicShape.roundedRect"

	########################

	stylexml_content=xmind_content_to_etree(stylexml) 	

	style_nodes=stylexml_content.find('styles').findall('style')

	for style_node in style_nodes:

		ids=style_node.attrib['id']

		if ids==styleid:  ## 如果相同则查找对应的  shape-class

			try:
				shape_class=style_node.getchildren()[0].attrib['shape-class']   #  相当于 style_node.find['relationship-properties'][0].attrib['shape-class']，但这个方法报错
				#print(shape_class)
			except:
				shape_class="org.xmind.topicShape.roundedRect"
				#print(u"shape-class取值错误,styleid:",styleid)

	### 转化

	if shape_class=="org.xmind.topicShape.roundedRect":
		types="sub"

	if shape_class=="org.xmind.topicShape.circle":
		types="select"

	if shape_class=="org.xmind.topicShape.diamond":
		types="func"



	return types

