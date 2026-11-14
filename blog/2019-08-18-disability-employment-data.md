---
title: "对残疾人就业情况的爬虫及数据分析"
authors: [mingqiang]
tags: ["旧站归档", "Python"]
---

这篇文章最初发表于 2019-08-18，现从旧站迁入。

<!-- truncate -->

> 归档说明：正文示例中的数据库密码已替换为占位值。

残疾人就业工作的重要性人人皆知，特别是对残疾人工作者来说，更加明显，是残疾人工作的重中之重。解决残疾人生活的根本出路就是实现劳动就业，只有解决就业问题，残疾人的基本生活才能得到保障，才能在整个社会大家庭中，实现平等、参与、共享。因此，为进一步做好残疾人就业服务工作，需要对当前残疾人就业状况进行统计分析，对残疾人就业工作进行探索和思考。

为此，我们以中国残联就创业官方网站（[https://www.cdpee.org.cn/](https://www.cdpee.org.cn/)）为数据源进行爬虫与数据分析。

首先，我们导入相关的python包： 每个第三方包的作用将在后面详细叙述。

```text
import requests
import matplotlib.pyplot as plt
#import jieba
#import faker
from urllib.parse import urlencode
from retrying import retry
import pymysql
from bs4 import BeautifulSoup
import logging
import pickle
#import os  #os.path 写目录可以固定 增强健壮性
import time
import threading
from collections import defaultdict,OrderedDict
import re
```

.py文件的整体设想基于面向对象的编程思想，建立两个类：webSpider和dataAnalysis，其中，webSpider类用于数据的抓取和清洗格式，主要使用BeautifulSoup进行数据清洗，使用requests模块进行数据的采集；dataAnalysis接受webSpider的属性，即清洗好的数据进行分析和绘图，其中绘图采用python强大的绘图包matplotlib。

首先我们先查看要爬取的网站结构https://www.cdpee.org.cn/jobRecruitment.htm

[![](/img/wordpress-archive/2019/08/unnamed-file-2.png)](/img/wordpress-archive/2019/08/unnamed-file-2.png)

我们需要的内容是职位名称公司名称等关键词，每页会呈现6个job，从底部得知一共有913页。手动点击翻页，我们发现网址并没有改变，所以我们不能简单地通过改变get请求中的网址来翻页。

[![](/img/wordpress-archive/2019/08/unnamed-file-3.png)](/img/wordpress-archive/2019/08/unnamed-file-3.png)

打开Fiddler抓包工具分析具体网络情况：

即136号请求：

![](/img/wordpress-archive/2019/08/image-49.png)

查看详细信息发现浏览器对该网址发送了POST请求，其中form表单的参数如下：

其实其中只有currentPage参数有用，我们便可以构造字典作为参数提交给服务器，实现自动翻页，得到每页的html源代码。

[![](/img/wordpress-archive/2019/08/unnamed-file-4.png)](/img/wordpress-archive/2019/08/unnamed-file-4.png)

新建webSpider类:

```text
class webSpider:

	def __init__(self,START_URL,headers):
		self.START_URL = START_URL
		# self.cookies = cookies
		self.headers = headers
		self.html_list = []
		self.all_info_parsed = []
		# Added
		self.provinceCountList = []
```

其中，START\_URL为传入的初始地址，html\_list用来保存响应的html源代码，all\_info\_parsed是一个存放清洗好的字典数据的列表，proviceCountList保存每个职位的地址，最后用于统计地域分布。

Headers是从浏览器中的得到的请求头，模拟真实访问。

下面构造获取页面html的函数crawl\_pages：

```text
def crawl_pages(self):

		'''发起爬虫请求并将所得到的HTML页面保存到列表中返回'''

		pages_raw = input("请输入爬取的页面数：(10-20)")
		pages_start = int(pages_raw.split('-')[0])
		pages_end = int(pages_raw.split('-')[1])

		for page in range(pages_start,pages_end+1):
			params={'currentPage':'{}'.format(page),'keytype':'1'}

			logger.info("爬取第 {} 页".format(page))
			try:
				response = requests.post(START_URL,data=params,timeout=20)
				logger.info("第 {} 页爬取成功".format(page))
				self.html_list.append(response.text)
			except Exception as e:
				#print(e)
				logger.warning("第 {} 页爬取失败".format(page))



		return self.html_list
```

首先从外部输入指定格式的页面范围，获取到开始和结束的位置，要注意的是input默认输入的是字符串型数据，需要用int转化一下，或者eval函数也可以。

然后是主循环，从开始页码到结束页码，构造params表单字典，用requests.post()函数获取响应，并添加到html\_list字典中。

获取到html数据之后，我们对每一个页面进行解析

```text
	def parse_pages(self):    #这里有多个键值对，最好用数据库来存取，留作重构
		for html in self.html_list: #每个HTML里有6个item
			soup = BeautifulSoup(html,'lxml')
			soup = soup.find_all('div',class_='text-center f16') #此时soup为一个tag类型的列表

			 #对每一个招聘信息用一个字典来存储

			for s in soup:
				info_dict_of_each_item = {}
				try:
					info_dict_of_each_item['jobName'] = s.find(class_='col-lg-2 text-success').text.replace('n','').replace('r','') # n营建人员rn 需要移除
					info_dict_of_each_item['company'] = s.find(class_='col-lg-5').text.replace('n','').replace('r','')
					info_dict_of_each_item['detailHref'] = s.find(class_='col-lg-2 text-success').a['href']
					info_dict_of_each_item['addDate'] = s.find_all(class_='col-lg-2')[1].text.replace('n','').replace('r','')
					info_dict_of_each_item['salary'] = s.find(class_='col-lg-3').text.replace('n','').replace('r','')
					self.all_info_parsed.append(info_dict_of_each_item)
				except Exception:
					pass


		return self.all_info_parsed
```

两层循环，第一层控制页面，第二层控制解析每个页面下的6条具体数据。

对每一个html文档新建BeautiSoup对象，查看网页源代码得到所需数据的具体节点信息（此例中每一条job是'div',class\_='text-center f16'）。然后解析tag列表中的信息并添加到字典。并将每条信息对影解析完成的字典添加到all\_info\_parsed列表。

因为爬虫过程中可能出现各种各样的问题导致程序终止，如果重新运行那么以前访问过的页面还需要重新爬取，这样会造成对方服务器压力并且浪费时间，所以我们最好每次爬取完一次都将数据保存起来。

保存数据这里提供两种方法，即以文件形式保存到本地，和保存到数据库中。

首先看保存到本地文件的函数：

```text
def saveParsedDataToMysql(self):
    db = pymysql.connect('127.0.0.1','root','REPLACE_WITH_DB_PASSWORD','webspider0724')
    '''sql_1 = CREATE TABLE 'webspider0724'.'job_crawler' (
            'Id' int(11) NOT NULL AUTO_INCREMENT,
            'jobName' varchar(255) NULL DEFAULT NULL,
            'company' varchar(255) NULL DEFAULT NULL,
            'detailHref' varchar(255) NULL DEFAULT NULL,
            'addDate' varchar(255) NULL DEFAULT NULL,
            'salary' varchar(255) NULL DEFAULT NULL,
            PRIMARY KEY ('Id')
            ) DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
            SHOW CREATE TABLE 'webspider0724'.'job_crawler';'''
    cursor = db.cursor()
    #cursor.execute(sql_1)
    #db.commit()

    for dict_ in self.all_info_parsed:
        try:
            jobName = dict_['jobName']
            company = dict_['company']
            detailHref = dict_['detailHref']
            addDate = dict_['addDate']
            salary = dict_['salary']

            sql="INSERT INTO job_crawler(jobName,company,detailHref,addDate,salary)VALUES(%s,%s,%s,%s,%s);" # python的sql语句转为符是：%s 。
            cursor.execute(sql,[jobName,company,detailHref,addDate,salary])
            db.commit()
        except Exception as e:
            print(e)

    cursor.close()
    db.close()
```

打开一个文件对象，用pickle模块提供的dump函数可以将变量保存到本地文件。

```text
def loadParsedDataFromFile(self):  #从文件中加载信息到all_info_parsed中

    fileName = 'all_info_parsed.dat'
    f = open(fileName,'rb')

    self.all_info_parsed = pickle.load(f)
```

在上一个爬取函数中，我们只是简单得到了一些梗概信息，并没有得到每一个职位的详细工作内容工作地点，该部分内容保存在detailHref网址指向的页面中，所以我们还需要对该部分进行爬取。代码如下：

```text
def crawl_detailed_pages_and_save_to_mysql(self):
    pages_raw = input("请输入爬取的项目编号：如(10-20),本地数据库id是从19开始的")
    pages_start = int(pages_raw.split('-')[0])
    pages_end = int(pages_raw.split('-')[1])

    db = pymysql.connect('127.0.0.1','root','REPLACE_WITH_DB_PASSWORD','webspider0724')
    cursor = db.cursor()

    for page in range(pages_start,pages_end+1):
        try:
            href = self.all_info_parsed[page]['detailHref']  #取出网址
            logger.info("爬取第 {} 项".format(page))

            html = requests.get(href,timeout=20).text
            logger.info("第 {} 项爬取成功".format(page))
            #time.sleep(0.5)
            #print(html)
            #html = html.replace('n','').replace('r','')
            html = pymysql.escape_string(html)
            #html = html.encode('utf8')

            sql = '''UPDATE job_crawler SET detailHtml='%s' WHERE detailHref='%s';''' % (html,href)
            if cursor.execute(sql)==1:
                print('Page {} Save Successfully! '.format(page))

            #db.commit()
        except Exception as e:
            logger.warning(e)
    cursor.close()
    db.close()

    ###啊啊啊啊 保存到SQL的函数又得重写 完事之后将整个代码重写吧还是  结构太烂了
```

重点是从数据库中的detailHref获取网址，并将html文档存入数据库。此处遇到过很大的问题，即将html文档插入text类型的mysql字段中时，总是提示语句错误，尝试了很多办法最终解决，见后文。

webSpider模块至此结束。

下面是数据分析模块dataAnalysis：

```text
class dataAnalysis:
'''分析数据'''

def __init__(self,data):
    self.counter = 0
    self.data = data
    self.salary = [ self.get_list_mean( _['salary'].replace('/月','').split('-')) for _ in data]
```

初始化函数设置一个counter变量用于计数，初始化传入data，即webSpider对象的all\_info\_parsed列表属性。Salary字段在字典中取出的是字符串‘4000-4999/月’这样的格式，所以在列表生成式中要进行一定的处理。其中用到的get\_list\_mean函数如下：

```text
def get_list_mean(self,l):
    try:
        #print((int(l[0])+int(l[1]))/2)
        if '10000' in l[0]:  #数据中有个别‘10000以上’数据无法split方法处理，只能单独搞定
            return 10000;
        return (int(l[0])+int(l[1]))/2
    except Exception as e:

        print(e)
        #self.counter+=1;
        #print(self.counter)
        return 0
```

画图操作比较简单：

```text
def salaryChart(self):

    faceTalk = 0
    s1k_2k = 0
    s2k_3k = 0
    s3k_4k = 0
    s4k_5k = 0
    s5k_6k = 0
    s6k_7k = 0
    s7k_plus = 0

    for salary_ in self.salary:

        if salary_ == 0:
            faceTalk+=1
        elif salary_//1000 == 1:
            s1k_2k+=1
        elif salary_//1000 == 2:
            s2k_3k+=1
        elif salary_//1000 == 3:
            s3k_4k+=1
        elif salary_//1000 ==4:
            s4k_5k+=1
        elif salary_//1000 == 5:
            s5k_6k+=1
        elif salary_//1000 == 6:
            s6k_7k+=1
        else:
            s7k_plus+=1
    label = ['1000-1999','2000-2999','3000-3999','4000-4999','5000-5999','6000-6999','7000+','bargain in reality']
    color = ['red', 'orange', 'yellow', 'green', 'blue', 'gray', 'goldenrod','purple']
    size = [s1k_2k,s2k_3k,s3k_4k,s4k_5k,s5k_6k,s6k_7k,s7k_plus,faceTalk]
    print(size)

    pie = plt.pie(size,colors=color,labels=label)
    plt.axis('equal')
    plt.title('The salary of disabled people on a recruitment website')
    plt.show()
```

进行简单统计之后，调用matplotlib的API画出饼图即可。此处有一个小问题，matplotlib无法显示中文，也许是字体配置有问题。后面解决。

下面统计招聘地址分布前十位

```text
def provinceChart(self,l):
    'l 是地址出现每一次构成的列表'
    #provinceDict保存的是每一个省份出现的次数
    #provinceNameList就是一个名单
    #paintData保存画图需要的数据

    provinceNameList = ['北京','天津','河北','河南','陕西',
                    '新疆','山西','四川','重庆','湖北',
                    '江苏','浙江','上海','江西','福建',
                    '广东','广西','云南','贵州','安徽',
                    '西藏','甘肃','宁夏','内蒙','山东'
                    '湖南','青海','辽宁','吉林','海南',
                    '黑龙','西藏']

    provinceDict = defaultdict(int)
    #paintData = OrderedDict()

    #paintData = []
    for i in l:
        if i != '':
            provinceDict[i]+=1;

    paintData = sorted(provinceDict.items(),key=lambda x:x[1],reverse=True)

    print(provinceDict.items())

    x_data = [dic[0] for dic in paintData[0:30]]
    y_data = [dic[1] for dic in paintData[0:30]]

    plt.bar(x_data,y_data)
    plt.show()
```

这里数据分析太慢了，日后可以考虑重构，多线程分析数据。

字体问题只需要开头加入如下几行:

```text
import matplotlib
matplotlib .rcParams['font.sans-serif'] = ['KaiTi']
matplotlib .rcParams['font.serif'] = ['KaiTi']
```

将matplotlib的默认字体设置为楷体。

[![](/img/wordpress-archive/2019/08/unnamed-file-5.png)](/img/wordpress-archive/2019/08/unnamed-file-5.png)

出了一点点问题，可以看到总统计图中X轴有一栏没有文字，输出Dict\_item发现此项的key值为空，解决办法是在记数时排除这些数据，增加条件语句即可 。

[![](/img/wordpress-archive/2019/08/unnamed-file-6.png)](/img/wordpress-archive/2019/08/unnamed-file-6.png)

[![](/img/wordpress-archive/2019/08/unnamed-file-7.png)](/img/wordpress-archive/2019/08/unnamed-file-7.png)

问题解决。

[![](/img/wordpress-archive/2019/08/unnamed-file-8.png)](/img/wordpress-archive/2019/08/unnamed-file-8.png)

可以看出直辖市中相比北京，天津和上海对待残疾人更加友好。

[![](/img/wordpress-archive/2019/08/unnamed-file-9.png)](/img/wordpress-archive/2019/08/unnamed-file-9.png)

薪资水平分布如上图所示。

词云分析如下：

[![](/img/wordpress-archive/2019/08/unnamed-file.jpg)](/img/wordpress-archive/2019/08/unnamed-file.jpg)

最初的代码如下：

[点击下载](/img/wordpress-archive/downloads/spider0.01.py)

后来觉得实在太烂，就重写了一下，更加符合面向对象的要求，加入了词云。

```text
import requests
import matplotlib.pyplot as plt
from urllib.parse import urlencode
from retrying import retry
import pymysql
from bs4 import BeautifulSoup
import logging
import time
import threading
from collections import defaultdict,OrderedDict
import re
import jieba
import cv2
from wordcloud import WordCloud,STOPWORDS
from io import BytesIO

import matplotlib
matplotlib .rcParams['font.sans-serif'] = ['KaiTi']
matplotlib .rcParams['font.serif'] = ['KaiTi']

__doc__ = '本程序针对特定页面爬虫'

LOG_LEVEL = logging.INFO    # 日志等级

def get_logger():
    """
    创建日志实例
    """
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    logger = logging.getLogger("monitor")
    logger.setLevel(LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = get_logger()

all_info_parsed = []
provinceCountList = []
URL = 'https://www.cdpee.org.cn/jobRecruitment.htm'

class webSpider:

	'''只用来爬取信息并返回'''

	#因为爬虫只针对这个页面，所以保存到全局变量就行了


	def __init__(self):
		self.first_floor_html_list = []

	def crawl_first_floor_pages(self,pages_start=0,pages_end=0):

		'''用户输入范围，发起爬虫请求并将所得到的HTML页面保存到列表中

		pages_raw = input("请输入爬取的页面范围，例如10-20：")
		pages_start = int(pages_raw.split('-')[0])
		pages_end = int(pages_raw.split('-')[1])
		'''

		for page in range(pages_start,pages_end+1):
			params={'currentPage':'{}'.format(page),'keytype':'1'}
			logger.info("正在爬取第 {} 页".format(page))
			try:
				response = requests.post(URL,data=params,timeout=20)
				logger.info("第 {} 页爬取成功".format(page))
				self.first_floor_html_list.append(response.text)
			except Exception as e:
				print(e)
				logger.warning("第 {} 页爬取失败".format(page))

class dataCleanser:
	'''
		对爬虫获取的HTML数据做最基本的摘要清洗
		对每一项职位进行摘取数据保存成字典
		再将所有字典保存到all_info_parsed字典中
	'''
	def __init__(self):
		'''
		print("Parsing first floor pages for items")
		self._parse_first_floor_pages()
		print("jonName/company/detailHref/addDate/salary have been added to dict.")

		print("Parsing second floor pages for item 'description'")
		self._parse_second_floor_pages()
		print("description has been added to dict")

		print("Parsing for province and city")
		self._parse_for_province_and_city()
		print("province and city have been added to the dict")'''
		pass

	def parse_first_floor_pages(self,first_floor_html_list):

		for html in first_floor_html_list: #每个HTML里有6个item
			soup = BeautifulSoup(html,'lxml')
			soup = soup.find_all('div',class_='text-center f16') #此时soup为一个tag类型的列表

			 #对每一个招聘信息用一个字典来存储
			for s in soup:
				info_dict_of_each_item = {}
				try:
					info_dict_of_each_item['jobName'] = s.find(class_='col-lg-2 text-success').text.replace('n','').replace('r','') # n营建人员rn 需要移除
					info_dict_of_each_item['company'] = s.find(class_='col-lg-5').text.replace('n','').replace('r','')
					info_dict_of_each_item['detailHref'] = s.find(class_='col-lg-2 text-success').a['href']
					info_dict_of_each_item['addDate'] = s.find_all(class_='col-lg-2')[1].text.replace('n','').replace('r','')
					info_dict_of_each_item['salary'] = s.find(class_='col-lg-3').text.replace('n','').replace('r','')

					all_info_parsed.append(info_dict_of_each_item)

				except Exception as e:
					logger.warning(e)

	def parse_second_floor_pages(self,start,end):

		'''调用完parse_first_floor_pages才能调用此函数,需要输入爬取的页面'''

		for dict_ in all_info_parsed[start:end]:
				url = dict_['detailHref']
				try:
					html_text = requests.get(url).text
					dict_['rawHtml'] = html_text
					soup = BeautifulSoup(html_text,'lxml')
					dict_['education'] = soup.find(class_='glyphicon glyphicon-education').parent.text.replace('n','').replace('r','')#.replace('学历','').replace('：','')
					#描述分散在多个p标签内，如下处理
					description = ''
					p_text_gen = soup.find('p',id = 'description').next_siblings
					for p in p_text_gen:
						if p.string is not None:
							description = description + p.string
					dict_['description'] = description

					provinceData = soup.small.text.replace(' ','').replace('r','').replace('n','')[0:2]  # 直接在这里处理了吧，不单独写一个函数了
					dict_['province'] = provinceData

				except Exception as e:
					print(e)
					dict_['education'] = ''
					dict_['description'] = ''

class mysqlOperator:

	'''只用来操作数据库'''

	def __init__(self,host='127.0.0.1',user='root',password='REPLACE_WITH_DB_PASSWORD',database='weispider0821'):
		self.db = pymysql.connect(host,user,password,database)
		print('Connect to database %s successfully!' % database)
		self.cursor = self.db.cursor()

	def saveToMysql(self):
		'''使用之前先手动建立好数据库和数据表'''
		page = 0
		for dict_ in all_info_parsed:
			try:
				jobName = dict_['jobName']
				company = dict_['company']
				detailHref = dict_['detailHref']
				addDate = dict_['addDate']
				salary = dict_['salary']
				province = dict_['province']
				education = dict_['education']
				description = dict_['description']

				rawHtml = pymysql.escape_string(dict_['rawHtml'])

				sql="INSERT INTO job_crawler(jobName,company,detailHref,addDate,salary,province,education,description,rawHtml)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);" # python的sql语句转为符是：%s 。
				state = self.cursor.execute(sql,[jobName,company,detailHref,addDate,salary,province,education,description,rawHtml])

				page += 1
				if state == 1:
					print('保存第{}页成功！'.format(page))
				else:
					print('保存第{}页失败！'.format(page))
				self.db.commit()

			except Exception as e:
				print(e)

		self.cursor.close()
		self.db.close()

	def loadFromMysql(self):
		sql = '''SELECT * FROM `weispider0821`.`job_crawler`;'''
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		for each in result:
			fetched_dict = {}

			fetched_dict['jobName'] = each[0]
			fetched_dict['company'] = each[1]
			fetched_dict['detailHref'] = each[2]
			fetched_dict['addDate'] = each[3]
			fetched_dict['salary'] = each[4]
			fetched_dict['province'] = each[5]
			fetched_dict['education'] = each[6]
			fetched_dict['description'] = each[7]

			try:
				proviceData = BeautifulSoup(each[6],'lxml').small.text.replace(' ','').replace('r','').replace('n','')[0:2]  # 直接在这里处理了吧，不单独写一个函数了
				self.provinceCountList.append(proviceData)
			except Exception:
				pass
			all_info_parsed.append(fetched_dict)

class dataAnalyst:
	'''更高级的清洗，为画图等提供最直接的数据'''
	def __init__(self):
		pass

	@staticmethod
	def _get_mean(l):
		try:
			if '10000' in l[0]:  #数据中有个别‘10000以上’数据无法split方法处理，只能单独搞定
				return 10000;
			return (int(l[0])+int(l[1]))/2
		except Exception as e:
			print(e) # 面议提示太多
			return 0

	def fillProviceCountList(self):

		try :
			for dict_ in all_info_parsed:
				provinceCountList.append(dict_['province'])
		except Exception:
			pass

class picDrawer:
	'''只用来画图'''

	def __init__(self):
		self.salary = [ dataAnalyst._get_mean( _['salary'].replace('/月','').split('-')) for _ in all_info_parsed]

	def drawSalaryAmountDistribution(self):

		faceTalk = 0
		s1k_2k = 0
		s2k_3k = 0
		s3k_4k = 0
		s4k_5k = 0
		s5k_6k = 0
		s6k_7k = 0
		s7k_plus = 0

		for salary_ in self.salary:

			if salary_ == 0:
				faceTalk+=1
			elif salary_//1000 == 1:
				s1k_2k+=1
			elif salary_//1000 == 2:
				s2k_3k+=1
			elif salary_//1000 == 3:
				s3k_4k+=1
			elif salary_//1000 ==4:
				s4k_5k+=1
			elif salary_//1000 == 5:
				s5k_6k+=1
			elif salary_//1000 == 6:
				s6k_7k+=1
			else:
				s7k_plus+=1

		label = ['1000-1999','2000-2999','3000-3999','4000-4999','5000-5999','6000-6999','7000+','bargain in reality']
		color = ['red', 'orange', 'yellow', 'green', 'blue', 'gray', 'goldenrod','purple']
		size = [s1k_2k,s2k_3k,s3k_4k,s4k_5k,s5k_6k,s6k_7k,s7k_plus,faceTalk]
		print(size)

		pie = plt.pie(size,colors=color,labels=label)
		plt.axis('equal')
		plt.title('The salary of disabled people on a recruitment website')
		plt.show()

	def drawProviceSalaryBar(self,l=provinceCountList):
		"""
		l 是地址出现每一次构成的列表
		provinceDict保存的是每一个省份出现的次数
		provinceNameList就是一个名单
		paintData保存画图需要的数据
		"""

		provinceNameList = ['北京','天津','河北','河南','陕西',
						'新疆','山西','四川','重庆','湖北',
						'江苏','浙江','上海','江西','福建',
						'广东','广西','云南','贵州','安徽',
						'西藏','甘肃','宁夏','内蒙','山东'
						'湖南','青海','辽宁','吉林','海南',
						'黑龙','西藏']

		provinceDict = defaultdict(int)

		for i in l:
			if i != '':
				provinceDict[i]+=1;

		paintData = sorted(provinceDict.items(),key=lambda x:x[1],reverse=True)

		x_data = [dic[0] for dic in paintData[0:30]]
		y_data = [dic[1] for dic in paintData[0:30]]

		plt.bar(x_data,y_data)
		plt.show()

	def drawWordCloud(self):

		"生成中文词云"
		tempStr = ''
		for dict_ in all_info_parsed:
			tempStr = tempStr + dict_['description']
		cut_text =" ".join(jieba.cut(tempStr))
		print(0)
		color_mask = cv2.imread('mask.jpg')

		block_list = ['工作','时间','每天','我们','需要','公司','任职','资格']
		sw = set(block_list)

		cloud = WordCloud(
							#设置字体，不指定就会出现乱码
							font_path=" C:\Windows\Fonts\STXINGKA.TTF",
							#font_path=path.join(d,'simsun.ttc'),
							#设置背景色
							background_color='white',
							#词云形状
							mask=color_mask,
							#允许最大词汇
							max_words=2000,
							#最大号字体
							max_font_size=150,
							scale=4,
							stopwords=sw

							)
		print(1)
		wCloud = cloud.generate(cut_text)
		print(2)
		wCloud.to_file('cloud.jpg')

def main():

	spider = webSpider()
	operator = mysqlOperator()
	operator.loadFromMysql()
	drawer = picDrawer()
	drawer.drawWordCloud()
'''
	t1 = threading.Thread(target=spider.crawl_first_floor_pages,args=(1,20))
	t2 = threading.Thread(target=spider.crawl_first_floor_pages,args=(21,40))
	t3 = threading.Thread(target=spider.crawl_first_floor_pages,args=(41,60))
	t4 = threading.Thread(target=spider.crawl_first_floor_pages,args=(61,80))
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t1.join()
	t2.join()
	t3.join()
	t4.join()

	cleanser = dataCleanser()
	cleanser.parse_first_floor_pages(spider.first_floor_html_list)
	cleanser.parse_second_floor_pages(0,len(all_info_parsed))

	analyst = dataAnalyst()
	analyst.fillProviceCountList()

	operator = mysqlOperator()
	operator.saveToMysql()

	drawer = picDrawer()
	drawer.drawSalaryAmountDistribution()
	drawer.drawProviceSalaryBar()
	drawer.drawWordCloud()
'''

if __name__ == '__main__':
	main()
```

下面记录一些DEBUG过程：

![](/img/wordpress-archive/2019/09/image-6.png)

*input默认输出的是字符串格式，所以要加个int才能和1运算*

![](/img/wordpress-archive/2019/09/image-7.png)

*不能以数字开头命名变量，非法*

一个大问题：将整段html文档保存到数据库中时，提示插入语法错误，因为html字符串中含有大量单双引号，与sql语法冲突。

![](/img/wordpress-archive/2019/09/image-9.png)

尝试更换定界符为其他字符比如$$$，无法解决。

尝试着把html原文件中的引号替换为双引号或者r’%%%’还是不行

我不知道怎么办了，干脆把html字符串encode成byte对象以二进制形式保存？Mysql设置为blob存取二进制对象，妈耶，查了一下发现 二进制存取更复杂。算了想别的办法。

去除新定义的定界符$$$，使用pymysql提供的转义方法 html = pymysql.escape\_string(html) ，问题解决。

![](/img/wordpress-archive/2019/09/image-10.png)
