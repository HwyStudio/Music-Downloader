# -*- coding:utf-8 -*-
#py3

import time
import sys
import urllib.request
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
# 歌曲名
music_name=''


# 获取url
def geturl():
	input_string = input('[==]请输入关键词:')
	driver = webdriver.Chrome()
	url='http://www.kugou.com/'
	driver.get(url)
	a = driver.find_element_by_xpath('html/body/div[1]/div[1]/div[1]/div[1]/input')  # 输入搜索内容
	a.send_keys(input_string)
	driver.find_element_by_xpath('html/body/div[1]/div[1]/div[1]/div[1]/div/i').click()  # 点击搜索
	driver.implicitly_wait(2)
	return driver


# 显示搜索结果
def show_results(driver):
	music_list = []
	for i in range(1,1000):
		try:
			music_list.append('%d.' % i+driver.find_element_by_xpath(
				".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % i).get_attribute('title')
			)  # 获取歌曲名
		except NoSuchElementException:
			break

	#倒着输出 方便查看
	for i in range(len(music_list)):
		print(music_list[len(music_list) - i - 1])

	choice = input("[==]请选择一个(你可以输入'quit'(不带引号)返回):")
	if choice == 'quit':  # 从下载界面退回
		result = 'quit'
		driver.quit()
	else:
		try:
			choice_int = int(choice)
		except:
			print('请进行选择!')
			return show_results(driver)
			#递归
		
		global music_name
		music_name = driver.find_element_by_xpath(
			".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % choice_int
		).get_attribute('title')
		a = driver.find_element_by_xpath(".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % choice_int)
		actions = ActionChains(driver)
		actions.move_to_element(a)
		actions.click(a)
		actions.perform()
		# wait(driver)
		time.sleep(5)
		driver.implicitly_wait(1)
		driver.switch_to_window(driver.window_handles[1])  # 跳转到新打开的页面
		result = driver.find_element_by_xpath(".//*[@id='myAudio']").get_attribute('src')  # 获取播放元文件url
		driver.quit()
	return result


def cbk(blocknum, blocksize, totalsize):
	"""
	urllib.urlretrieve 的回调函数,即下载回调python urlretrieve 下载进度条
	:param blocknum: 已经下载的数据块
	:param blocksize: 数据块的大小
	:param totalsize: 远程文件的大小
	:return:
	"""

	percent = 100 * blocknum * blocksize / totalsize
	if percent >= 100:
		percent = 100
	
	if  0 <= percent <=100:#防止出bug刷屏
		progress = int(percent) // 2
		#print('[' + '#' * progress + '-' * (50 - progress)  + ']',end = '')
		progress_str = '[' + '#' * progress + '-' * (50 - progress)  + ']%.2f%%\r' % percent
		sys.stdout.write(progress_str)
		sys.stdout.flush()
		
		if percent == 100:
			print('[' + '#' * progress + '-' * (50 - progress)  + ']%.2f%%\r' % percent)


def main():
	print('================================欢迎使用音乐下载器================================')
	time.sleep(1)
	while True:
		driver = geturl()
		result = show_results(driver)
		if result == 'quit':
			print('\n')
			continue
		else:
			local = 'E:\\音乐\\' + music_name + '.mp3'
			print('开始下载 目前进度:')
			# time.sleep(1)
			urllib.request.urlretrieve(result, local, cbk)
			print('%s.mp3 下载完成' % music_name + '\n\n')


if __name__=='__main__':
	main()
