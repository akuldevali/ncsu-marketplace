from fastapi import FastAPI
from controller import router
from database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NCSU Marketplace - Messaging Service", version="1.0.0")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "NCSU Marketplace Messaging Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}