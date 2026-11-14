---
title: "微信《动物餐厅》python脚本"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-08-30，现从旧站迁入。

<!-- truncate -->

P.S.想用OpenCV识别并驱赶放屁赶客人的臭鼬和偷钱的小动物。日后再添加此功能。

P.P.S. GUI反正凑凑呼呼给搭建起来了。每个控件都能用。

P.P.P.S 好像没有绑定滚动条。算了以后再弄。

![](/img/wordpress-archive/2019/08/image-91-1024x202.png)

最近玩了玩微信的小游戏动物餐厅，想搞点手段来提高排名，用python写了个自动刷钱的小程序。

程序分两个类，第一个类adbHandler用来调取adb工具控制手机模拟点击。第二个类写具体的点击模式。

首先引用包和创建config

```text
from random import random
import time
import json
import os

config = {'goLeft': {'x': 59, 'y': 1085},
'goRight': {'x': 1022, 'y': 1089},
'firstFood': {'x': 395, 'y': 802},
'firstMoney': {'x': 431, 'y': 946},
'propaganda': {'x': 963, 'y': 2014},
'offset': {"x": 270, "y": 360},
'hallMoney': {'收银台': {'x': 436, 'y': 756},
'水桌': {'x': 711, 'y': 1566}},
'kitchenMoney': {'烤炉': {'x': 75, 'y': 710},
'上案板': {'x': 930, 'y': 775},
'下案板': {'x': 440, 'y': 1640}},
'sp1': {'x': 775, 'y': 2017},  #超级宣传 三个点
 'sp2': {'x': 529, 'y': 1366},
 'sp3': {'x': 970, 'y': 80},}
```

adbHandler如下：

```text
class adbHandler:
	'''用来操纵ADB程序'''

	def execute_command(self,cmd):
		os.system('adb '+cmd)

	def click(self,x,y,info=True):
		self.execute_command('shell input tap '+str(x)+' '+str(y))
		print(f'正在点击{x},{y}')

	def swipe(self,x1,y1,x2,y2,time):
		self.execute_command('shell input swipe '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+time)
```

adb是google提供的安卓调试工具，需要提前下载好并加入PATH。adb shell input X Y 命令行输入后会模拟点击手机上的X,Y位置。

restaurantHandler类的初始化有三个参数，第一个是新建一个adbHandler对象用于调用adb程序(P.S.修改:后来不在类内新建了，改为传入)。

然后引入config字典，记录坐标信息。

最后的self.screen保存一个字符串用来判断当前场景位置，我的账号还没达到开通garden的等级，所以先只写两个场景，hall和kitchen。

chscr函数读取screen信息，并负责切换场景。

pickMoney和serveFood读取config中的坐标，完成捡钱和上菜的功能。

clickPropaganda自动按照三个位置的顺序完成一次浏览广告的操作。

如下：

```text
class restaurantHandler:
	'''具体的操作流程'''
	def __init__(self):
		self.adbHandler = adbHandler()
		self.config = config
		self.screen = 'hall'
	def chscr(self,scr):
		'''变换场景,默认现在只有大厅和厨房两个场景'''
		if self.screen=='hall' and scr=='kitchen':
			self.adbHandler.click(self.config['goRight']['x'],self.config['goRight']['y'])
			self.screen='kitchen'
		if self.screen=='kitchen' and scr=='hall':
			self.adbHandler.click(self.config['goLeft']['x'],self.config['goLeft']['y'])
			self.screen='hall'
	def pickMoney(self):
		if self.screen=='hall':
			# 捡餐费
			for i in range(0,3):				self.adbHandler.click(self.config['firstMoney']['x']+self.config['offset']['x']*i,self.config['firstMoney']['y'])
				time.sleep(0.5)
				self.adbHandler.click(self.config['firstMoney']['x']+self.config['offset']['x']*i,self.config['firstMoney']['y']+self.config['offset']['y'])
				time.sleep(0.5)
			# 捡小费
			for location in self.config['hallMoney'].items():
				self.adbHandler.click(location[1]['x'],location[1]['y'])
				time.sleep(0.5)
		if self.screen=='kitchen':
			# 捡小费
			for location in self.config['kitchenMoney'].items():
				self.adbHandler.click(location[1]['x'],location[1]['y'])
				time.sleep(0.5)
	def serveFood(self):
		'''上菜'''
		for i in range(0, 2):
			for j in range(0, 3):
				x = self.config['firstFood']['x'] + self.config['offset']['x'] * j
				y = self.config['firstFood']['y'] + self.config['offset']['y'] * i

				print(f'点击第 {(i * 3) + (j + 1)} 桌订单')
				self.adbHandler.click(x, y)
				time.sleep(0.5)  #不sleep会导致点击频繁应用无法识别
	def clickPropaganda(self,number):
		print(f'\n点击 {number} 次宣传按钮\n')
		for i in range(0, number):
			self.adbHandler.click(self.config['propaganda']['x'], self.config['propaganda']['y'])
			time.sleep(0.5)

	def clickSuperPropaganda(self):

		self.adbHandler.click(self.config['sp1']['x'], self.config['sp1']['y'])
		time.sleep(1)
		self.adbHandler.click(self.config['sp2']['x'], self.config['sp2']['y'])
		time.sleep(34)
		self.adbHandler.click(self.config['sp3']['x'], self.config['sp3']['y'])
```

