from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db, engine
from models import Base
from schemas import DefectResponse
from crud import get_defect_status

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/status/{defect_id}", response_model=DefectResponse)
async def get_status(defect_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получает статус дефекта по его ID.
    """
    defect = await get_defect_status(db, defect_id)
    
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")

    return defect
