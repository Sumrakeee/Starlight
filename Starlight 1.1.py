import asyncio
import pyppeteer
import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Inches
import time
import os
import starcleaner

gpath = 'C:\\Users\\Sumrak\\OneDrive\\Проекты Python\\Работа\\Starlight\\Ads\\'
glid = ''
browser_con = False

def get_total_pages(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]

	return int(total_pages)

def parse_id(url):
	global glid
	glid = url.split('_')[-1]

async def init_browser():
	global browser
	global page
	global browser_con

	try:
		browser = await pyppeteer.launch()
		page = await browser.newPage()
		browser_con = True
	except:
		print('browser init error')

async def init_page_scr(url):
	global browser
	global page
	global browser_con

	try:
		await page.goto(url)
		print('page goto OK')
	except:
		print('page goto error')
	try:	
		await page.click('div.item-map-control')
		print('page click map OK')
		await page.setViewport(dict(width=1920, height=1080))
		print('page set viewport OK')
		await page.screenshot(path='img.jpg', fullPage=True)
		print('page screenshot OK')
	except:
		print('screenshot error')

def browser_logic(url):
	global browser_con
	global browser
	global page

	if browser_con == False:
		asyncio.get_event_loop().run_until_complete(init_browser())
		asyncio.get_event_loop().run_until_complete(init_page_scr(url))
	else:
		asyncio.get_event_loop().run_until_complete(init_page_scr(url))

def create_document():
	global glid
	global gpath
	filename = glid
	path = gpath

	doc = Document()
	doc.add_picture('img.jpg', width=Inches(6.5))
	doc.save(path+glid+'.docx')

def get_ads(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='js-catalog-list').find_all('div', class_='item_list')

	for ad in ads:
		url = 'https://www.avito.ru'+ad.find('div', class_='description-title').find('h3').find('a').get('href')
		print(url)
		parse_id(url)
		browser_logic(url)
		create_document()

def main():
	print('Starlight v1.1.01112018',
		'\nРазработчики: Чернышев Егор Владимирович \n\t      Чернышева Татьяна Анатольевна',
		'\n\nФункционал ограничен',
		'\n===========================================')

	p_url = input('\nВВЕДИТЕ ССЫЛКУ: ')
	startup_page = int(input('\nВВЕДИТЕ НОМЕР СТРАНИЦЫ, С КОТОРОЙ ХОТИТЕ НАЧАТЬ: '))

	base_part = p_url.split('?')[0]
	query_part = '?&s=104&view=list'
	page_part = '&p='

	total_pages = get_total_pages(p_url)

	print('\nПРОГРАММА НАЧАЛА ВЫПОЛНЕНИЕ РАБОТЫ')

	for i in range(startup_page, total_pages+1):
		url_gen = base_part + query_part + page_part + str(i)
		print('\nСГЕНЕРИРОВАНА ССЫЛКА: '+url_gen+'\n')
		get_ads(url_gen)

		print('\nСТРАНИЦА ОБРАБОТАНА')
	
	starcleaner.clean_chrome()
	starcleaner.clean_py()
	print('\nПРОГРАММА ЗАВЕРШИЛА РАБОТУ')
	#time.sleep(60*60*24)

if __name__ == '__main__':
	main()