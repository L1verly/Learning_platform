""" File with settings and configs for the project """
from envparse import Env

env = Env()

APP_PORT: int = env.int("APP_PORT")

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5433/postgres",
)  # Connect string for the database

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5434/postgres_test",
)  # Connect string for the database


ACCESS_TOKE_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")

SENTRY_URL: str = env.str("SENTRY_URL")
