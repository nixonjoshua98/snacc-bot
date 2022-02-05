from src.models import BaseModel
from pydantic import Field


class ServerConfigModel(BaseModel):
    class Aliases:
        PREFIX = "prefix"
        SERVER_ID = "serverId"

    server_id: str = Field(..., alias=Aliases.SERVER_ID)
    prefix: str = Field("s!", alias=Aliases.PREFIX)
