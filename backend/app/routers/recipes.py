from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.models import Ingredient, IngredientUnit, Recipe, RecipeLine
from app.routers.deps import get_current_user
from app.schemas.recipes import RecipeCreate, RecipeOut, RecipePricingOut, RecipeUpdate

router = APIRouter(prefix="/recipes", tags=["recipes"], dependencies=[Depends(get_current_user)])


def unit_to_base_qty(unit: IngredientUnit, qty: float) -> float:
    if unit == IngredientUnit.KG:
        return qty * 1000
    if unit == IngredientUnit.L:
        return qty * 1000
    return qty


def unit_cost_to_base(unit: IngredientUnit, unit_cost: float) -> float:
    if unit in {IngredientUnit.KG, IngredientUnit.L}:
        return unit_cost / 1000
    return unit_cost


def pricing_summary(recipe: Recipe) -> RecipePricingOut:
    ingredients_total_batch = 0.0
    for line in recipe.lines:
        ingredient = line.ingredient
        ingredients_total_batch += line.qty * unit_cost_to_base(ingredient.unit, ingredient.unit_cost)

    ingredients_cost_per_unit = ingredients_total_batch / recipe.yield_units
    labor_cost_per_unit = ((recipe.labor_minutes_per_batch / 60) * recipe.labor_rate_per_hour) / recipe.yield_units
    total_cost_per_unit = (
        ingredients_cost_per_unit
        + labor_cost_per_unit
        + recipe.packaging_cost_per_unit
        + recipe.other_cost_per_unit
    )
    suggested_price = total_cost_per_unit * recipe.markup_multiplier
    margin = 0 if suggested_price == 0 else (suggested_price - total_cost_per_unit) / suggested_price

    return RecipePricingOut(
        recipe_id=recipe.id,
        product_name=recipe.product_name,
        ingredients_cost_per_unit=round(ingredients_cost_per_unit, 4),
        labor_cost_per_unit=round(labor_cost_per_unit, 4),
        total_cost_per_unit=round(total_cost_per_unit, 4),
        suggested_price=round(suggested_price, 4),
        margin=round(margin, 4),
    )


def _validate_line_compatibility(ingredient: Ingredient):
    if ingredient.unit not in {IngredientUnit.KG, IngredientUnit.G, IngredientUnit.L, IngredientUnit.ML, IngredientUnit.UN}:
        raise HTTPException(status_code=400, detail=f"Unidade do ingrediente {ingredient.name} não suportada.")


@router.get("", response_model=list[RecipeOut])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).options(joinedload(Recipe.lines)).all()


@router.post("", response_model=RecipeOut)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    recipe = Recipe(**payload.model_dump(exclude={"lines"}))
    for line in payload.lines:
        ingredient = db.query(Ingredient).get(line.ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=404, detail=f"Ingrediente {line.ingredient_id} não encontrado.")
        _validate_line_compatibility(ingredient)
        recipe.lines.append(RecipeLine(ingredient_id=line.ingredient_id, qty=line.qty))

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return db.query(Recipe).options(joinedload(Recipe.lines)).get(recipe.id)


@router.put("/{recipe_id}", response_model=RecipeOut)
def update_recipe(recipe_id: int, payload: RecipeUpdate, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).options(joinedload(Recipe.lines)).get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")

    for field, value in payload.model_dump(exclude={"lines"}).items():
        setattr(recipe, field, value)

    recipe.lines.clear()
    for line in payload.lines:
        ingredient = db.query(Ingredient).get(line.ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=404, detail=f"Ingrediente {line.ingredient_id} não encontrado.")
        recipe.lines.append(RecipeLine(ingredient_id=line.ingredient_id, qty=line.qty))

    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    db.delete(recipe)
    db.commit()
    return {"message": "Receita removida."}


@router.get("/{recipe_id}/pricing", response_model=RecipePricingOut)
def recipe_pricing(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).options(joinedload(Recipe.lines).joinedload(RecipeLine.ingredient)).get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return pricing_summary(recipe)
