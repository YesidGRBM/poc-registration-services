from datetime import UTC, datetime

from tortoise import Model
from tortoise.fields import BooleanField, CharField, DatetimeField

class UserModel(Model):
    id = CharField(pk=True, max_length=22)
    document_type = CharField(max_length=3)
    document_number = CharField(max_length=15)
    email = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    phone_indicative = CharField(max_length=3)
    process_name = CharField(max_length=100)
    entity = CharField(max_length=2)
    auto = BooleanField(default=False)
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)
    deleted_at = DatetimeField(null=True)

    class Meta:
        table = "users"

    async def auto_delete(self, using_db=None, keep_parents=False):
        self.auto = True
        self.deleted_at = datetime.now(UTC)
        await self.save(update_fields=["deleted_at", "auto"])

    async def delete(self, using_db=None, keep_parents=False):
        self.deleted_at = datetime.now(UTC)
        await self.save(update_fields=["deleted_at"])
