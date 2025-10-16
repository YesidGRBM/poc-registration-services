from typing import Literal
from datetime import datetime

from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from src.models import UserModel


class UserIn(BaseModel):
    document_type: Literal["CC", "CE", "PP"] = Field(..., min_length=2,max_length=3, alias="documentType")
    document_number: str = Field(..., min_length=5, max_length=15, alias="documentNumber")
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20, alias="phoneNumber")
    phone_indicative: Literal["57", "1"] = Field(..., min_length=2, max_length=3, alias="phoneIndicative")
    process_name: str = Field(..., min_length=2, max_length=100, alias="processName")
    entity: str = Field(..., max_length=2)

class Response(BaseModel):
    id: str

__ResponseUser = pydantic_model_creator(
    UserModel,
    name="ResponseUser",
    exclude=(
        "auto"
    ),
    model_config=ConfigDict(
        alias_generator=lambda string: "".join(word.capitalize() if i > 0 else word for i, word in enumerate(string.split('_'))),
        populate_by_name=True
    )
)

class ResponseUser(__ResponseUser):
    pass
