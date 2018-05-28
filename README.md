# workflow2case
通过绘制的xmind流程可视化文件，可直接分析生成所有遍历路径，以及python逻辑脚本，适合与各类自动化测试框架进行结合，在基础功能团操作封装完毕后，完成测试路径的覆盖遍历。

## 安装

python环境 3.x

```bash
pip install HTMLParser
pip install lxml

```

## 样例

流程图效果

![](https://github.com/sheerfish999/workflow2case/blob/master/example.png) 

### 调用方法（参考xmind2case.py）

```python

xmindfile="test.xmind"
endtitle="Stop"

lastpath=xmind2path(xmindfile, endtitle)

```

### 生成的逻辑脚本

case 目录下  case_code.py:

```python

Receive_Data()

Verify_Data()

a=test()

if a=="Y":
	b=Transform(a)

	if b>1:
		Load()

	c=select1()

	if c==5:
		e=select2(c)

		if e>=5:
			d=select4(c)

			if d<=8:
				runit()

	if c==2:
		d=select3(c)

		if d>8:
			runit()

		if d<=8:
			runit()

if a=="N":
	Report_Errors()


```

### 生成的遍历路径

生成的 case 目录下各个 casen_path.py
case 目录下 case.csv

## 基本绘图要求

1） 使用xmind中workflow类型，只能有一个起始入口和结束点 \
2） 函数使用钻石型，返回判断条件使圆形，过程使用圆角矩形

### 未来计划支持

1） 处理回环 \
2） 支持 else 逻辑条件

