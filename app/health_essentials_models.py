import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# import the user credentials
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
db_health = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

# initialise the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{server}:{port}/{db_health}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# we will create models to create new tables in the database
#################################################### CONDITIONS TABLE ############################################################
class Conditions(db.Model):
    __tablename__ = 'Conditions'
    condition_ID = db.Column(db.Integer, autoincrement=True,nullable=False,primary_key=True)
    Condition_name = db.Column(db.String, nullable=False)
    Care_Type = db.Column(db.String)
    Interventions = db.Column(db.String)
    Costing_unit = db.Column(db.String)
    Unit_cost = db.Column(db.Float)
    Total_cost = db.Column(db.Float)
    Population_allocated = db.Column(db.Integer)
    Target_population = db.Column(db.Integer)  

    # Relationship to ChronicFund table
    chronic_funds = db.relationship('CHRONIC_Fund', backref='condition', lazy=True) 

    # Relationship to ChronicFund table
    shif_funds = db.relationship('SHIF_Fund', backref='condition', lazy=True)

    # Relationship to ChronicFund table
    phc_funds = db.relationship('PHC_Fund', backref='condition', lazy=True)

    # Relationship to ChronicFund table
    emergency_funds = db.relationship('EMERGENCY_Fund', backref='condition', lazy=True) 

#################################################### MEDICINE TABLE ############################################################
class Medicine(db.Model):
    __tablename__ = 'Medicine'
    # for the medicine ID 
    atc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    atc_code_name = db.Column(db.String,nullable=False)
    Medicine_Name = db.Column(db.String)
    Medicine_class = db.Column(db.String)
    Dose_Form = db.Column(db.String)
    Strength = db.Column(db.String)
    LOU = db.Column(db.Integer)
    Therapeutic_category = db.Column(db.String)
    Therapeutic_subcategory = db.Column(db.String)
    Route_of_Administration = db.Column(db.String)
    Unit_of_Issue = db.Column(db.String)

    # define relationship
        # A manufacturer supplies many medicines
    manufacturer = db.relationship('Manufacturer', back_populates='medicines')
    
#################################################### MANUFACTURERS TABLE ############################################################
class Manufacturer(db.Model):
    __tablename__ = 'Manufacturer'
    atc_code_name = db.Column(db.String,nullable=False)
    atc_id = db.Column(db.Integer, db.ForeignKey('Medicine.atc_id'),nullable=False)    
    # we will use both the atc_id and manufacturer_name as primary keys(Composite primary key)
    __table_args__ = (
        db.PrimaryKeyConstraint('atc_id', 'Manufacturer_Name'),
    )
    Manufacturer_Name = db.Column(db.String, nullable = False, unique = True)
    Medicine_Name = db.Column(db.String)

    # define relationships
    medicines = db.relationship('Medicine', back_populates='manufacturer')
 
#################################################### SHIF TABLE ############################################################
class SHIF_Fund(db.Model):
    __tablename__ = 'SHIF_Fund'
    intervention_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition_ID = db.Column(db.Integer,db.ForeignKey('Conditions.condition_ID'),nullable=False)
    Condition_name = db.Column(db.String, nullable=False)
    Care_Type = db.Column(db.String, nullable = False)
    Percentage_Coverage = db.Column(db.Float, nullable=False)
    Number_of_Medicines = db.Column(db.Integer)
    Intervention = db.Column(db.String, nullable=False)
    Medicine_Name = db.Column(db.String, nullable=False)
    Drug_Class = db.Column(db.String)
    Strength = db.Column(db.String)
    Dose_Form = db.Column(db.String)
    Route_of_Administration = db.Column(db.String)
    Unit_of_Issue = db.Column(db.String)
    Number_of_Doses = db.Column(db.Integer)
    Duration_of_Treatment = db.Column(db.Integer)
    Repeat_Prescription = db.Column(db.Integer)
    Allocated_Proportions = db.Column(db.Integer)
    Timestamp = db.Column(db.TIMESTAMP)
    Submit_data = db.Column(db.Integer)
    Number_of_sources = db.Column(db.Integer)
    Conditions_Open = db.Column(db.String)
    Assumptions = db.Column(db.String)
    Publication_title  = db.Column(db.String)
    Publication_Year = db.Column(db.String)
    Publication_URL = db.Column(db.String)

