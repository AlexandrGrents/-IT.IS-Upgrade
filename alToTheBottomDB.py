from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

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