场景如下两图，打开开发者模式找准具体的位置坐标是关键。

![](/img/wordpress-archive/2019/09/image-18.png)

以下是DEBUG过程：

有一个这样的字典d=\{'a':\{'x':1,'y':1\},'b':\{'x':2,'y':2\}\}，即字典的值是另一个字典。本来以为用for循环，for i in d，得到的i是包含xy的字典，然而报错，其实返回的是内字典的键值，是一个str类型的值。也就是说，python中，for i in d和for i in d.keys()等价。

![](/img/wordpress-archive/2019/08/image-89-300x275.png)

![](/img/wordpress-archive/2019/08/image-81.png)

最后用items()解决了。

![](/img/wordpress-archive/2019/08/image-83.png)

然后接上数据线测试，发现怎么都不生效。本来以为是adb控制手机需要开启ROOT权限，但是查询了一下说并不需要，毕竟是google亲儿子，adb可以开后门2333. 最后发现是小米这个后妈对android做了点手脚。

MIUI开启开发者模式之后需要单独开启模拟点击权限才能使用adb shell input tap。

![](/img/wordpress-archive/2019/09/image-19.png)

脚本的效果很好。要不我试一下用tkinter包装成GUI界面？干。

写tkinter的过程中碰到一个难题，不知道怎么把每次点击产生的日志更新到屏幕上去，碰到了循环依赖的问题。我用你，你用我，哪个放前面都会导致产生referenced before assignment 的错误，尴尬。想一会儿。。。。

把adbHandler在main中生成，和text控件一起传进去，解决了。

