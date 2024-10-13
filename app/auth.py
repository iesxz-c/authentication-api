from fastapi import APIRouter, Depends, HTTPException  
from app import models, schemas, crud, database
from jose import jwt, JWTError
from datetime import datetime, timedelta  # Import datetime utilities
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer  # Import OAuth2PasswordBearer for token handling
import bcrypt

router = APIRouter()  # Create a new APIRouter instance for handling routes

SECRET_KEY = "your_secret_key"  # Define the secret key for JWT encoding
ALGORITHM = "HS256"  # Specify the algorithm used for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Set the default expiration time for access tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Set up OAuth2 password bearer scheme

def create_access_token(data: dict, expires_delta: timedelta = None):  # Function to create a JWT access token
    to_encode = data.copy()  # Make a copy of the data to include in the token
    if expires_delta:  # Check if a custom expiration time is provided
        expire = datetime.utcnow() + expires_delta  # Set expiration time based on provided delta
    else:  # Use default expiration time
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Add expiration time to the token data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the JWT with the secret key
    return encoded_jwt  # Return the encoded JWT

# Function to hash a password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Hash the password and return it

# Function to verify a plain password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))  # Return True if the password matches

# Function to get the current user based on the provided JWT token
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(database.get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the JWT to get the payload
        username: str = payload.get("sub")  # Extract the username from the payload
        if username is None:  # Check if the username is present
            raise HTTPException(status_code=401, detail="Invalid token")  # Raise an error if the token is invalid
        user = crud.get_user_by_username(session, username)  # Retrieve the user from the database
        if user is None:  # Check if the user exists
            raise HTTPException(status_code=401, detail="User not found")  # Raise an error if user not found
        return user  # Return the current user
    except JWTError:  # Handle JWT decoding errors
        raise HTTPException(status_code=401, detail="Invalid token")  # Raise an error for invalid token

# Register route to create a new user
@router.post("/register/", response_model=schemas.UserCreate)
def register(user: schemas.UserCreate, session: Session = Depends(database.get_session)):
    existing_user = crud.get_user_by_username(session, user.username)  # Check if the username is already taken
    if existing_user:  # If the username exists
        raise HTTPException(status_code=400, detail="Username already taken")  # Raise an error
    hashed_password = hash_password(user.password)  # Hash the user's password
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)  # Create a new user model
    crud.create_user(session, new_user)  # Save the new user to the database
    return new_user  # Return the newly created user

# Login route to authenticate a user
@router.post("/login/")
def login(user: schemas.UserLogin, session: Session = Depends(database.get_session)):
    db_user = crud.get_user_by_username(session, user.username)  # Retrieve the user by username
    if not db_user or not verify_password(user.password, db_user.hashed_password):  # Check for invalid credentials
        raise HTTPException(status_code=401, detail="Invalid credentials")  # Raise an error if credentials are invalid
    access_token = create_access_token(data={"sub": db_user.username})  # Create an access token for the user
    return {"access_token": access_token, "token_type": "bearer"}  # Return the access token

# Protected route to get the current user's details
@router.get("/users/me/")
def read_users_me(current_user: models.User = Depends(get_current_user)):  # Get the current user
    return current_user  # Return the current user's details
