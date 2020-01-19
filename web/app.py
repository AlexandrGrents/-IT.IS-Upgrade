import json
import sys

from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import select

# импорт описанных баз данных
sys.path.append('../')
from alToTheBottomDB import EventsCountry, CountryCategory, DaypartCatrgory, Base

engine = create_engine('sqlite:///../all_to_the_bottom.db', echo=False)
SESSION_DB = sessionmaker(bind=engine)()

app = Flask(__name__)


@app.route('/')
def index():
	print("in index")
	return render_template('index.html')

@app.route('/events_per_country', methods=['GET'])
def events_per_country():
	res = [{"country": elem.country, "count":elem.count} for elem in SESSION_DB.query(EventsCountry).order_by('count')]
	SESSION_DB.commit()
	return json.dumps(res)

@app.route('/country_category', methods=['POST'])
def country_category():
	category = request.data.decode("utf-8")
	res = [{"country": elem.country, "count":elem.count} for elem in SESSION_DB.query(CountryCategory).filter(CountryCategory.category == category).order_by('count')]
	SESSION_DB.commit()
	return json.dumps(res)


@app.route('/daypart_category', methods=['POST'])
def daypart_category():
	category = request.data.decode("utf-8")
	res = [{"daypart": elem.daypart, "count":elem.count} for elem in SESSION_DB.query(DaypartCatrgory).filter(DaypartCatrgory.category == category).order_by('count')]
	SESSION_DB.commit()
	return json.dumps(res)

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)