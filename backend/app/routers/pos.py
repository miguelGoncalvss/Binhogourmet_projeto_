from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.models import Ingredient, IngredientUnit, Order, OrderItem, Recipe, RecipeLine, Transaction, TransactionType
from app.routers.deps import get_current_user
from app.schemas.pos import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["pos"], dependencies=[Depends(get_current_user)])


def to_base_qty(unit: IngredientUnit, qty: float) -> float:
    if unit in {IngredientUnit.KG, IngredientUnit.L}:
        return qty * 1000
    return qty


def from_base_qty(unit: IngredientUnit, qty_base: float) -> float:
    if unit in {IngredientUnit.KG, IngredientUnit.L}:
        return qty_base / 1000
    return qty_base


@router.post("", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Pedido sem itens.")

    consumption_by_ingredient: dict[int, float] = defaultdict(float)

    for item in payload.items:
        recipe = (
            db.query(Recipe)
            .options(joinedload(Recipe.lines).joinedload(RecipeLine.ingredient))
            .get(item.recipe_id)
        )
        if not recipe:
            raise HTTPException(status_code=404, detail=f"Receita {item.recipe_id} não encontrada.")

        for line in recipe.lines:
            consumption_by_ingredient[line.ingredient_id] += line.qty * item.quantity

    for ingredient_id, needed_base_qty in consumption_by_ingredient.items():
        ingredient = db.query(Ingredient).get(ingredient_id)
        available_base_qty = to_base_qty(ingredient.unit, ingredient.quantity)
        if needed_base_qty > available_base_qty:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Estoque insuficiente: {ingredient.name} "
                    f"(precisa {round(needed_base_qty, 2)}{('g' if ingredient.unit in {IngredientUnit.KG, IngredientUnit.G} else 'ml' if ingredient.unit in {IngredientUnit.L, IngredientUnit.ML} else 'un')}, "
                    f"tem {round(available_base_qty, 2)}{('g' if ingredient.unit in {IngredientUnit.KG, IngredientUnit.G} else 'ml' if ingredient.unit in {IngredientUnit.L, IngredientUnit.ML} else 'un')})"
                ),
            )

    order_total = sum(item.quantity * item.unit_price for item in payload.items)
    order = Order(total_amount=order_total)
    db.add(order)
    db.flush()

    for item in payload.items:
        db.add(OrderItem(order_id=order.id, recipe_id=item.recipe_id, quantity=item.quantity, unit_price=item.unit_price))

    for ingredient_id, needed_base_qty in consumption_by_ingredient.items():
        ingredient = db.query(Ingredient).get(ingredient_id)
        ingredient.quantity -= from_base_qty(ingredient.unit, needed_base_qty)

    db.add(
        Transaction(
            description=f"Venda pedido #{order.id}",
            amount=order_total,
            type=TransactionType.INCOME,
        )
    )

    db.commit()
    db.refresh(order)
    return OrderOut(id=order.id, total_amount=order.total_amount)
