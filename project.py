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

@app.route("/catalog/item/<int:item_id>")
def item_details(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('itemdetails.html', item=item)


@app.route("/catalog/<int:category_id>")
def items_category(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('categories.html', title_items=category.name,
                           items=items)


@app.route("/delete/item/<int:item_id>", methods=['GET', 'POST'])
def delete_item(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        return render_template('deleteitem.html', item=item)
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('list_latest'))


@app.route("/edit/item/<int:item_id>", methods=['GET', 'POST'])
def edit_item(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('edititem.html', item=item, categories=categories)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category']
        session.add(item)
        session.commit()
        return redirect(url_for('item_details', item_id=item.id))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
