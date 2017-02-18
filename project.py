from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def list_latest():
    categories = session.query(Category).order_by(asc(Category.name))
    title_items = 'Latest Items'
    items = session.query(Item).order_by(desc(Item.time_created))
    return render_template('categories.html', categories=categories,
                           title_items=title_items, items=items)

@app.route("/new", methods=['GET', 'POST'])
def new_item():
    if request.method == 'GET':
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('newitem.html', categories=categories)

    if request.method == 'POST':
        item = Item(name=request.form['name'],
                    description=request.form['description'],
                    category_id=int(request.form['category']))
        session.add(item)
        session.commit()
        return redirect(url_for('list_latest'))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
