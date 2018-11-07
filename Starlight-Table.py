import requests
from bs4 import BeautifulSoup
import csv
import time

def delay(sec=2):
	print('delay: '+str(sec))
	time.sleep(sec)

def write_csv(data):
	with open('avito.csv', 'a', encoding='utf8') as f:
		writer = csv.writer(f)

		writer.writerow( (data['title'],
						  data['location'],
						  data['params'],
						  data['description'],
						  data['price'],
						  data['phone'],
						  data['uid']) )

def get_total_pages(url):
	try:
		html = requests.get(url).text
		soup = BeautifulSoup(html, 'lxml')
		pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
		total_pages = pages.split('=')[1].split('&')[0]
	except:
		total_pages = 1

	return int(total_pages)

def get_page_data(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='js-catalog-list').find_all('div', class_='item_list')

	for ad in ads:
		url = 'https://www.avito.ru' + ad.find('div', class_='description-title').find('h3').find('a').get('href')
		m_url = 'https://m.avito.ru' + ad.find('div', class_='description-title').find('h3').find('a').get('href')
		print(url)

		html = requests.get(url).text
		soup = BeautifulSoup(html, 'lxml')

		m_html = requests.get(m_url).text
		m_soup = BeautifulSoup(m_html, 'lxml')

		# Title
		try:
			title = soup.find('div', class_='title-info-main').text.strip()
		except:
			title = ''
			print('ЗАГОЛОВОК ОТСУТСТВУЕТ')

		# Location
		try:
			location = soup.find('div', class_='item-map-location').text.strip().replace('\n', '').replace('  ', ' ').split('Скрыть карту')[0].split('Адрес: ')[-1]
		except:
			try:
				location = soup.find('div', class_='item-view-seller-info').text.split('Адрес')[-1].strip()
			except:
				location = ''
				print('ИНФОРМАЦИЯ О МЕСТОПОЛОЖЕНИИ ОТСУТСТВУЕТ')

		# Params
		try:
			params = soup.find('div', class_='item-params').text.strip().replace('\xa0', '').replace('\n', '')
		except:
			params = ''
			print('ДАННЫЕ О ПЛОЩАДИ ОТСУТСТВУЮТ')

		# Description
		try:
			description = soup.find('div', class_='item-description').text.strip()
		except:
			description = ''
			print('ОПИСАНИЕ ОТСУТСТВУЕТ')

		# Price
		try:
			price = soup.find('div', class_='item-price').find('span', class_='price-value-string').text.strip().replace('\xa0', '')	
		except:
			price = ''
			print('ИНФОРМАЦИЯ О ЦЕНЕ ОТСУТСТВУЕТ')

		# ID
		try:
			uid = soup.find('div', class_='title-info-metadata').text.split()[1].split(',')[0]
		except:
			uid = ''
			print('ID ОТСУТСТВУЕТ')

		# Phone
		try:
			phone = m_soup.find('div', class_='_1DzgK').find('a').get('href').split(':')[-1]
		except:
			phone = ''
			print('НОМЕР ТЕЛЕФОНА ОТСУТСТВУЕТ')

		data = {'title': title,
				'location': location,
				'description': description,
				'params': params,
				'uid': uid,
				'phone': phone,
				'price': price}

		print('ОБРАБОТАНО')

		write_csv(data)			

		delay()

def main():
	print('Starlight-Table v1.1(07112018)',
		'\nРазработчик: Чернышев Егор Владимирович',
		'\n\nФункционал ограничен',
		'\n===========================================')

	p_url = input('\nВВЕДИТЕ ССЫЛКУ: ')

	try:
		startup_page = int(input('\nВВЕДИТЕ НОМЕР СТРАНИЦЫ, С КОТОРОЙ ХОТИТЕ НАЧАТЬ: '))
	except:
		startup_page = 1
		print('\nНАЧАЛЬНАЯ СТРАНИЦА НЕ УКАЗАНА. ВЫБРАНА СТРАНИЦА ПО УМОЛЧАНИЮ (1)')

	base_part = p_url.split('?')[0]
	query_part = '?&s=104&view=list'
	page_part = '&p='

	total_pages = get_total_pages(p_url)

	print('\nПРОГРАММА НАЧАЛА ВЫПОЛНЕНИЕ РАБОТЫ')

	for i in range(startup_page, total_pages + 1):
		url_gen = base_part + query_part + page_part + str(i)
		print('\nСГЕНЕРИРОВАНА ССЫЛКА: '+ url_gen +'\n')
		get_page_data(url_gen)

		print('\nСТРАНИЦА ОБРАБОТАНА')

	print('\nПРОГРАММА ЗАВЕРШИЛА РАБОТУ')

if __name__ == '__main__':
	main()