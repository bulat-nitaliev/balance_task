from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    balance: float = Field(..., ge=0)


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    balance: float

    class Config:
        orm_mode = True


class TransferRequest(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    amount: float = Field(..., gt=0)


class TransferResponse(BaseModel):
    message: str
    from_user_balance: float
    to_user_balance: float
