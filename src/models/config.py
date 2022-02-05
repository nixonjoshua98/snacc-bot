from pydantic import Field

from .basemodels import BaseModel
from .validators import SecondsTimeDelta


class MongoConfiguration(BaseModel):
    connection: str = Field("localhost", alias="ConnectionString")
    database_name: str = Field(..., alias="DatabaseName")


class LevelsConfiguration(BaseModel):
    min_exp: int = Field(..., alias="MinExp")
    max_exp: int = Field(..., alias="MaxExp")
    interval: SecondsTimeDelta = Field(..., alias="ExpInterval")


class EconomyConfiguration(BaseModel):
    base_daily_reward: int = Field(..., alias="BaseDailyLoginReward")


class CogConfiguration(BaseModel):
    levels: LevelsConfiguration = Field(..., alias="Levels")
    economy: EconomyConfiguration = Field(..., alias="Economy")


class BotConfiguration(BaseModel):
    bot_token: str = Field(..., alias="BotToken")
    launch_extensions: list[str] = Field([], alias="LaunchExtensions")

    invite_link: str = Field(..., alias="InviteLink")
    server_link: str = Field(..., alias="ServerLink")
    github_link: str = Field(..., alias="GitHubLink")

    mongo: MongoConfiguration = Field(..., alias="Mongo")
    cogs: CogConfiguration = Field(..., alias="CogConfigurations")