import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from health_essentials_models import Medicine, Manufacturer, Cost, Conditions
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Import the user credentials
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
db_health = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{server}:{port}/{db_health}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Paths to your Excel files
file5_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/Kenya Essential Benefit Package for UHC WIP Final GROUP 26.09.24.xlsx'
# Load Excel sheets into DataFrames
shif_df = pd.read_excel(file5_path, sheet_name='SHIF', engine='openpyxl')

# Debug: 
print("Conditions DataFrame Columns Before Renaming:", shif_df.columns)
print(shif_df.head()) 

# Handle column name issues by stripping spaces
shif_df.columns = shif_df.columns.str.strip()

# rename the needed coluns
try:
    shif_df.rename(columns={
        'Disease condition':'condition_name',
        'Category of health services':'service_type',
        'Intervention name':'interventions',
        'Fund':'fund_type',
        'Target population':'target_population',
        'Proportion allocated':'proportion_allocated'       
    },inplace=True)
    print("Renaming successful. Columns after renaming:", shif_df.columns)
except Exception as e:
    print(f"Renaming not successful: {e}")

# Drop unnamed columns
shif_df = shif_df.loc[:, ~shif_df.columns.str.contains('^Unnamed')]
print(shif_df.columns)


