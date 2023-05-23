from fastapi import APIRouter, Response
from config.database import conection
from models.user import users
from schemas.user import User
from typing import List
from starlette.status import HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet

router = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

@router.get(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get a list of all users")
def get_users():
    query = users.select()
    result = conection.execute(query).fetchall()
    user_list = [User(id=row.id, name=row.name, email=row.email, password=row.password) for row in result]
    return user_list


@router.get(
    "/users/{id}",
    tags=["users"],
    response_model=User,
    description="Get a single user by Id",)
def get_user(id: int):
    query = users.select().where(users.c.id == id)
    result = conection.execute(query).fetchone()

    if result is None:
        return Response(status_code=404)
    else:
        user = User(id=result.id, name=result.name, email=result.email, password=result.password)
        return user


@router.post("/users", tags=["users"], response_model=User, description="Create a new user")
def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email,
    }
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conection.execute(users.insert().values(new_user))
    
    user_id = result.lastrowid
    print(user_id)

    new_user["id"] = user_id
    return User(**new_user)


@router.put(
    "/users/{id}", tags=["users"], response_model=User, description="Update a User by Id")
def update_user(user: User, id: int):
    conection.execute(
        users.update()
        .values(name=user.name, email=user.email, password=user.password)
        .where(users.c.id == id))
    
    update_user = conection.execute(users.select().where(users.c.id == id)).fetchone()
    
    if update_user is None:
            return Response(status_code=404)
    else:
            update_user_dict = dict(update_user)
            return User(**update_user_dict)
    

@router.delete("/users/{id}", tags=["users"], status_code=HTTP_204_NO_CONTENT)
def delete_user(id: int):
    conection.execute(users.delete().where(users.c.id == id))
    return conection.execute(users.select().where(users.c.id == id)).first()

routes = router.routes