from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from database import get_db
from routers.auth import get_current_user, get_user_exception, get_password_hash, verify_password
from utils.common_responses import successful_response
import models

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {
            "description": "User not found."
        }
    }
)


class User(BaseModel):
    username: str
    email: Optional[str] = Field()
    first_name: str
    last_name: str
    phone_number: str
    hashed_password: Optional[str]
    is_active: bool


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


@router.get("/")
async def read_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{username}")
async def read_by_username(username: str, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.username == username).first()

    if user_model is None:
        raise user_not_found_exception()

    return user_model


@router.get("/by_name/")
async def read_by_name(first_name: str,
                       last_name: str,
                       db: Session = Depends(get_db)):

    user_model = db.query(models.Users)\
        .filter(models.Users.first_name == first_name, models.Users.last_name == last_name)\
        .first()

    if user_model is None:
        raise user_not_found_exception()

    user = User(
        username=user_model.username,
        email=user_model.email,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        phone_number=user_model.phone_number,
        is_active=user_model.is_active
    )

    user = user.dict(exclude={'hashed_password'})

    return user


@router.put("/password")
async def update_user_password(change_password: ChangePassword,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):

    if change_password.new_password.replace(" ", "") == "" \
            or change_password.new_password.replace(" ", "") == "":
        raise HTTPException(status_code=400, detail="Password is required.")

    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get("id"))\
        .first()

    if user_model is None:
        raise user_not_found_exception()

    if not verify_password(change_password.current_password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="current_password do not mach current password.")

    user_model.hashed_password = get_password_hash(change_password.new_password)

    db.add(user_model)
    db.commit()

    return successful_response(200)


@router.delete("/{username}")
async def delete_user(username: str,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get("id"), models.Users.username == username)\
        .first()

    if user_model is None:
        raise user_not_found_exception()

    todo_counts = db.query(models.Todos) \
        .filter(models.Todos.owner_id == user.get("id")) \
        .count()

    if todo_counts > 0:
        raise HTTPException(status_code=400,
                            detail="There are Todos linked to this user. "
                                   "First remove the todos and then delete the user.")

    db.query(models.Users)\
        .filter(models.Users.id == user.get("id"))\
        .delete()

    db.commit()

    return successful_response(200)


def user_not_found_exception():
    return HTTPException(status_code=404, detail="User not found.")

