from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Ingredient, IngredientUnit
from app.routers.deps import get_current_user
from app.schemas.inventory import IngredientCreate, IngredientOut, IngredientUpdate

router = APIRouter(prefix="/ingredients", tags=["ingredients"], dependencies=[Depends(get_current_user)])


def _parse_unit(unit: str) -> IngredientUnit:
    try:
        return IngredientUnit(unit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Unidade inválida. Use: kg, g, L, ml, un") from exc


@router.get("", response_model=list[IngredientOut])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).order_by(Ingredient.name.asc()).all()


@router.post("", response_model=IngredientOut)
def create_ingredient(payload: IngredientCreate, db: Session = Depends(get_db)):
    ingredient = Ingredient(**payload.model_dump(exclude={"unit"}), unit=_parse_unit(payload.unit))
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(ingredient_id: int, payload: IngredientUpdate, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).get(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")

    data = payload.model_dump()
    ingredient.unit = _parse_unit(data.pop("unit"))
    for field, value in data.items():
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).get(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado.")
    db.delete(ingredient)
    db.commit()
    return {"message": "Ingrediente removido."}
