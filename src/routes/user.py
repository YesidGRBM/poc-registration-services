import shortuuid
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from src.models import UserModel
from src.schemas.user import UserIn, Response, ResponseUser
from src.utils.deactivate_registry import auto_deactivate_registry

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("", response_model=Response)
async def create_user(user_in: UserIn, background_tasks: BackgroundTasks):
    user = UserModel(id=shortuuid.uuid(), **user_in.model_dump())
    await user.save()
    background_tasks.add_task(auto_deactivate_registry, user.id)
    return Response(id=user.id)


@user_router.get('/{id}', response_model=ResponseUser)
async def get_user(id: str):
    user = await UserModel.get_or_none(id=id, deleted_at=None)
    if user is None:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Not found element"
            }
        )
    await user.delete()
    return user

@user_router.get('/{id}/meta')
async def get_user_meta(id: str):
    user = await UserModel.get_or_none(id=id)
    if user is None:
        return {
            "process": "",
            "active": False
        }
    return {
        "process": user.process_name,
        "active": user.deleted_at == None
    }