```text
from random import random
import time
import json
import os

from tkinter import *
from tkinter import ttk

config = {'goLeft': {'x': 59, 'y': 1085},
'goRight': {'x': 1022, 'y': 1089},
'firstFood': {'x': 395, 'y': 802},
'firstMoney': {'x': 431, 'y': 946},
'propaganda': {'x': 963, 'y': 2014},
'offset': {"x": 270, "y": 360},
'hallMoney': {'收银台': {'x': 436, 'y': 756},
'水桌': {'x': 711, 'y': 1566}},
'kitchenMoney': {'烤炉': {'x': 75, 'y': 710},
'上案板': {'x': 930, 'y': 775},
'下案板': {'x': 440, 'y': 1640}},
'sp1': {'x': 775, 'y': 2017},  #超级宣传 三个点
 'sp2': {'x': 529, 'y': 1366},
 'sp3': {'x': 970, 'y': 80},}

class adbHandler:
	'''用来操纵ADB程序'''
	def execute_command(self,cmd):
		os.system('adb '+cmd)

	def click(self,x,y):
		self.execute_command('shell input tap '+str(x)+' '+str(y))
		#self.txt.insert('insert',f'正在点击{x},{y}'+'\n')
		#self.txt.update()

	def swipe(self,x1,y1,x2,y2,time):
		self.execute_command('shell input swipe '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+time)

class restaurantHandler:

	'''具体的操作流程'''

	def __init__(self,handler,txt):
		self.adbHandler = handler
		self.config = config
		self.screen = 'hall'
		self.txt = txt

	def chscr(self,scr):
		'''变换场景,默认现在只有大厅和厨房两个场景'''
		if self.screen=='hall' and scr=='kitchen':
			self.adbHandler.click(self.config['goRight']['x'],self.config['goRight']['y'])
			self.screen='kitchen'
		if self.screen=='kitchen' and scr=='hall':
			self.adbHandler.click(self.config['goLeft']['x'],self.config['goLeft']['y'])
			self.screen='hall'
	def pickMoney(self):
		if self.screen=='hall':
			# 捡餐费
			for i in range(0,3):
				self.adbHandler.click(self.config['firstMoney']['x']+self.config['offset']['x']*i,self.config['firstMoney']['y'])
				time.sleep(0.5)
				self.adbHandler.click(self.config['firstMoney']['x']+self.config['offset']['x']*i,self.config['firstMoney']['y']+self.config['offset']['y'])
				time.sleep(0.5)
			# 捡小费
			for location in self.config['hallMoney'].items():
				self.adbHandler.click(location[1]['x'],location[1]['y'])
				time.sleep(0.5)

		if self.screen=='kitchen':
			# 捡小费
			for location in self.config['kitchenMoney'].items():
				self.adbHandler.click(location[1]['x'],location[1]['y'])
				time.sleep(0.5)

	def serveFood(self):
		'''上菜'''
		for i in range(0, 2):
			for j in range(0, 3):
				x = self.config['firstFood']['x'] + self.config['offset']['x'] * j
				y = self.config['firstFood']['y'] + self.config['offset']['y'] * i

				self.txt.insert('insert',f'点击第 {(i * 3) + (j + 1)} 桌订单'+'\n')
				self.txt.update()

				self.adbHandler.click(x, y)
				time.sleep(0.5)  #不sleep会导致点击频繁应用无法识别

	def clickPropaganda(self,number):

		for i in range(0, number):
			self.adbHandler.click(self.config['propaganda']['x'], self.config['propaganda']['y'])
			self.txt.insert('insert',f'点击第 {i} 次宣传按钮'+'\n')
			self.txt.update()
			time.sleep(0.5)

	def clickSuperPropaganda(self):

		self.adbHandler.click(self.config['sp1']['x'], self.config['sp1']['y'])
		time.sleep(1)
		self.adbHandler.click(self.config['sp2']['x'], self.config['sp2']['y'])
		time.sleep(34)
		self.adbHandler.click(self.config['sp3']['x'], self.config['sp3']['y'])

class tkGUI:
	def __init__(self,master,restaurantHandler):
		self.master = master
		self.initWidgets()
		self.restaurantHandler = restaurantHandler

	def initWidgets(self):

		bt1 = ttk.Button(self.master,text='捡餐厅的小钱钱',command=self.pickHallMoney)
		bt1.pack(expand=True,side=LEFT)

		bt2 = ttk.Button(self.master,text='捡厨房的小钱钱',command=self.pickKitchenMoney)
		bt2.pack(expand=True,side=LEFT)

		bt3 = ttk.Button(self.master,text='上菜',command=self.serveFood)
		bt3.pack(expand=True,side=RIGHT)

		bt4 = ttk.Button(self.master,text='全自动',command=self.allTogether)
		bt4.pack(expand=True,side=TOP)
	def pickHallMoney(self):
		if self.restaurantHandler.screen=='hall':
			self.restaurantHandler.pickMoney()
		else:
			self.restaurantHandler.chscr('hall')
			self.restaurantHandler.pickMoney()
	def pickKitchenMoney(self):
		if self.restaurantHandler.screen=='kitchen':
			self.restaurantHandler.pickMoney()
		else:
			self.restaurantHandler.chscr('kitchen')
			self.restaurantHandler.pickMoney()
	def serveFood(self):
		if self.restaurantHandler.screen == 'hall':
			self.restaurantHandler.serveFood()
		else:
			self.restaurantHandler.chscr('hall')
			self.restaurantHandler.serveFood()
	def allTogether(self):
		while True:
			r=self.restaurantHandler
			r.serveFood()
			r.pickMoney() # 捡大厅的钱
			r.chscr('kitchen')
			r.pickMoney() # 捡厨房的钱
			r.chscr('hall')
			r.serveFood()
			r.pickMoney() # 捡大厅的钱
			r.chscr('kitchen')
			r.pickMoney() # 捡厨房的钱
			r.chscr('hall')
			r.serveFood()
			r.pickMoney() # 捡大厅的钱
			r.chscr('kitchen')
			r.pickMoney() # 捡厨房的钱
			r.chscr('hall')
			r.serveFood()
			r.pickMoney() # 捡大厅的钱
			r.chscr('kitchen')
			r.pickMoney() # 捡厨房的钱
			r.chscr('hall')
			r.clickSuperPropaganda()

def main():

	'''
	写的好乱
	先新建一个root根窗口
	然后创建text文本框并绑定到root
	然后建立一个adbhandler用来处理点击请求
	然后建立restaurantHandler，传入前面建立的adb和txt文本框，内部使用adb操作指令
	每操作完一次就用txt文本框更新日志显示到屏幕上
	最后tkGUI创建剩余部分的Button控件并内部绑定restaurantHandler的函数
	所以需要传入root和r对象
	反正现在能用了
	试试用pyinstaller打包
	'''

	print('请手动移动到大厅')
	root = Tk()
	root.title('动物餐厅自动点击工具')

	txt = Text(root,width=32,height=5)
	txt.pack()

	adb = adbHandler()
	r = restaurantHandler(handler=adb,txt=txt)

	gui = tkGUI(root,r)

	root.mainloop()

main()
```
