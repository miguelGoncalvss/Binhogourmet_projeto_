from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Account, Category, Transaction, TransactionType
from app.routers.deps import get_current_user
from app.schemas.finance import AccountOut, CategoryOut, TransactionIn, TransactionOut

router = APIRouter(tags=["finance"], dependencies=[Depends(get_current_user)])


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name.asc()).all()


@router.get("/accounts", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(Account).order_by(Account.name.asc()).all()


@router.get("/transactions", response_model=list[TransactionOut])
def list_transactions(
    days: int | None = Query(default=None, description="Use 7 ou 30 para filtro rápido"),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if days:
        start = date.today() - timedelta(days=days)
        query = query.filter(Transaction.date >= start)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    return query.order_by(Transaction.date.desc()).all()


@router.post("/transactions", response_model=TransactionOut)
def create_transaction(payload: TransactionIn, db: Session = Depends(get_db)):
    try:
        tx_type = TransactionType(payload.type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Tipo inválido. Use income ou expense") from exc

    tx = Transaction(**payload.model_dump(exclude={"type"}), type=tx_type)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx
