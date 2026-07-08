from dotenv import load_dotenv
import os

load_dotenv()

api_url = os.getenv("API_URL")
db_password = os.getenv("POSTGRES_PASSWORD")

print(f"{api_url} {db_password}")
