import os
import gspread
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from health_essentials_models import CHRONIC_Fund, SHIF_Fund, PHC_Fund, EMERGENCY_Fund, Conditions
from sqlalchemy.orm import sessionmaker
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Import the user credentials
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
db_health = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')
credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
print("Credentials Path:", credentials_path)

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)

# Initialize the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{server}:{port}/{db_health}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Update tables with new data from Google Sheets
def update_table(sheet_name, table_name, has_condition_name=False):
    sheet = client.open("Essential Pharmaceutical Benefits Package data").worksheet(sheet_name)
    
    # Fetch all rows as a list of dictionaries
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Iterate through all rows in sheets and upsert the data
    for _, row in df.iterrows():
        row_data = dict(row)
        print(f"Inserting row: {row_data}")
        
        # If the table has a condition_name and needs a condition_ID from the Conditions table
        if has_condition_name:
            condition_name = row_data.get("Condition_name")
            if condition_name:
                # Query the Conditions table to get the condition_ID based on condition_name
                condition = db.session.query(Conditions).filter_by(Condition_name=condition_name).first()
                if condition:
                    row_data['condition_ID'] = condition.condition_ID
                else:
                    print(f"Condition '{condition_name}' not found in Conditions table, skipping row.")
                    continue  #skip if no matching conditions are found

        try:
            new_record = table_name(**row_data)
            db.session.add(new_record)
        except Exception as error:
            print(f"Error adding record {row_data}: {error}")
    
    try:
        db.session.commit()
    except Exception as error:
        print(f"Error committing data from {sheet_name}: {error}")
        db.session.rollback()

# Update each table with the respective sheet
if __name__ == "__main__":
    success = True  

    with app.app_context():
        try:
            update_table("chronic", CHRONIC_Fund, has_condition_name=True)
            update_table("emergency", EMERGENCY_Fund, has_condition_name=True)
            update_table("phc", PHC_Fund, has_condition_name=True)  
            update_table("shif", SHIF_Fund, has_condition_name=True)  
        except Exception as e:
            print(f"An error occurred during data insertion: {e}")
            success = False  

    if success:
        print("Data population completed successfully.")
    else:
        print("Data population encountered errors.")
