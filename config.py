import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    token: str
    admin_ids: list[int]

adm_ids_str = os.getenv("ADMIN_IDS", "")

if adm_ids_str:
    adm_ids_list = [int(id.strip()) for id in adm_ids_str.split(",")]
else:
    adm_ids_list = []

config = Config(
    token = os.getenv("BOT_TOKEN"),
    admin_ids=adm_ids_list
)