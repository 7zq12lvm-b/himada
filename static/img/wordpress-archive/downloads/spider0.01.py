#coding:utf-8
import requests
import matplotlib.pyplot as plt
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

import matplotlib
matplotlib .rcParams['font.sans-serif'] = ['KaiTi']
matplotlib .rcParams['font.serif'] = ['KaiTi']



START_URL = 'https://www.cdpee.org.cn/jobRecruitment.htm'
headers = {b'Host': b'www.cdpee.org.cn',
 b'Connection': b'keep-alive',
 b'Content-Length': b'204',
 b'Cache-Control': b'max-age=0',
 b'Upgrade-Insecure-Requests': b'1',
 b'User-Agent': b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
 b'Origin': b'https://www.cdpee.org.cn',
 b'Content-Type': b'application/x-www-form-urlencoded',
 b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
 b'Referer': b'https://www.cdpee.org.cn/jobRecruitment.htm',
 b'Accept-Encoding': b'gzip, deflate, br',
 b'Accept-Language': b'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
 b'Cookie': b'UM_distinctid=16c211066b22cd-0dad63023af44f-e323069-144000-16c211066b33fd; _ga=GA1.3.1886916474.1563922819; _gid=GA1.3.1519279805.1563922819; __51cke__=; CNZZDATA1273996978=364796639-1563922818-null%7C1564007261; SHAREJSESSIONID=a3535d46-f6d0-426f-a40d-d2747e2ec88b; Hm_lvt_ee31947220a83dbba5919eb6c496b632=1563922819,1564009462; CNZZDATA1271161620=567415642-1563922818-null%7C1564008808; __tins__19537549=%7B%22sid%22%3A%201564009461795%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201564011425952%7D; __51laig__=5; Hm_lpvt_ee31947220a83dbba5919eb6c496b632=1564009626'}
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


class webSpider:


	def __init__(self,START_URL,headers):
		self.START_URL = START_URL
		self.headers = headers
		self.html_list = []
		self.all_info_parsed = []
		# Added
		self.provinceCountList = []

	@retry(3) #重试三次 装饰器
	def crawl_each_page(self,START_URL,params):
		response = requests.post(START_URL,data=params,timeout=20)
		return response

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

	def parse_pages(self):    #这里有多个键值对，最好用数据库来存取，留作重构
		for html in self.html_list: #每个HTML里有6个item
			soup = BeautifulSoup(html,'lxml')
			soup = soup.find_all('div',class_='text-center f16') #此时soup为一个tag类型的列表

			 #对每一个招聘信息用一个字典来存储

			for s in soup:
				info_dict_of_each_item = {}
				try:
					info_dict_of_each_item['jobName'] = s.find(class_='col-lg-2 text-success').text.replace('\n','').replace('\r','') # \n营建人员\r\n 需要移除
					info_dict_of_each_item['company'] = s.find(class_='col-lg-5').text.replace('\n','').replace('\r','')
					info_dict_of_each_item['detailHref'] = s.find(class_='col-lg-2 text-success').a['href']
					info_dict_of_each_item['addDate'] = s.find_all(class_='col-lg-2')[1].text.replace('\n','').replace('\r','')
					info_dict_of_each_item['salary'] = s.find(class_='col-lg-3').text.replace('\n','').replace('\r','')
					self.all_info_parsed.append(info_dict_of_each_item)
				except Exception:
					pass


		return self.all_info_parsed

	#这两个函数运行后，数据都保存在html_list 和 all_info_parsed 中了
	#算了 添加到数据库的操作在main函数里完成吧

	def crawl_and_parse_detailed_info_of_each_item(self,start,end):
		'''start-end代表爬取第几项到第几项的详细信息'''

		detailed_info_of_each_item_dict = {}
		detailed_info_of_each_item_list = []

		for dict_ in self.all_info_parsed[start:end]:
			url = dict_['detailHref']
			try:
				html_text = requests.get(url)
				soup = BeautifulSoup(html_text)
				detailed_info_of_each_item_dict['education'] = soup.find(class_='glyphicon glyphicon-education').parent.text.replace('\n','').replace('\r','')#.replace('学历','').replace('：','')
				detailed_info_of_each_item_dict['description'] = soup.find('p',id = 'description').nextSibling.text
			except Exception:
				pass
			detailed_info_of_each_item_list.append(detailed_info_of_each_item_dict)

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

	def saveParsedDataToFile(self):  #把此次爬取的数据保存到文件中以供后续分析
		fileName = 'all_info_parsed.dat'

		f = open(fileName,'wb')
		pickle.dump(self.all_info_parsed,f)
		f.close()

	def loadParsedDataFromFile(self):  #从文件中加载信息到all_info_parsed中

		fileName = 'all_info_parsed.dat'
		f = open(fileName,'rb')

		self.all_info_parsed = pickle.load(f)

	def loadParsedDataFromMYSQL(self):
		db = pymysql.connect('127.0.0.1','root','REPLACE_WITH_DB_PASSWORD','webspider0724')
		cursor = db.cursor()
		sql = '''SELECT * FROM `webspider0724`.`job_crawler`;'''
		cursor.execute(sql)
		result = cursor.fetchall()


		for each in result:
			fetched_dict = {}

			fetched_dict['jobName'] = each[1]
			fetched_dict['company'] = each[2]
			fetched_dict['detailHref'] = each[3]
			fetched_dict['addDate'] = each[4]
			fetched_dict['salary'] = each[5]

			try:
				proviceData = BeautifulSoup(each[6],'lxml').small.text.replace(' ','').replace('\r','').replace('\n','')[0:2]  # 直接在这里处理了吧，不单独写一个函数了
				self.provinceCountList.append(proviceData)
			except Exception:
				pass
			self.all_info_parsed.append(fetched_dict)




		cursor.close()
		db.close()

	#以上所有函数都是在概括页面进行爬取,由于昨天忘记把HTML数据保存到数据库，现在无法对地域分布等数据进行分析，所以我决定利用保存了的详情页面地址重新爬取

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
				#html = html.replace('\n','').replace('\r','')
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


	#def parse_detailed_pages(self):









class dataAnalysis:

	'''分析数据'''

	def __init__(self,data):
		self.counter = 0
		self.data = data
		self.salary = [ self.get_list_mean( _['salary'].replace('/月','').split('-')) for _ in data]
		#self.location =

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
			print('start')
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









if __name__ == "__main__":
	spider = webSpider(START_URL,headers)
	#spider.crawl_pages()
	#spider.parse_pages()
	#spider.saveParsedDataToFile()
	#spider.loadParsedDataFromFile()
	#print(spider.all_info_parsed)
	#spider.saveParsedDataToMysql()
	spider.loadParsedDataFromMYSQL()


	brush = dataAnalysis(spider.all_info_parsed)
	#brush.salaryChart()
	#spider.crawl_detailed_pages_and_save_to_mysql()


	#spider2 = webSpider(START_URL,headers)
	#spider2.loadParsedDataFromMYSQL()
	#spider2.crawl_detailed_pages_and_save_to_mysql()



	#多线程,速度快了一倍
	#t1 = threading.Thread(target=spider.crawl_detailed_pages_and_save_to_mysql)
	#t2 = threading.Thread(target=spider2.crawl_detailed_pages_and_save_to_mysql)

	#t1.start()
	#t2.start()

	#省份分布
	brush.provinceChart(spider.provinceCountList)
	brush.salaryChart()
