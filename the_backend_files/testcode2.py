#just annother test code!!
'''
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from models import User, Base
from main import engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new session
db = SessionLocal()

# Insert data into the User table
stmt = insert(User).values(username="spongebob", email="spongebobsquarepants@gmail.com", cryptkey="password")
try:
    db.execute(stmt)
    db.commit()
    print("Data inserted successfully!")
except Exception as e:
    db.rollback()
    print(f"Failed to insert data: {e}")
finally:
    db.close()
    '''