from flask import Flask, render_template
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

def create_app():   
    app = Flask(__name__)
    app.config.from_object('config')
    return app

app=create_app()
db=SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Build the database:
# This will create the database file using SQLAlchemy


__import__('app.blueprints')
__import__('app.models')

db.create_all()


'''
The views are written in crud_view/resources/controllers.py
'''

 


