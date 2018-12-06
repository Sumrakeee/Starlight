import os
import time
import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from docx import Document
from docx.shared import Inches
from bs4 import BeautifulSoup
from colorama import init as colorinit
from colorama import Fore, Back, Style

colorinit()

browser = False
uid = ''
path = 'C:\\Users\\SerovaSG\\Desktop\\Starlight\\Files\\'

def get_total_pages(url):
	try:
		html = requests.get(url).text
		soup = BeautifulSoup(html, 'lxml')
		pages = soup.find('div', class_='pagination-pages').find_all('a', 
								 class_='pagination-page')[-1].get('href')
		total_pages = pages.split('=')[1].split('&')[0]
	except:
		total_pages = 1

	return int(total_pages)

def get_id(url):
	global uid
	uid = url.split('_')[-1]

def launch_browser():
	global driver
	print(Style.BRIGHT, Fore.CYAN + '\nИнициализация браузера' + Style.RESET_ALL)
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument('headless')
	chromeOptions.add_argument('--ignore-certificate-errors')
	chromeOptions.add_argument('--test-type')
	chromeOptions.add_argument('--log-level=3')
	chromeOptions.add_argument('--window-size=1000x3000')
	driver = webdriver.Chrome(options=chromeOptions)

	print(Style.BRIGHT, Fore.YELLOW + '\nБраузер запущен\t=====>\t [ OK ]' + Style.RESET_ALL)
	return driver

def open_page(url):
	global driver

	driver.get(url)
	print(Style.BRIGHT, Fore.GREEN + 'Страница открыта\t=====>\t [ OK ]' + Style.RESET_ALL)
	try:
		driver.find_element_by_class_name('item-phone-number').click()
		time.sleep(1) # !!!

		driver.find_elements_by_class_name('close')[-1].click()
		print(Style.BRIGHT, Fore.GREEN + 'Номер телефона открыт\t=====>\t [ OK ]' + Style.RESET_ALL)

	except:
		print(Style.BRIGHT, Fore.RED + 'Невозможно открыть номер телефона\t=====>\t [ ERROR ]' + Style.RESET_ALL)

	try:
		driver.find_element_by_class_name('item-map-control').click()
		print(Style.BRIGHT, Fore.GREEN + 'Карта скрыта\t\t=====>\t [ OK ]' + Style.RESET_ALL)
	except:
		print(Style.BRIGHT, Fore.RED + 'Невозможно скрыть карту\t=====>\t [ ERROR ]' + Style.RESET_ALL)
	
def take_screenshot():
	global driver

	driver.save_screenshot('img.png')
	print(Style.BRIGHT, Fore.GREEN + 'Скриншот сохранен\t=====>\t [ OK ]' + Style.RESET_ALL)

def create_document():
	global uid
	global path
	doc = Document()
	doc.add_picture('img.png', width=Inches(4))
	doc.save(path + uid + '.docx')
	print(Style.BRIGHT, Fore.GREEN + 'Документ сохранен\t=====>\t [ OK ]' + Style.RESET_ALL)

def browser_logic_hub(url, page, adnum):
	global browser

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='js-catalog-list').find_all('div', class_='item_table')

	for ad in ads:
		url = 'https://www.avito.ru' + ad.find('div', class_='item_table-header').find('h3').find('a').get('href')

		get_id(url)

		if browser == False:
			launch_browser()
			print(Style.BRIGHT, 
				  Fore.WHITE,
				  '\n' + str(page) + ':' + str(adnum) + ' - ', Fore.MAGENTA + url, 
				  Style.RESET_ALL)
			open_page(url)
			take_screenshot()
			create_document()
			browser = True
		else:
			print(Style.BRIGHT, 
				  Fore.WHITE,
				  '\n' + str(page) + ':' + str(adnum) + ' - ', Fore.MAGENTA + url, 
				  Style.RESET_ALL)
			open_page(url)
			take_screenshot()
			create_document()

		adnum += 1
		#time.sleep(2)

def main():
	print('\n=============================================',
		'\nStarlight v1.4 (06/12/2018)',
		'\nРазработчики: Чернышев Егор Владимирович',
		'\n\t      Чернышева Татьяна Анатольевна',
		'\n\nФункционал ограничен',
		'\n=============================================')

	p_url = input('\nВВЕДИТЕ ССЫЛКУ: ')

	try:
		startup_page = int(input('\nВВЕДИТЕ НОМЕР СТРАНИЦЫ, С КОТОРОЙ ХОТИТЕ НАЧАТЬ: '))
	except:
		startup_page = 1
		print('\nНАЧАЛЬНАЯ СТРАНИЦА НЕ УКАЗАНА. ВЫБРАНА СТРАНИЦА ПО УМОЛЧАНИЮ (1)')

	base_part = p_url.split('?')[0]
	page_part = '?p='
	query_part = '&s=104'

	total_pages = get_total_pages(p_url)

	print('\nПРОГРАММА НАЧАЛА ВЫПОЛНЕНИЕ РАБОТЫ')

	for i in range(startup_page, total_pages + 1):
		url_gen = base_part + page_part + str(i) + query_part
		print('\nССЫЛКА ПРЕОБРАЗОВАНА:'+ Style.BRIGHT, Fore.YELLOW + url_gen + Style.RESET_ALL)
		browser_logic_hub(url_gen, i, 1)

		print(Style.BRIGHT, Fore.CYAN + '\nСТРАНИЦА ОБРАБОТАНА' + Style.RESET_ALL)

	print('\nПРОГРАММА ЗАВЕРШИЛА РАБОТУ')

if __name__ == '__main__':
	main()
	print('driver quit')
	driver.quit()