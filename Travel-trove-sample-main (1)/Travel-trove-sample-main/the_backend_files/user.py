from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy import  Column, String, Integer, LargeBinary, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from passlib.context import CryptContext
from models import User  
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
    username_id: int

class UserResponse(BaseModel):
    username_id: int
    username: str
    email: str
   

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
@app.post("/register/", response_model=UserResponse)
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
    
    # Hash the password before storing
    hashed_password = hash_password(user.password)
   # Create the user record in the database
    new_user = User(
        username=user.username,
        email=user.email,
        cryptkey=hashed_password,
       
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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
        return Response(content=user.profile_pic, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Profile picture not found")
#area untested

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
