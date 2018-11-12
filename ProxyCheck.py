import socks
import socket
import requests
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().chrome}

def setProxy(ip, port):
	socks.set_default_proxy(socks.SOCKS5, ip, int(port))
	socket.socket = socks.socksocket
	print('Прокси сокет установлен')

def getIP():
	print('Попытка получить IP')
	ip = requests.get('http://ident.me').text
	print('Новый IP адрес: '+ip)

def writeIP(data):
	f = open('proxylist.txt', 'a+')
	f.write(data+'\n')
	f.close()

def avitoBreach():
	global ipport

	print('Попытка установления соединения с сайтом через прокси\n')
	try:
		r = requests.get('https://www.avito.ru/stavropolskiy_kray/kvartiry/prodam/2-komnatnye?p=11&view=list', headers=headers)
		if str(r) == '<Response [200]>':
			print('='*17)
			print('Успешно')
			print('='*17)
			print(r)

			writeIP(ipport)
		else:
			print('Сайт не вернул [200]')
			print(r)
	except:
		print('x'*14)
		print('Ошибка')
		print('x'*14)	

def main():
	global ipport
	ipport = input('Socket: ')
	ip = ipport.split(':')[0]
	port = ipport.split(':')[-1]

	setProxy(ip, port)
	getIP()

	avitoBreach()

if __name__ == '__main__':
	main()