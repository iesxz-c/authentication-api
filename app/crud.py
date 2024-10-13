from sqlmodel import Session, select
from app.models import User

def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Import Session and select from SQLModel
# Import the User model from app.models

# Function to get a user by username
# Create a SELECT statement to find the user
# Execute the statement and return the first result

# Function to create a new user
# Add the user to the session
# Commit the session to save changes to the database
# Refresh the user object with updated attributes from the database
# Return the created user object
