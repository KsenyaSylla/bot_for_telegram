from pydantic import BaseModel

class DefectResponse(BaseModel):
    defect: int
    status: str

    class Config:
        from_attributes = True
