from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import forms, queries

# Initialize FastAPI app
app = FastAPI()

# Mount static files for CSS, JS, and other assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers for modular routes
app.include_router(forms.router)
app.include_router(queries.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Forms Filler Web App!"}
