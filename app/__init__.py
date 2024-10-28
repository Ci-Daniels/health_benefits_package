from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# instantiate the database
db = SQLAlchemy()

#create the application
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI_HESBP'] = f'postgresql://{user}:{password}@{server}:{port}/{db_health}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #initialize the appllication
    db.init_app(app)
    
    return app
