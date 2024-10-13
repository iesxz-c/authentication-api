from fastapi import FastAPI
from app import models, auth, database

app = FastAPI()

# Include authentication-related routes
app.include_router(auth.router)

# Create the database tables
@app.on_event("startup")
def on_startup():
    models.SQLModel.metadata.create_all(database.engine)

# Simple health check route
@app.get("/")
def read_root():
    return {"message": "Hello Brother , ASALAM ALIKUM "}
