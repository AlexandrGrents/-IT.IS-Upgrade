import re
from datetime import datetime,time,date
from enum import Enum

import geoip2.database
import geoip2.errors

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils.functions import drop_database

# создаём соединение с базой данных ip-адрессов (нужно для определения страны)
GEOIP2_READER = geoip2.database.Reader('Geoip2/GeoLite2-Country.mmdb')

# создаём соединение с заполняемой базой данных
engine = create_engine('sqlite:///../all_to_the_bottom.db', echo=False)
drop_database(engine.url)
Base = declarative_base()

class EventsCountry(Base):
	__tablename__ = 'events_per_country'
	country = Column(String(40), primary_key=True)
	count = Column(Integer)
	def __init__(self, country, count=1):
		self.country = country
		self.count = count

class CountryCategory(Base):
	__tablename__ = 'country_category'
	country = Column(String(40), primary_key=True)
	category = Column(String(40), primary_key=True)
	count = Column(Integer)
	def __init__(self, country, category,count = 1):
		self.country = country
		self.category = category
		self.count = count

class DaypartCatrgory(Base):
	__tablename__ = 'daypart_category'
	daypart = Column(String(8), primary_key = True)
	category = Column(String(40), primary_key = True)
	count = Column(Integer)
	def __init__(self,daypart,category,count=1):
		self.daypart = daypart
		self.category = category
		self.count = count

SESSION_DB = sessionmaker(bind=engine)()
Base.metadata.create_all(engine)

# Определение названия страны по ip
def getCountryByIp(ip):
    try:
        country = GEOIP2_READER.country(ip).country.name
    except geoip2.errors.AddressNotFoundError:
        country = 'another'
    if country is None:
    	country = 'another'
    return country

# Определение периода дня (ночь, утро, день, вечер) по времени
def getDaypartByTime(action_time):
	if 		action_time < time(6,0,0): 	return "night"
	elif 	action_time < time(12,0,0): return "morning"
	elif	action_time < time(18,0,0): return "day"				
	else:								return "evening"


if __name__ == '__main__':
	lineCount = 0				# счётчик для кол-ва строк в лог-файле
	countryCategory_count = 0	# счётчик для добавленных в таблицу events_per_country строк
	eventsCountry_count = 0		# счётчик для добавленных в таблицу country_category строк
	daypartCatrgory_count = 0	# счётчик для добавленных в таблицу daypart_category строк
	print("Начинается считывание файла")
	with open("../Input data/logs.txt") as log_file:
		#цикл по всем строкам лог-файла
		for line in log_file:
			lineCount+=1
			# Получение даты, времени, ip, адреса перехода (url), страны пользователя и периоде дня перехода (daypart)
			action_date = datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', line).group(),"%Y-%m-%d").date()
			action_time = datetime.strptime(re.search(r'\d{2}:\d{2}:\d{2}', line).group(),"%H:%M:%S").time()
			ip = re.search(r'\d+\.\d+\.\d+\.\d+', line).group()
			url = re.search(r'https://all_to_the_bottom.com\S+',line).group()[30:-1]
			country = getCountryByIp(ip)
			daypart = getDaypartByTime(action_time)
			
			# Увеличение на 1 счётчика действий для данной страны. ЕСЛИ строки с данной страной нет, то она добавляется, счётчик в этой строке равен 1
			if SESSION_DB.query(EventsCountry).filter_by(country = country).update({EventsCountry.count : EventsCountry.count+1}) == 0:
				countryCategory_count+=1
				SESSION_DB.add(EventsCountry(country = country))

			# Проверка на то, что url перехода является страницей категории
			if (url!='' and url.count('/')==0 and not url.startswith('pay') and not url.startswith('cart') and not url.startswith('success_pay')):
				category = url

				# Увеличение на 1 счётчика просмотра данной категории для данной страны. 
				# ЕСЛИ строки с данной комбинацией страны и категории нет, то она добавляется, счётчик в этой строке равен 1
				if SESSION_DB.query(CountryCategory).filter_by(country = country, category = category).update({CountryCategory.count : CountryCategory.count + 1}) == 0:
					eventsCountry_count+=1
					SESSION_DB.add(CountryCategory(country = country, category = category))

				# Увеличение на 1 счётчика просмотра данной категории для данного времени суток.
				# ЕСЛИ строки с данной комбинацией времени суток и категории нет, то она добавляется, счётчик в этой строке равен 1
				if SESSION_DB.query(DaypartCatrgory).filter_by(daypart = daypart, category = category).update({DaypartCatrgory.count : DaypartCatrgory.count + 1}) == 0:
					daypartCatrgory_count+=1
					SESSION_DB.add(DaypartCatrgory(daypart = daypart, category = category))

			#конец цикла по всем строкам лог-файла
		# Сохранение результатов и закрытие соединения с базой данных
		SESSION_DB.commit()	
		SESSION_DB.close()
		print ("Файл считан.Всего строк:", lineCount)
		print ("Добавлено записей в таблицу events_per_country:",eventsCountry_count)
		print ("Добавлено записей в таблицу country_category:",countryCategory_count)
		print ("Добавлено записей в таблицу daypart_category:",daypartCatrgory_count)
		print ("Всего добавлено записей:",eventsCountry_count+countryCategory_count+daypartCatrgory_count)