import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str | None
    jwt_secret: str
    jwt_expire_minutes: int
    backend_cors_origins: str

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return "sqlite:///./dev.db"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


settings = Settings(
    database_url=os.getenv("DATABASE_URL"),
    jwt_secret=os.getenv("JWT_SECRET", "dev-secret"),
    jwt_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "1440")),
    backend_cors_origins=os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://frontend:3000"),
)
