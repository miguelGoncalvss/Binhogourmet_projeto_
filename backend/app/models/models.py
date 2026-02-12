from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class IngredientUnit(str, Enum):
    KG = "kg"
    G = "g"
    L = "L"
    ML = "ml"
    UN = "un"


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), default="Administrador")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    unit: Mapped[IngredientUnit] = mapped_column(SQLEnum(IngredientUnit), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(140), nullable=False)
    yield_units: Mapped[float] = mapped_column(Float, nullable=False)
    packaging_cost_per_unit: Mapped[float] = mapped_column(Float, default=0)
    labor_minutes_per_batch: Mapped[float] = mapped_column(Float, default=0)
    labor_rate_per_hour: Mapped[float] = mapped_column(Float, default=0)
    other_cost_per_unit: Mapped[float] = mapped_column(Float, default=0)
    markup_multiplier: Mapped[float] = mapped_column(Float, default=2)

    lines: Mapped[list["RecipeLine"]] = relationship(
        "RecipeLine", back_populates="recipe", cascade="all, delete-orphan"
    )


class RecipeLine(Base):
    __tablename__ = "recipe_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), nullable=False)
    qty: Mapped[float] = mapped_column(Float, nullable=False)

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="lines")
    ingredient: Mapped[Ingredient] = relationship("Ingredient")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"), nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped[Order] = relationship("Order", back_populates="items")


class TaxSettings(Base):
    __tablename__ = "tax_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    tipo_mei: Mapped[str] = mapped_column(String(100), default="comercio")
    salario_minimo: Mapped[float] = mapped_column(Float, default=1412)
    inss_percent: Mapped[float] = mapped_column(Float, default=5)
    iss: Mapped[float] = mapped_column(Float, default=0)
    icms: Mapped[float] = mapped_column(Float, default=1)
    faturamento_mensal: Mapped[float] = mapped_column(Float, default=0)
    meses_no_ano: Mapped[int] = mapped_column(Integer, default=12)
    notes: Mapped[str | None] = mapped_column(Text)
