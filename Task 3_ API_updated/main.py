# main.py
from fastapi import FastAPI
from mysql_crud_api import router as mysql_router
from mongodb_crud_api import router as mongo_router

app = FastAPI(title="Traffic Data API", version="1.0")
app.include_router(mysql_router)
app.include_router(mongo_router)

@app.get("/")
def root():
    return {"message": "Traffic Data API. Use /mysql or /mongo endpoints."}