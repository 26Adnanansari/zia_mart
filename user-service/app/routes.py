import os
from PIL import Image
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlmodel import Session, select
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.database import get_session
from passlib.context import CryptContext

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Helper function to hash passwords
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/users/{user_id}/profile-picture")
def update_profile_picture(user_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    directory = "profile_pictures"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")

    file_location = f"{directory}/{user_id}_{file.filename}"
    print(f"Attempting to save file to: {file_location}")

    try:
        # Reset file pointer to the beginning before opening with Pillow
        file.file.seek(0)

        # Open the image to ensure it's valid
        image = Image.open(file.file)
        print(f"Image format: {image.format}, size: {image.size}, mode: {image.mode}")

        # Save the image
        image.save(file_location)
        print(f"File '{file_location}' saved successfully.")

        # Update user's profile picture path in the database
        user.profile_picture = file_location
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"User {user_id} profile picture updated successfully in the database.")
        return {"message": "Profile picture updated successfully"}

    except Exception as e:
        print(f"Failed to process image: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    session.add(user)
    session.commit()
    return {"message": "User account deactivated"}