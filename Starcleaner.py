import os

def clean():
	print('Cleaning...')
	try:
		os.system('taskkill /im chrome.exe /f')
		print('Done')
	except:
		print('Error')

def main():
	clean()

if __name__ == '__main__':
	main()