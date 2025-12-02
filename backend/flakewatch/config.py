import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://flakewatch:flakewatch@db:5432/flakewatch")
