from pydantic import BaseModel, Field


class OrderItemIn(BaseModel):
    recipe_id: int
    quantity: float = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderCreate(BaseModel):
    items: list[OrderItemIn]


class OrderOut(BaseModel):
    id: int
    total_amount: float


class OrderItemOut(BaseModel):
    id: int
    recipe_id: int
    quantity: float
    unit_price: float

    class Config:
        from_attributes = True
