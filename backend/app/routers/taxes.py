from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import TaxSettings
from app.routers.deps import get_current_user
from app.schemas.taxes import TaxSettingsIn, TaxSettingsOut

router = APIRouter(prefix="/taxes", tags=["taxes"], dependencies=[Depends(get_current_user)])


@router.get("/settings", response_model=TaxSettingsOut)
def get_taxes_settings(db: Session = Depends(get_db)):
    settings = db.query(TaxSettings).first()
    if not settings:
        settings = TaxSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.put("/settings", response_model=TaxSettingsOut)
def update_taxes_settings(payload: TaxSettingsIn, db: Session = Depends(get_db)):
    settings = db.query(TaxSettings).first()
    if not settings:
        settings = TaxSettings()
        db.add(settings)
    for field, value in payload.model_dump().items():
        setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return settings
