from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.models import Account, Category, Ingredient, IngredientUnit, TaxSettings, User


DEFAULT_CATEGORIES = ["Vendas", "Insumos", "Embalagens", "Operacional"]
DEFAULT_ACCOUNTS = ["Caixa", "Conta Bancária", "Cartão"]
DEFAULT_INGREDIENTS = [
    {"name": "Chocolate", "unit": IngredientUnit.KG, "quantity": 5, "unit_cost": 45.0},
    {"name": "Leite Condensado", "unit": IngredientUnit.UN, "quantity": 30, "unit_cost": 6.5},
    {"name": "Creme de Leite", "unit": IngredientUnit.UN, "quantity": 20, "unit_cost": 4.5},
]


def run_seed(db: Session) -> None:
    if not db.query(User).filter(User.email == "admin@binhogourmet.local").first():
        db.add(
            User(
                email="admin@binhogourmet.local",
                hashed_password=hash_password("admin123"),
                full_name="Administrador Binho Gourmet",
            )
        )

    for name in DEFAULT_CATEGORIES:
        if not db.query(Category).filter(Category.name == name).first():
            db.add(Category(name=name))

    for name in DEFAULT_ACCOUNTS:
        if not db.query(Account).filter(Account.name == name).first():
            db.add(Account(name=name))

    for item in DEFAULT_INGREDIENTS:
        if not db.query(Ingredient).filter(Ingredient.name == item["name"]).first():
            db.add(Ingredient(**item))

    if not db.query(TaxSettings).first():
        db.add(TaxSettings())

    db.commit()
