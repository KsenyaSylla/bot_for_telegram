from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db  # функция получения сессии
from api.models import MiniTest, MiniTestResponse

router = APIRouter()

@router.get("/mini_test/{id}", response_model=MiniTestResponse)
def get_mini_test_status(id: int, db: Session = Depends(get_db)):
    item = db.query(MiniTest).filter(MiniTest.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/test")
def test():
    return {"status":"work"}