from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import MiniTest

# test
async def get_first_line(db: AsyncSession):
    result = await db.execute(select(MiniTest).limit(1))
    return result.scalars().first()