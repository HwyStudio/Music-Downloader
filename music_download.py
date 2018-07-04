# -*- coding:utf-8 -*-

import time
import urllib.request
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
# 歌曲名
music_name=''


# 获取url
def geturl():
	input_string = input('>>>please input the search key:')
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
	for i in range(1,1000):
		try:
			print('%d.' % i+driver.find_element_by_xpath(
				".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % i).get_attribute('title')
			)  # 获取歌曲名
		except NoSuchElementException:
			break
	choice = input(">>>Which one do you want(you can input 'quit' to go back(带引号)):")
	if choice == 'quit':  # 从下载界面退回
		result = 'quit'
	else:
		global music_name
		music_name = driver.find_element_by_xpath(
			".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % int(choice)
		).get_attribute('title')
		a = driver.find_element_by_xpath(".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % int(choice))
		actions = ActionChains(driver)
		actions.move_to_element(a)
		actions.click(a)
		actions.perform()
		# wait(driver)
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
	# f = sys.stdout # 设置下载进度条
	percent = 100.0 * blocknum * blocksize / totalsize
	if percent > 100:
		percent = 100
	print('%.2f%%' % percent, end=' ')


def main():
	print('***********************欢迎使用音乐下载器********************************')
	time.sleep(1)
	while True:
		driver = geturl()
		result = show_results(driver)
		if result == 'quit':
			print('\n')
			continue
		else:
			local = 'F://音乐/%s.mp3' % music_name
			print('download start')
			# time.sleep(1)
			urllib.request.urlretrieve(result, local, cbk)
			print('finish download %s.mp3' % music_name + '\n\n')


if __name__=='__main__':
	main()