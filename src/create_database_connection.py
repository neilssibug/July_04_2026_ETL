# from sqlalchemy import create_engine

# engine = create_engine(
# "postgresql+psycopg2://postgres:secret@localhost: 5432/bootcamp"
# )

from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

def get_database_url() -> str:
    load_dotenv()

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    database = os.getenv("POSTGRES_DB", "default_dw")
    user = os.getenv("POSTGRES_USER", "default_admin")
    password = os.getenv("POSTGRES_PASSWORD", "default_pw")

    # print(f"{host} {port} {database} {user} {password}")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    get_database_url()
)

if engine:
    print("Database connection established successfully.")



if __name__ == "_main_":
    main()