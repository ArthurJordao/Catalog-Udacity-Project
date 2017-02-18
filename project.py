from flask import Flask, render_template
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

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
