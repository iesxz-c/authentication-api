from fastapi import FastAPI
from app import models, auth, database
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Include authentication-related routes
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
@app.on_event("startup")
def on_startup():
    models.SQLModel.metadata.create_all(database.engine)

# Simple health check route
@app.get("/")
def read_root():
    return {"message": "Hello Brother , ASALAM ALIKUM "}
