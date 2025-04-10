import os

if os.getenv("ENV", "development") == "development":
    from dotenv import load_dotenv
    load_dotenv()

# Access values safely
DATABASE_URL: str = os.getenv("DATABASE_URL")
