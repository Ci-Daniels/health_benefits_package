import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from health_essentials_models import Medicine, Manufacturer, Cost
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
file1_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/Combined Group 1,2,3_Pharmacy Benefit Package Costing tool.xlsx'
file2_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/KEML_clean data.xlsx'
file3_path = 'D:/CEMA PROJECTS/Kenya Essential Health Benefits Package(SHA)/health_benefits_essentials_package.xlsx'

# Load Excel sheets into DataFrames
costing_tool_df = pd.read_excel(file1_path, sheet_name='Costing  tool ', engine='openpyxl', header=1)
atc_code_df = pd.read_excel(file1_path, sheet_name='ATC Code Ref', engine='openpyxl')
standardization_df = pd.read_excel(file2_path, sheet_name='Standardization', engine='openpyxl')
shif1_df = pd.read_excel(file3_path, sheet_name='combined data', engine='openpyxl')

# Debug: 
print("Costing Tool DataFrame Columns Before Renaming:", costing_tool_df.columns)
print(costing_tool_df.head()) 

# Handle column name issues by stripping spaces
costing_tool_df.columns = costing_tool_df.columns.str.strip()

# Rename columns for clarity
try:
    costing_tool_df.rename(columns={
        'ATC Codes': 'atc_code_name',
        'Name of Medicine': 'medicine_name',
        'Dose-form': 'dose_form',
        'Strength / Size': 'strength',
        'LOU': 'LOU',
        'Therapeutic category': 'therapeutic_category',
        'Therapeutic subcategory': 'therapeutic_subcategory',
        'Fund?': 'fund_type',
        'Unit cost per pack':'unit_cost',
        'Total cost':'total_cost'

    }, inplace=True)
    print("Renaming successful. Columns after renaming:", costing_tool_df.columns)
except Exception as e:
    print(f"Renaming not successful: {e}")

# Debug atc code ref
print("ATC Code Reference DataFrame Columns Before Renaming:", atc_code_df.columns)
print(atc_code_df.head()) 

# Rename columns for clarity in ATC Code sheet
try:
    atc_code_df.rename(columns={
        'atc_code_id': 'atc_id',
        'atc_code_name': 'atc_code_name',
        'pharmacotheraupuetic_group': 'manufacturer_name'
    }, inplace=True)
    print("Renaming successful. Columns after renaming:", atc_code_df.columns)
except Exception as e:
    print(f"Renaming not successful: {e}")

# standardization tool dataframe
#print("Standardization DataFrame Columns Before Renaming:", standardization_df.columns)
#print(standardization_df.head()) 

# Handle column name issues by stripping spaces
standardization_df.columns = standardization_df.columns.str.strip()
# Rename columns for clarity in Standardization sheet
try:
    standardization_df.rename(columns={
        'Name of Medicine': 'medicine_name',
        'Dose-form': 'dose_form',
        'ROUTE OF ADMINISTRATION': 'route_of_admin',
        'UNIT OF ISSUE': 'unit_of_issue',
        'Strength of medicine': 'strength'
    }, inplace=True)
    print("Renaming successful. Columns after renaming:", standardization_df.columns)
except Exception as e:
    print(f"Renaming not successful: {e}")

# Perform a merge on the DataFrames
try:
    combined_df = pd.merge(costing_tool_df, atc_code_df, on='atc_code_name', how='left')
    combined_df = combined_df.loc[:, ~combined_df.columns.str.contains('^Unnamed')]
    shif_df = pd.merge(combined_df, standardization_df, on=['medicine_name','strength','dose_form'], how='left')
    shif1_df = shif_df.loc[:, ~shif_df.columns.str.contains('^Unnamed')]
    #drop all rows without atc_code name
    shif2_df = shif1_df[(shif1_df['atc_code_name'].notna()) & (shif1_df['atc_code_name'] != '')]
   
    print("The list of columns in the combined dataframe:", shif2_df.columns)
except Exception as Error:
    print(f"Not successful: {Error}")

# save the merged document
#shif_df.to_excel('health_benefits_essentials_package.xlsx', index=False)
#print("File has been saved in the working directory.")

# Function to populate the database
def populate_data():
    # create the session to call the db 
    session = db.session

    for index, row in shif1_df.iterrows():
        try:
            medicine = session.query(Medicine).filter_by(medicine_name=row['medicine_name'],).first()
            if not medicine:
                # Add a new medicine entry
                medicine = Medicine(
                    atc_id =row['atc_id'],
                    atc_code_name=row['atc_code_name'],
                    medicine_name=row['medicine_name'],
                    dose_form=row['dose_form'],
                    strength=row['strength'],
                    LOU=row['LOU'],
                    therapeutic_category=row['therapeutic_category'],
                    therapeutic_subcategory=row['therapeutic_subcategory'],
                    route_of_admin=row['route_of_admin'],
                    unit_of_issue=row['unit_of_issue']                    
                )
                session.add(medicine)
                session.commit() 

            # Add Manufacturer entry
            manufacturer = session.query(Manufacturer).filter_by(manufacturer_name=row['manufacturer_name']).first()
            if not manufacturer:
                manufacturer = Manufacturer(
                    atc_id=row['atc_id'],                    
                    atc_code_name=row['atc_code_name'],
                    manufacturer_name=row['manufacturer_name']
                )
                session.add(manufacturer)
                session.commit()  

             # Add cost entry
            cost = session.query(Cost).filter_by(manufacturer_name=row['manufacturer_name']).first()
            if not cost:
                cost = Cost(
                    atc_id=row['atc_id'],       
                    atc_code_name=row['atc_code_name'],  
                    manufacturer_name=row['manufacturer_name'],         
                    fund_type=row['fund_type'],
                    unit_cost=row['unit_cost'],
                    total_cost=row['total_cost']
                )
                session.add(cost)
                session.commit()  

        except Exception as Error:
            print(f"Population not successful: {Error}")
            session.rollback()

    session.commit()

# Execute the populate_data function
if __name__ == "__main__":
    with app.app_context():  
        populate_data()        
        print("Data population completed.")