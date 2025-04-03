from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Defect

async def get_defect_status(db: AsyncSession, defect_id: int):
    result = await db.execute(select(Defect).where(Defect.defect == defect_id))
    return result.scalars().first()