#################################################### PHC TABLE ############################################################
class PHC_Fund(db.Model):
    __tablename__ = 'PHC_Fund'
    intervention_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition_ID = db.Column(db.Integer,db.ForeignKey('Conditions.condition_ID'), nullable=False)
    Condition_name = db.Column(db.String, nullable=False)
    Care_Type = db.Column(db.String, nullable = False)
    Percentage_Coverage = db.Column(db.Float, nullable=False)
    Number_of_Medicines = db.Column(db.Integer)
    Intervention = db.Column(db.String, nullable=False)
    Medicine_Name = db.Column(db.String, nullable=False)
    Drug_Class = db.Column(db.String)
    Strength = db.Column(db.String)
    Dose_Form = db.Column(db.String)
    Route_of_Administration = db.Column(db.String)
    Unit_of_Issue = db.Column(db.String)
    Number_of_Doses = db.Column(db.Integer)
    Duration_of_Treatment = db.Column(db.Integer)
    Repeat_Prescription = db.Column(db.Integer)
    Allocated_Proportions = db.Column(db.Integer)
    Timestamp = db.Column(db.TIMESTAMP)
    Submit_data = db.Column(db.Integer)
    Number_of_sources = db.Column(db.Integer)
    Conditions_Open = db.Column(db.String)
    Assumptions = db.Column(db.String)
    Publication_title  = db.Column(db.String)
    Publication_Year = db.Column(db.String)
    Publication_URL = db.Column(db.String)
   
#################################################### EMERGENCY TABLE ############################################################
class EMERGENCY_Fund(db.Model):
    __tablename__ = 'Emergency_Fund'
    intervention_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition_ID = db.Column(db.Integer,db.ForeignKey('Conditions.condition_ID'),nullable=False)
    Condition_name = db.Column(db.String, nullable=False)
    Care_Type = db.Column(db.String, nullable = False)
    Percentage_Coverage = db.Column(db.Float, nullable=False)
    Number_of_Medicines = db.Column(db.Integer)
    Intervention = db.Column(db.String, nullable=False)
    Medicine_Name = db.Column(db.String, nullable=False)
    Drug_Class = db.Column(db.String)
    Strength = db.Column(db.String)
    Dose_Form = db.Column(db.String)
    Route_of_Administration = db.Column(db.String)
    Unit_of_Issue = db.Column(db.String)
    Number_of_Doses = db.Column(db.Integer)
    Duration_of_Treatment = db.Column(db.Integer)
    Repeat_Prescription = db.Column(db.Integer)
    Allocated_Proportions = db.Column(db.Integer)
    Timestamp = db.Column(db.TIMESTAMP)
    Submit_data = db.Column(db.Integer)
    Number_of_sources = db.Column(db.Integer)
    Conditions_Open = db.Column(db.String)
    Assumptions = db.Column(db.String)
    Publication_title   = db.Column(db.String)
    Publication_Year = db.Column(db.String)
    Publication_URL = db.Column(db.String)

#################################################### CHRONIC TABLE ############################################################
class CHRONIC_Fund(db.Model):
    __tablename__ = 'Chronic_Fund'
    intervention_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition_ID = db.Column(db.Integer,db.ForeignKey('Conditions.condition_ID'), nullable=False)
    Condition_name = db.Column(db.String, nullable=False)
    Care_Type = db.Column(db.String, nullable = False)
    Percentage_Coverage = db.Column(db.Float, nullable=False)
    Number_of_Medicines = db.Column(db.Integer)
    Intervention = db.Column(db.String, nullable=False)
    Medicine_Name = db.Column(db.String, nullable=False)
    Drug_Class = db.Column(db.String)
    Strength = db.Column(db.String)
    Dose_Form = db.Column(db.String)
    Route_of_Administration = db.Column(db.String)
    Unit_of_Issue = db.Column(db.String)
    Number_of_Doses = db.Column(db.Integer)
    Duration_of_Treatment = db.Column(db.Integer)
    Repeat_Prescription = db.Column(db.Integer)
    Allocated_Proportions = db.Column(db.Integer)
    Timestamp = db.Column(db.TIMESTAMP)
    Submit_data = db.Column(db.Integer)
    Number_of_sources = db.Column(db.Integer)
    Conditions_Open = db.Column(db.String)
    Assumptions = db.Column(db.String)
    Publication_title  = db.Column(db.String)
    Publication_Year = db.Column(db.String)
    Publication_URL = db.Column(db.String) 

if __name__ == '__main__':
    app.run(debug=True)