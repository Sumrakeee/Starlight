import asyncio
import pyppeteer
import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Inches
import time
import os

gpath = 'C:\\Users\\SerovaSG\\Desktop\\Starlight\\Files\\'
glid = ''

def get_total_pages(url):
	try:
		html = requests.get(url).text
		soup = BeautifulSoup(html, 'lxml')
		pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
		total_pages = pages.split('=')[1].split('&')[0]
	except:
		total_pages = 1

	return int(total_pages)

def parse_id(url):
	global glid
	glid = url.split('_')[-1]

async def init_pyppeteer(url):
	browser = await pyppeteer.launch()
	page = await browser.newPage()
	try:
		await page.goto(url)
		await page.click('div.item-map-control')
		await page.setViewport(dict(width=1920, height=1080))
		await page.screenshot(path='img.jpg', fullPage=True)
	except:
		pass
	try:
		await browser.close()
	except:
		os.system('taskkill /im chrome.exe /f')

def create_document():
	global glid
	global gpath
	filename = glid
	path = gpath

	doc = Document()
	doc.add_picture('img.jpg', width=Inches(6.5))
	doc.save(path + glid + '.docx')

def get_ads(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='js-catalog-list').find_all('div', class_='item_list')

	for ad in ads:
		url = 'https://www.avito.ru' + ad.find('div', class_='description-title').find('h3').find('a').get('href')
		print(url)            
		parse_id(url)
		try:
			asyncio.get_event_loop().run_until_complete(init_pyppeteer(url))
		except:
			continue
		create_document()

def main():
	print('Starlight v1.01.02112018',
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

#	try:
	for i in range(startup_page, total_pages + 1):
		url_gen = base_part + query_part + page_part + str(i)
		print('\nСГЕНЕРИРОВАНА ССЫЛКА: '+ url_gen +'\n')
		get_ads(url_gen)

		print('\nСТРАНИЦА ОБРАБОТАНА')
#	except:
#		url_gen = base_part + query_part + page_part + str(1)
#		print('\nСГЕНЕРИРОВАНА ССЫЛКА: '+ url_gen +'\n')
#		get_ads(url_gen)

#		print('\nСТРАНИЦА ОБРАБОТАНА')

	print('\nПРОГРАММА ЗАВЕРШИЛА РАБОТУ')
	#time.sleep(60 * 60 * 24)

if __name__ == '__main__':
	main()
