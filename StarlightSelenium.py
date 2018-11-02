import time
from selenium import webdriver
from selenium.webdriver import Chrome
from docx import Document
from docx.shared import Inches
import requests
from bs4 import BeautifulSoup
import os

browser = False

def launch_browser():
	global driver
	print('browser initialization')
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument("headless")
	chromeOptions.add_argument('--ignore-certificate-errors')
	chromeOptions.add_argument("--test-type")
	chromeOptions.add_argument("--window-size=1000x2500")
	driver = webdriver.Chrome(options=chromeOptions)

	print('browser launched -OK')
	return driver

def open_page(url):
	global driver

	driver.get(url)
	print(url)
	driver.find_element_by_class_name('item-map-control').click()
	print('map closed -OK')

def take_screenshot():
	global driver

	driver.save_screenshot('img.png')
	print('screenshot saved -OK')

def create_document(filename):
	doc = Document()
	doc.add_picture('img.png', width=Inches(4))
	doc.save(filename + '.docx')

def browser_logic_hub(url, filename):
	global browser
	if browser == False:
		launch_browser()
		open_page(url)
		print('page has been opened -OK')
		take_screenshot()
		create_document(filename)
		browser = True
	else:
		open_page(url)
		print('page has been opened -OK')
		take_screenshot()
		create_document(filename)

def main():
	urls = ['https://www.avito.ru/stavropol/kvartiry/2-k_kvartira_65_m_59_et._1676844596']
			#,'https://www.avito.ru/stavropol/zemelnye_uchastki/uchastok_16_sot._snt_dnp_1551738138']

	for url in urls:
		uid = url.split('_')[-1]
		browser_logic_hub(url, uid)

if __name__ == '__main__':
	main()
	print('driver quit')
	driver.quit()
