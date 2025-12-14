import random
from dataclasses import dataclass
from database.db import db_client


@dataclass
class Result:
    usr: str

class BeService:
    async def open_box(self, user_id: int, box_id: str) -> str | Result:

        return Result(
            user="123",
        )

besmart_service = BeService()