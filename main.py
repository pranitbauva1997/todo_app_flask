from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, List

app = Flask(__name__)

engine = create_engine('sqlite:///todo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    todo_entry = List(description = request.args['description'],
                      date = request.args['date'])
    session.add(todo_entry)
    session.commit()
    return "Successfully created added to list"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
