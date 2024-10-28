import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from health_essentials_models import Manufacturer
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

# paths to the excel files
file3_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/health_benefits_essentials_package.xlsx'

# load data
manufacturer_df = pd.read_excel(file3_path, sheet_name='combined data', engine='openpyxl')

# Handle column name issues by stripping spaces
manufacturer_df.columns = manufacturer_df.columns.str.strip()

# populate the condition table
def populate_manufacturer_data():
    # create the session to call the db 
    session = db.session

    for index, row in manufacturer_df.iterrows():
        try:
            manufacturer = session.query(Manufacturer).filter_by(Manufacturer_Name=row['Manufacturer_Name']).first()
            if not manufacturer:
                manufacturer = Manufacturer(
                    atc_id=row['atc_id'],                    
                    atc_code_name=row['atc_code_name'],
                    Manufacturer_Name=row['Manufacturer_Name'],
                    Medicine_Name=row['Medicine_Name']
                )
                session.add(manufacturer)
                session.commit()                
             
        except Exception as Error:
            print(f"Population not successful: {Error}")
            session.rollback()

    session.commit()

# Execute the populate_data function
if __name__ == "__main__":
    with app.app_context():  
        populate_manufacturer_data()        
        print("Data population completed.")