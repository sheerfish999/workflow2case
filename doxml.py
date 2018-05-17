# -*- coding: utf-8 -*-

########### 本脚本用于解析标准 xml

from lxml import etree  # pip install lxml

class XmlDocment():

	xmldoc=""

	### xmldoc  tree 对象
	def __init__(self,filename):

		self.xmldoc = etree.parse(filename)


	### xpath特征对象的 list  注意是符合该 xpath 特征的所有对象 例如第一个对象为  lists[0]
	def ele_list(self,xpath):

		lists=[]

		for eles in self.xmldoc.xpath(xpath):

			lists.append(eles)

		return lists


	### 对象的 子对象的list 

	def getchildren_list_byele(self,eles):

		eles_childrens=[]

		for eles_children in eles.getchildren():  

			eles_childrens.append(eles_children)

		return eles_childrens


	### 注意是符合该 xpath 特征的所有对象的子对象  例如第一个对象的第一个子对象为  lists[0][0]

	def getchildren_list(self,xpath):

		lists=[]

		for eles in self.xmldoc.xpath(xpath):

			eles_childrens=self.getchildren_list_byele(eles)

			lists.append(eles_childrens)

		return lists


	### 获得对象的某个属性
	def get_attr(self,ele,attr=""):

		ret=""
		if attr=="":
			ret=htmldecode(ele.text)
		else:
			ret=ele.attrib.get(attr)

		return ret

	### 设置对象的某个属性
	def set_attr(self,ele,value,attr=""):

		if attr=="":
			ele.text=value
		else:
			ele.set(attr, value)


	### 插入子节点
	def insert_node(self,father_ele,child_node_name):

		child_node = etree.SubElement(father_ele, child_node_name)

		return child_node



	#### 完整的 xml 信息  供输出和调试
	def gettext(self):

		ret=etree.tostring(self.xmldoc, pretty_print=True)

		return ret



## 字符转换

def htmldecode(strs):


	strs=strs.replace("&amp;","&")
	strs=strs.replace("&lt;","<")
	strs=strs.replace("&gt;",">")
	strs=strs.replace("&nbsp;"," ")


	return strs



###########################################


if __name__ == '__main__':


	filename="./test/test1.xml"
	xmldoc=XmlDocment(filename)

	### 返回成员
	xpath="//*[@lang='en']"
	ele_lists=xmldoc.ele_list(xpath)  #一维list
	print(len(ele_lists))

	xpath='//book'
	ele_lists=xmldoc.ele_list(xpath)  #一维list
	print(ele_lists)

	ele_lists=xmldoc.getchildren_list(xpath)  # 二维list
	print(ele_lists)

	### 成员属性

	ele=ele_lists[0][0]
	ret=xmldoc.get_attr(ele)
	print(ret)

	ret=xmldoc.get_attr(ele,"lang")
	print(ret)


	### 添加节点
	child_node=xmldoc.insert_node(ele,"test1")
	xmldoc.set_attr(child_node,"11111111")
	xmldoc.set_attr(child_node,"22222222",attr="attr")

	### 当前 xml
	ret=xmldoc.gettext()
	print(ret)

