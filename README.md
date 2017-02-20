# Catalog Project - Udacity Project
## How to run it
* Install vagrant and git in your machine
* Clone this repository with the command:
```
git clone https://github.com/ArthurJordao/Catalog-Udacity-Project.git catalog
```
* Change your directory to project's folder:
```
cd catalog
```
* Up the virtual machine:
```
vagrant Up
```
* Connect into the virtual machine with ssh:
```
vagrant ssh
```
* Go to the foler /vagrant
```
cd /vagrant
```
* Create the db:
```
python database_setup.py
```
* Load the db with some categories:
```
python lot_of_categories.py
```
* up the server:
```
python project.py
```
* The application is up in localhost:5000

## Project tips
* You can add some categories in the lot_of_categories.py
* The folder templates has the html of the project
* The folder static has static files like css
* project.py has the serve logic

## Endpoints
* the project has 3 json endpoints:
1. /categories/JSON - list all categories
2. /catalog/\<int:category_id\>/JSON  - list items from a category
3. /catalog/item/\<int:item_id\>/JSON - show the item details
