from fastapi import APIRouter
from backend.app.core.logging import get_logger
router=APIRouter(prefix="/home")
logger=get_logger();

@router.get("/")
def home():
    return {"message":"Welcome to the NextGen Bank API"}

@router.get("/check")
def check():
    return {"message":"api_endpoint_found"}