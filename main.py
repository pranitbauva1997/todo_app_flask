from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/edit/<int:todo_id>/')
def edit(todo_id):
    todo_entry = session.query(List).filter_by(id = todo_id).one()
    return render_template('edit.html', entry = todo_entry)

@app.route('/edit_handler/<int:todo_id>/', methods = ['GET', 'POST'])
def edit_handler(todo_id):
    todo_entry = session.query(List).filter_by(id = todo_id).one()
    todo_entry.description = request.args['description']
    todo_entry.date = request.args['date']
    session.add(todo_entry)
    session.commit()
    return render_template('view.html', entry = todo_entry)

@app.route('/delete/<int:todo_id>/')
def delete(todo_id):
    todo_entry = session.query(List).filter_by(id = todo_id).one()
    session.delete(todo_entry)
    session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
