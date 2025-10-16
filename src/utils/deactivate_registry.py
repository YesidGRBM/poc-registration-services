import asyncio
from src.models import UserModel

async def auto_deactivate_registry(id: str):
    await asyncio.sleep(300)
    user = await UserModel.get_or_none(id=id)
    if user and user.auto == False:
        await user.auto_delete()
