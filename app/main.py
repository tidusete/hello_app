from fastapi import FastAPI, Path, status, HTTPException
from fastapi.responses import JSONResponse
from datetime import date

from app.models import UserBirthdayRequest
from app.db import init_db_connection, upsert_user, get_user_birthdate

app = FastAPI()

@app.on_event("startup")
def startup_event() -> None:
    init_db_connection()

@app.put("/hello/{username}", status_code=status.HTTP_204_NO_CONTENT)
def save_birthday(
    username: str = Path(..., pattern="^[a-zA-Z]+$"),
    request: UserBirthdayRequest = ...
) -> None:
    username = username.lower()

    if request.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="Date of birth must be in the past")
    # TODO Implement Logger
    print(f"This is the user {username} and this is the date {request.dateOfBirth}")
    upsert_user(username, request.dateOfBirth)

@app.get("/hello/{username}")
def greet_user(
    username: str = Path(..., pattern="^[A-Za-z]+$")
) -> JSONResponse:
    lookup_username = username.lower()  
    display_name = username.capitalize()
    
    day_birthday = get_user_birthdate(lookup_username)
    if day_birthday is None:
        # TODO Implement Logger
        print(f"This user {lookup_username} does not exist on the DB")
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()
    next_birthday = day_birthday.replace(year=today.year)

    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    days_left = (next_birthday - today).days
    if days_left == 0:
        message = f"Hello, {display_name}! Happy birthday!"
    else:
        message = f"Hello, {display_name}! Your birthday is in {days_left} day(s)"

    return JSONResponse(content={"message": message})
