from src.models import BaseModel
from pydantic import Field
import datetime as dt


class UserEconomyProfile(BaseModel):

    class Aliases:
        USER_ID = "userId"
        CURRENCY = "totalCurrency"
        LAST_DAILY_CLAIM = "lastDailClaimTime"
        DAILY_STREAK = "dailyClaimStreak"

    user_id: str = Field(..., alias=Aliases.USER_ID)
    currency: int = Field(0, alias=Aliases.CURRENCY)
    last_daily_claim: dt.datetime = Field(None, alias=Aliases.LAST_DAILY_CLAIM)
    daily_streak: int = Field(0, alias=Aliases.DAILY_STREAK)
