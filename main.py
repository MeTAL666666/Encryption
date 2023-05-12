import os, sys, requests, json

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, abort, jsonify
'''
create_words - функция принимает на вход шифр слова, маску для поиска слова. Возвращает массив букв,
соответсвующих шифру и список всех найденных слов с помощью API, соответствующих маске.

get_keyword - функция принимает на вход все буквы, необходимые для составления ключевого слова.
Возвращает составленное ключевое слово

write_crossword - функция составляющая и выводящая на экран весь кроссворд и ключевое слово по заданию

'''
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
	if request.method == 'POST':
		try:
			word_code = request.form['code']
			mask = request.form['mask']
			if word_code and mask:
				result = create_words(word_code, {"mask": mask})				# отправить запрос к API
				flag = 0														# флаг
				for word in result[-1]:											# цикл по всему списку найденных слов
					if len(word) <= len(result[0]):								# если длина слова меньше или равна длине массива набора букв
						for key, char_set in enumerate(result[0]):				# пронумеровать каждый набор букв
							char = word[key] if key <= len(word) + 1 else ""	# пока порячядковый номер меньше или равен длине слова + 1,... 
																				# присвоить переменной букву из проверяемого слова
							if char not in char_set:							# если буква не входит в набор букв по заданию, прерывать цикл
								break
						else:													# если break не сработал, значит слово полностью соответсвует набору букв
							flag = 1											# флаг
							return jsonify({'output': word, 'word_code': word_code, 
								'mask': mask})
				if flag == 0:													# если флан остался со значением 0...
					return jsonify({'output': 'Не найдено подходящих слов!'})	
		except:
			letters = request.get_json()['letters']
			return jsonify ({'keyword':get_keyword(letters)})
		return jsonify({'error' : 'Missing data!'})
	return render_template('index.html')

def create_words(word_code, mask):
	# шифр по заданию
	code = {'1': ("а", "в", "г"),
			'2': ("е", "и", "к"),
			'3': ("л", "н", "о"),
			'4': ("п", "р", "с"),
			'5': ("т", "у", "щ"),
			'6': ("ь", "я", "")}

	url = "https://poncy.ru/crossword/crossword-solve.jsn?"		# ссылка на API poncy.ru
	response = requests.get(url, params=mask)					# запрос к API
	data = json.loads(response.text)							# десереализация ответа в словарь
	received_words = [i.lower() for i in data["words"]]			# получение из ответа списка слов 
	return [code[i] for i in list(word_code)], received_words

def get_keyword(letters):
	# заголовок для запроса - необходим для корректного ответа сервиса
	headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"\
				" (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
	MAX_RETRIES = 20
	url =f'https://sanstv.ru/find_words/word-{letters}/strong-2?'	# сервис для составления анограммы
	# создание объекта сессии для обращения к сервису, т.к. сервис не предоставляет доступ по API
	session = requests.Session()
	adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
	session.mount('https://', adapter)
	session.mount('http://', adapter)
	# парсинг html-страницы с ответом от сервиса
	response = BeautifulSoup(session.get(url, headers = headers).text, 'lxml')
	keyword = response.find('ol',class_='words').find(target='_blank ').text
	
	return keyword

'''def write_crossword():

	str_1 = input('Введите ПЕРВУЮ строку: ')
	str_2 = input('Введите ВТОРУЮ строку: ')
	str_3 = input('Введите ТРЕТЬЮ строку: ')
	str_4 = input('Введите ЧЕТВЁРТУЮ строку: ')
	str_5 = input('Введите ПЯТУЮ строку: ')
	# обработка исключений
	try:
		key_letters = str_1[4] + str_2[6] + str_3[1] + str_3[3] + str_4[0] + str_4[3] + str_4[-1] + str_5[-3] + str_5[-1]

		print(f'\nИтоговый кроссворд:\n{str_1}\n{str_2}\n{str_3}\n{str_4}\n{str_5}')
		print(f'\nКлючевое слово: {get_keyword(key_letters)}')
		os.system('pause')

	except IndexError:
		print('Ошибка в составлении кроссворда!')
		os.system('pause')
		sys.exit()

	except AttributeError:
		print('Ключевое слово не найдено!')
		os.system('pause')
		sys.exit()'''
# точка входа
if __name__ == '__main__':
	app.debug=False
	# Запуск программы
	app.run()

	'''# повторять цикл, пока пользователь не перейдет к вводу всего кроссворда
	while True:
		word_code = input('Введите шифр слова (оставить пустым для ввода всего кроссворда): ').replace(" ", "")

		if word_code != '':
			mask = input(f'Введите маску слова для поиска ({len(word_code.replace(" ", ""))} букв): ')

			if mask != '' and len(word_code.replace(" ", "")) == len(mask):		# если длина шифра и маски совпадают...
				result = create_words(word_code, {"mask": mask})				# отправить запрос к API
				flag = 0														# флаг
				for word in result[-1]:											# цикл по всему списку найденных слов
					if len(word) <= len(result[0]):								# если длина слова меньше или равна длине массива набора букв
						for key, char_set in enumerate(result[0]):				# пронумеровать каждый набор букв
							char = word[key] if key <= len(word) + 1 else ""	# пока порячядковый номер меньше или равен длине слова + 1,... 
																				# присвоить переменной букву из проверяемого слова
							if char not in char_set:							# если буква не входит в набор букв по заданию, прерывать цикл
								break
						else:													# если break не сработал, значит слово полностью соответсвует набору букв
							flag = 1											# флаг
							print(f'Результат поиска: {word}\n')				# выводить подобранное слово
				if flag == 0:													# если флан остался со значением 0...
					print(f'Не найдено подходящих слов!\n')						# значит слово не было найдено
		else:																	
			write_crossword()													# если ничего не введено - вызвать функцию ввода кроссворда целиком...
			break'''																# завершить сценарий