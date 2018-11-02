import time
from selenium import webdriver
from selenium.webdriver import Chrome
from docx import Document
from docx.shared import Inches
import requests
from bs4 import BeautifulSoup
import os

browser = False
uid = ''
path = 'C:\\Users\\SerovaSG\\Desktop\\Starlight\\Files\\'

def get_total_pages(url):
	try:
		html = requests.get(url).text
		soup = BeautifulSoup(html, 'lxml')
		pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
		total_pages = pages.split('=')[1].split('&')[0]
	except:
		total_pages = 1

	return int(total_pages)

def get_id(url):
	global uid
	uid = url.split('_')[-1]

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
	print('page has been opened -OK')
	try:
		driver.find_element_by_class_name('item-map-control').click()
		print('map closed -OK')
	except:
		print('unable to close map -ERROR')
		pass
	
def take_screenshot():
	global driver

	driver.save_screenshot('img.png')
	print('screenshot saved -OK')

def create_document():
	global uid
	global path
	doc = Document()
	doc.add_picture('img.png', width=Inches(4))
	doc.save(path + uid + '.docx')
	print('document saved -OK')

def browser_logic_hub(url):
	global browser

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='js-catalog-list').find_all('div', class_='item_list')

	for ad in ads:
		url = 'https://www.avito.ru' + ad.find('div', class_='description-title').find('h3').find('a').get('href')
		print(url)            
		get_id(url)

		if browser == False:
			launch_browser()
			open_page(url)
			take_screenshot()
			create_document()
			browser = True
		else:
			open_page(url)
			take_screenshot()
			create_document()

		#time.sleep(2)

def main():
	print('Starlight v1.2S.02112018',
		'\nРазработчики: Чернышев Егор Владимирович',
		'\n\t      Чернышева Татьяна Анатольевна',
		'\n\nФункционал ограничен',
		'\n===========================================')

	p_url = input('\nВВЕДИТЕ ССЫЛКУ: ')
	startup_page = int(input('\nВВЕДИТЕ НОМЕР СТРАНИЦЫ, С КОТОРОЙ ХОТИТЕ НАЧАТЬ: '))

	base_part = p_url.split('?')[0]
	query_part = '?&s=104&view=list'
	page_part = '&p='

	total_pages = get_total_pages(p_url)

	print('\nПРОГРАММА НАЧАЛА ВЫПОЛНЕНИЕ РАБОТЫ')

	for i in range(startup_page, total_pages + 1):
		url_gen = base_part + query_part + page_part + str(i)
		print('\nСГЕНЕРИРОВАНА ССЫЛКА: '+ url_gen +'\n')
		browser_logic_hub(url_gen)

		print('\nСТРАНИЦА ОБРАБОТАНА')

	print('\nПРОГРАММА ЗАВЕРШИЛА РАБОТУ')

if __name__ == '__main__':
	main()
	print('driver quit')
	driver.quit()
