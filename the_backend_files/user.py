import datetime

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy import  Column, String, Integer, LargeBinary, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from passlib.context import CryptContext
from models import User, Location,State,TravelData
from main import engine  
import uvicorn

# FastAPI app setup
app = FastAPI()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Pydantic models for data validation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    location: str
    state: str
    
    country: str
# class Location(BaseModel):
#    location_id: int
#    location_name :str
#    state_id: int
   
class UserResponse(BaseModel):
    username_id: int
    username: str
    email: str
    location :str
    state: str
    country : str
    password:str
    
class UserR(BaseModel):
    username_id: int
    username: str
    email: str
    profie_pic:str
    location_id: int
    crptkey: str

class Travel(BaseModel):
    username_id: int
    username: str
    start_location: str
    start_location_state: str
    start_location_country: str

    destination: str
    destination_state: str
    destination_country: str
    travel_date: str
    travel_type: str
    travel_price: int
    days: int
    stay: bool
    stay_price: int
    travel_time: int
    fromdate: datetime.date
    todate: datetime.date
    backdate: datetime.date
    #
class Travel_db(BaseModel):
    username_id: int
    start_location_id: int
    
    destination_id: int

    travel_type: str
    travel_price: int
    days: int
    stay: bool
    stay_price: int
    travel_time: int
    fromdate: datetime.date
    todate: datetime.date
    backdate: datetime.date
    


    class Config:
        from_attribute = True

# Dependency to get the database session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# FastAPI Routes
@app.post("/register/") #, response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print(locals())
    # Check if the user or email already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        print('existing_user')
        raise HTTPException(status_code=400, detail="Username already registered")
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_country = db.query(State).filter(State.country_name == user.country).first()
    if existing_country:
        print('existing_state')
    
    existing_state = db.query(State).filter(State.state_name == user.state).first()
    if not existing_state:
        new_state = State(
            state_name=user.state,
            country_name=user.country,
        
        )
        db.add(new_state)
        db.commit()
        db.refresh(new_state)
        existing_state = new_state
        
        
    existing_location= db.query(Location).filter(Location.location_name == user.location).first()
    if not existing_location:
        new_location = Location(
            location_name=user.location,
            state_id = existing_state.state_id
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        existing_location = new_location
        

    else:
        print('existing_state')

    
    # Hash the password before storing
    hashed_password = hash_password(user.password)
   # Create the user record in the database
    
    
    new_user = User(
        username=user.username,
        email=user.email,
        cryptkey=hashed_password,
        location_id=existing_location.location_id
       
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# FastAPI Routes
@app.post("/travel/")  # , response_model=UserResponse)
async def travel(travel: Travel, db: Session = Depends(get_db)):
    print(locals())
    # Check if the user or email already exists
    existing_user = db.query(User).filter(User.username_id == travel.username_id).first()
    start_location = location_add(location=travel.start_location, state=travel.start_location_state,country= travel.start_location_country, db=db)
    destination = location_add(location=travel.destination, state=travel.destination_state, country=travel.destination_country, db=db)
    new_Travel_data= TravelData(
        username_id=travel.username_id,
        start_location=start_location.location_id,
        destination=destination.location_id,
        travel_type=travel.travel_type,
        travel_price=travel.travel_price,
        days=travel.days,
        stay=travel.stay,
        stay_price=travel.stay_price,
        travel_time=travel.travel_time,
        fromdate=travel.fromdate,
        todate=travel.todate,
        backdate=travel.backdate
    )
    db.add(new_Travel_data)
    db.commit()
    db.refresh(new_Travel_data)
    


    return destination

def location_add(country: str, state: str, location: str, db: Session = Depends(get_db)):
    existing_country = db.query(State).filter(State.country_name == country).first()
    if existing_country:
        print('existing_state')
    
    existing_state = db.query(State).filter(State.state_name == state).first()
    if not existing_state:
        new_state = State(
            state_name=state,
            country_name=country,
        
        )
        db.add(new_state)
        db.commit()
        db.refresh(new_state)
        existing_state = new_state
    
    existing_location = db.query(Location).filter(Location.location_name == location).first()
    if not existing_location:
        new_location = Location(
            location_name=location,
            state_id=existing_state.state_id
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        existing_location = new_location
    
    
    else:
        print('existing_state')
    print(existing_location.location_id)
    return existing_location

@app.get("/user/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username_id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/pass/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username_id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.cryptkey


@app.get("/passcheck/{username, password}")
async def get_user(username: str, pasword: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(pasword, user.cryptkey):
        raise HTTPException(status_code=401, detail="Invalid password")
    return user.username

@app.get("/user/{password_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(username=user.username, password=user.password)
@app.put("/user/{user_id}/profile", response_model=UserResponse)
async def update_profile_pic(user_id: int, profile_pic: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # this area is untested 
    profile_pic_data = await profile_pic.read()
    user.profile_pic = profile_pic_data
    db.commit()
    db.refresh(user)
    
    return user

@app.get("/user/{user_id}/profile")
async def get_profile_pic(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    # Return the profile picture as a binary response
    if user.profile_pic:
        from fastapi.openapi.models import Response
        return Response(content=user.profile_pic, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Profile picture not found")
#area untested

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)