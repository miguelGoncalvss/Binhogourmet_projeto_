from datetime import date

from pydantic import BaseModel, Field


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AccountOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TransactionIn(BaseModel):
    description: str
    amount: float = Field(gt=0)
    type: str
    date: date
    category_id: int | None = None
    account_id: int | None = None


class TransactionOut(TransactionIn):
    id: int

    class Config:
        from_attributes = True
