import time
from selenium import webdriver
from selenium.webdriver import Chrome

browser = False

class BrowserStuff():
	def launch_browser():
		global driver
		print('browser initialization')
		chromeOptions = webdriver.ChromeOptions()
		chromeOptions.add_argument("headless")
		chromeOptions.add_argument('--ignore-certificate-errors')
		chromeOptions.add_argument("--test-type")
		chromeOptions.add_argument("--window-size=1280x3000")
		driver = webdriver.Chrome(chrome_options=chromeOptions)

		print('browser launched')
		return driver

	def open_page(url, filename):
		global driver

		driver.get(url)
		print(url)
		driver.save_screenshot(filename)
		print('screenshot saved')

def browser_logic(url, filename):
	global browser
	if browser == False:
		BrowserStuff.launch_browser()
		BrowserStuff.open_page(url, filename)
		print('page has been opened')
		browser = True
	else:
		BrowserStuff.open_page(url, filename)
		print('page has been opened')

def main():
	filename = 0
	urls = ['https://www.avito.ru/stavropol/kvartiry/2-k_kvartira_65_m_59_et._1676844596',
			'https://www.avito.ru/stavropol/zemelnye_uchastki/uchastok_16_sot._snt_dnp_1551738138']
			
	for url in urls:
		browser_logic(url, str(filename)+'.png')
		filename += 1

if __name__ == '__main__':
	main()
	print('driver quit')
	driver.quit()