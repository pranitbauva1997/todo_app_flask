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
    list = session.query(List).all()
    return render_template('index.html', list = list)

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    todo_entry = List(description = request.args['description'],
                      date = request.args['date'])
    session.add(todo_entry)
    session.commit()
    return render_template('view.html', entry = todo_entry)

@app.route('/view/<int:todo_id>/')
def view(todo_id):
    todo_entry = session.query(List).filter_by(id = todo_id).one()
    return render_template('view.html', entry = todo_entry)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
