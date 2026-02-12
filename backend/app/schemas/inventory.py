from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    unit: str
    quantity: float = Field(gt=0)
    unit_cost: float = Field(gt=0)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientOut(IngredientBase):
    id: int

    class Config:
        from_attributes = True
