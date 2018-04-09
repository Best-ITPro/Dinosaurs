# dino-img.py -  Dinosaurs beautiful images downloader
# Created by Best IT Pro
# http://best-itpro.ru

# Installing Beautiful Soup
# $ pip install beautifulsoup4
# $ apt-get install python3-bs4 (for Python 3)  - Ubuntu

# Installing a parser
# $ pip install lxml
# $ apt-get install python-lxml

# Installing urllib
# $ pip install urllib

# Проверка pip freeze

# target = https://wall.alphacoders.com/by_sub_category.php?id=134799&name=Dinosaur+Wallpapers&page=1

import requests
from bs4 import BeautifulSoup
import re
import os
import time

# Загрузка страницы
def get_html(url):
	r = requests.get(url)
	# если <Response [200]> - всё ок
	print (r)
	# само содержимое
	#print (r.text)
	# возвращаем именно содержимое!
	return r.text

# Получение номеров изображений
def get_links (html):
	# список ссылок на изображения
	imgs = []
	# Создаём объект супа
	soup = BeautifulSoup (html, 'lxml')
	# Вытаскиваем ссылки
	links = soup.find_all('a', href=re.compile('big.php'))
	#print (link)
	
	for a in links:
		link = a.get ('href')
		print (link)
		# получаем ссылку вида 'big.php?i=номер_изображения' и оставляем только 'номер_изображения'
		imgs.append (link [10:] )
	return imgs

# Загрузка изображений
def download_img(imgs, download_folder, url_img_target):

	path = os.getenv("PWD", os.getcwd())
	download_folder = path + '\\' + download_folder + '\\'
	print ("Папка для изображений :", download_folder)
	for element in imgs: 

		download_link = download_folder + element + '.jpg'
		print ("Получаем файл : ", download_link)
		f=open(download_link,"wb") #открываем файл для записи, в режиме wb
		
		url_link = url_img_target + element [:3] + '/' + element + '.jpg'
		print ("Ссылка для скачивания файла : ", url_link)

		ufr = requests.get(url_link) #делаем запрос
		status = ufr.status_code
		print ("Статус соединения: ", status)
		
		if status != 200:
			i = 2
			while (i < 10):
				
				url_img_target_new = 'https://images'+ str(i) + '.alphacoders.com/'
				url_link = url_img_target_new + element [:3] + '/' + element + '.jpg'
				ufr = requests.get(url_link) #делаем запрос
				status = ufr.status_code
				print ("Статус соединения: ", status)
				if status == 200:
						i = 9
				i += 1

		f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
		f.close()

			

def main():
	# Target_URL
	url = "https://wall.alphacoders.com/by_sub_category.php?id=134799&name=Dinosaur+Wallpapers&page="
	page_start = 1
	page_end = 7

	# URL с изображениями
	url_img = 'https://wall.alphacoders.com/big.php?i='
	url_img_target = 'https://images3.alphacoders.com/872/87235.jpg' # образец (!)
	url_img_target = 'https://images.alphacoders.com/'
	
	# Папка для сохранения
	download_folder = "img"
	
	# Последовательный вызов функций в цикле

	page_curr = page_start
	time_begin = time.clock() 

	while page_curr <= page_end:

		url = url + str (page_curr)
		html = get_html(url)
		result = get_links (html)
		print (result)
		download_img(result, download_folder, url_img_target)
		page_curr +=1

	time_end = time.clock() 
	time_delta = time_end - time_begin

	print("\n\r")
	print ("Загрузка изображений окончена!")
	message ="Время выполнения программы: " +str(time_delta)+ " сек - или " +str(time_delta/60) + " мин"
	print (message)

# Точка входа (если файл запущен из консоли)
if __name__ == '__main__':
	main()