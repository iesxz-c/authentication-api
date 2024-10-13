from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    token_expire_minutes: int = 129600
 
    class Config:
        env_file = ".env"

settings = Settings()
# Import BaseSettings from Pydantic for settings management

# Define a Settings class that inherits from BaseSettings
# Declare a string attribute for the secret key
# Set a default value of 129600 minutes for token expiration (90 days)

# Inner configuration class for Pydantic settings
# Specify the .env file to load environment variables from

# Create an instance of the Settings class, loading values from the .env file
