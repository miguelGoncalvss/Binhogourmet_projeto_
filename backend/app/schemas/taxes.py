from pydantic import BaseModel, Field


class TaxSettingsIn(BaseModel):
    tipo_mei: str
    salario_minimo: float = Field(gt=0)
    inss_percent: float = Field(ge=0)
    iss: float = Field(ge=0)
    icms: float = Field(ge=0)
    faturamento_mensal: float = Field(ge=0)
    meses_no_ano: int = Field(gt=0)
    notes: str | None = None


class TaxSettingsOut(TaxSettingsIn):
    id: int

    class Config:
        from_attributes = True
