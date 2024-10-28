import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from health_essentials_models import Conditions
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Medicine, Manufacturer, Cost, 
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
file4_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/Kenya Essential Benefit Package for UHC WIP Final GROUP 26.09.24.xlsx'
file5_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/test_health_benefits_essentials_package.xlsx'
file6_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/test2_health_benefits_essentials_package.xlsx'

# Load Excel sheets into DataFrames
conditions_df = pd.read_excel(file4_path, sheet_name='PHC Fund', engine='openpyxl')
conditions_df1 = pd.read_excel(file5_path, sheet_name='conditions data', engine='openpyxl')
conditions_df2 = pd.read_excel(file6_path, sheet_name='conditions data', engine='openpyxl')

# Debug: 
print("Conditions DataFrame Columns Before Renaming:", conditions_df.columns)
print(conditions_df.head()) 

# Handle column name issues by stripping spaces
conditions_df.columns = conditions_df.columns.str.strip()

# Handle column name issues by stripping spaces
conditions_df1.columns = conditions_df1.columns.str.strip()

# Handle column name issues by stripping spaces
conditions_df2.columns = conditions_df2.columns.str.strip()

# rename the needed coluns]
try:
    conditions_df1.rename(columns={
        'condition_name':'Condition_name',
        'service_type':'Care_Type',
        'interventions':'Interventions',
        'target_population':'Target_population',
        'proportion_allocated':'Population_allocated',
        'Unit cost (KES)':'Unit_cost'  ,
        'Total cost' :'Total_cost' , 
        'Costing unit':'Costing_unit'
    },inplace=True)
    print("Renaming successful. Columns after renaming:", conditions_df1.columns)
except Exception as e:
    print(f"Renaming not successful: {e}")

# save the merged docum
#conditions_df1.to_excel('test2_health_benefits_essentials_package.xlsx', index=False)
#print("File has been saved in the working directory.")

# populate the condition table
def populate_conditions_data():
    # create the session to call the db 
    session = db.session

    for index, row in conditions_df2.iterrows():
        try:
            conditions = session.query(Conditions).filter_by(Interventions=row['Interventions']).first()
            if not conditions:
                # Add a new medicine entry
                conditions = Conditions(
                    Condition_name=row['Condition_name'],
                    Care_Type=row['Care_Type'],
                    Interventions=row['Interventions'],
                    Costing_unit=row['Costing_unit'],
                    Unit_cost=row['Unit_cost'],
                    Total_cost=row['Total_cost'],
                    Target_population=row['Target_population'],
                    Population_allocated=row['Population_allocated']             
                )
                session.add(conditions)
                session.commit() 
        except Exception as Error:
            print(f"Population not successful: {Error}")
            session.rollback()

    session.commit()

# Execute the populate_data function
if __name__ == "__main__":
    with app.app_context():  
        populate_conditions_data()        
        print("Data population completed.")