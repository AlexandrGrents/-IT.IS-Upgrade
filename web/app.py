import json

from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///all_to_the_bottom.db', echo=True)
SESSION_DB = sessionmaker(bind=engine)()

@app.route('/', methods=['GET'])
def index():
	return render_template('templates/index.html')


if __name__ == '__main__':
    app.run()