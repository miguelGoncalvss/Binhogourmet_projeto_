from pydantic import BaseModel, Field


class RecipeLineIn(BaseModel):
    ingredient_id: int
    qty: float = Field(gt=0)


class RecipeLineOut(RecipeLineIn):
    id: int

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    product_name: str
    yield_units: float = Field(gt=0)
    packaging_cost_per_unit: float = Field(ge=0)
    labor_minutes_per_batch: float = Field(ge=0)
    labor_rate_per_hour: float = Field(ge=0)
    other_cost_per_unit: float = Field(ge=0)
    markup_multiplier: float = Field(gt=0)
    lines: list[RecipeLineIn]


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeOut(RecipeBase):
    id: int
    lines: list[RecipeLineOut]

    class Config:
        from_attributes = True


class RecipePricingOut(BaseModel):
    recipe_id: int
    product_name: str
    ingredients_cost_per_unit: float
    labor_cost_per_unit: float
    total_cost_per_unit: float
    suggested_price: float
    margin: float
