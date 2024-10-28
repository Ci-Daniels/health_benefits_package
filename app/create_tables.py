# create_tables.py
from health_essentials_models import db, app
from sqlalchemy.exc import IntegrityError

# Create all tables in the database
with app.app_context():
        try:
            # if table exist, we drop it
            db.drop_all()
            print("Existing tables dropped successfully.")

            # create the new tables
            db.create_all()
            print("Tables created successfully.")
        except IntegrityError:
            print("Error: Tables already exist or there was a database integrity issue.")



