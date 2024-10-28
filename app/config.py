import os
from app import app
from dotenv import load_dotenv

load_dotenv()

class Config:
    # for the shif database connection
    SQLALCHEMY_DATABASE_URI_HESBP = os.getenv('DATABASE_URL_1', 'postgresql://postgres:c3mA_hUb@localhost/shif_health_essential_benefits_package')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_BINDS = {
        'shif_health_essential_benefits_package': SQLALCHEMY_DATABASE_URI_HESBP
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False