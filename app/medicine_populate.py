import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from health_essentials_models import Medicine
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
file4_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/cleanedData.xlsx'
file5_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/health_benefits_essentials_package.xlsx'
file6_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/KEML_clean data - Medicine, dose form, unit of issue, etc.xlsx'
file7_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/final_benefits_package.xlsx'

# Load Excel sheets into DataFrames
medicine_df = pd.read_excel(file4_path, sheet_name='cleanedData', engine='openpyxl')
medicine_df1 = pd.read_excel(file5_path, sheet_name='combined data', engine='openpyxl')
medicine_df2 = pd.read_excel(file6_path, sheet_name='Standardization', engine='openpyxl')
medicine_df3 = pd.read_excel(file7_path, sheet_name='Final_data', engine='openpyxl')

# Handle column name issues by stripping spaces
medicine_df.columns = medicine_df.columns.str.strip()

# Handle column name issues by stripping spaces
medicine_df1.columns = medicine_df1.columns.str.strip()

# Handle column name issues by stripping spaces
medicine_df2.columns = medicine_df2.columns.str.strip()

# Handle column name issues by stripping spaces
medicine_df3.columns = medicine_df3.columns.str.strip()

# Perform a merge on the DataFrames
try:
    combined_df = pd.merge(medicine_df1, medicine_df, on='atc_code_name', how='left')
    combined_df = combined_df.loc[:, ~combined_df.columns.str.contains('^Unnamed')]          
    print("The list of columns in the combined dataframe:", combined_df.columns)
           
except Exception as Error:
    print(f"Not successful: {Error}")

combined_df2 = combined_df.rename(columns ={'Medicine_Name_x':'Medicine_Name'})
combined_df2 = combined_df2.drop(columns =['Medicine_Name_y'])
print("The list of columns in the combined dataframe:", combined_df2.columns)

# Perform a merge on the DataFrames
try:
    combined_df3 = pd.merge(combined_df2, medicine_df2, on='Medicine_Name', how='left')         
    print("The list of columns in the combined dataframe:", combined_df3.columns)
           
except Exception as Error:
    print(f"Not successful: {Error}")

combined_df4 = combined_df3.rename(columns ={
    'Dose_Form_x':'Dose_Form',
    'Strength_x': 'Strength',
    })
combined_df4 = combined_df4.drop(columns =['Dose_Form_y','Strength_y'])
print("The list of columns in the combined dataframe:", combined_df4.columns)

# save the merged document
#combined_df4.to_excel('final_benefits_package.xlsx', index=False)
#print("File has been saved in the working directory.")

# populate the condition table
def populate_medicine_data():
    # create the session to call the db 
    session = db.session

    for index, row in medicine_df3.iterrows():
        try:
            medicine = session.query(Medicine).filter_by(Medicine_Name=row['Medicine_Name'],).first()
            if not medicine:
                # Add a new medicine entry
                medicine = Medicine(
                    atc_id =row['atc_id'],
                    atc_code_name=row['atc_code_name'],
                    Medicine_Name=row['Medicine_Name'],
                    Medicine_class=row['Medicine_class'],
                    Dose_Form=row['Dose_Form'],
                    Strength=row['Strength'],
                    LOU=row['LOU'],
                    Therapeutic_category=row['Therapeutic_category'],
                    Therapeutic_subcategory=row['Therapeutic_subcategory'],
                    Route_of_Administration=row['Route_of_Administration'],
                    Unit_of_Issue =row['Unit_of_Issue']                    
                )
                session.add(medicine)
                session.commit() 
        except Exception as Error:
            print(f"Population not successful: {Error}")
            session.rollback()

    session.commit()

# Execute the populate_data function
if __name__ == "__main__":
    with app.app_context():  
        populate_medicine_data()        
        print("Data population completed.")