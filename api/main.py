from fastapi import FastAPI, Depends, HTTPException
import asyncio
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db, engine #test_connection #
from models import Base
from schemas import DefectResponse
from crud import get_defect_status


app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")

""" @app.get("/")
def read_root():
    return {"result": test_connection()}
""" 
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/status/{defect_id}", response_model=DefectResponse)
async def get_status(defect_id: int, db: AsyncSession = Depends(get_db)):
 
    defect = await get_defect_status(db, defect_id)
    
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")

    return defect
