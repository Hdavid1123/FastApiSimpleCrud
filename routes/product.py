from fastapi import APIRouter, Response
from config.database import conection
from models.product import products
from schemas.product import Product
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import func, select

from cryptography.fernet import Fernet

router = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


@router.get(
    "/products",
    tags=["products"],
    response_model=List[Product],
    description="Get a list of all products",)
def get_products():
    query = products.select()
    result = conection.execute(query).fetchall()
    product_list = [Product(id=row.id, name=row.name, price=row.price, imageUrl=row.imageUrl) for row in result]
    return product_list

@router.get(
    "/products/{id}",
    tags=["products"],
    response_model=Product,
    description="Get a single products by Id",)
def get_product(id: int):
    query = products.select().where(products.c.id == id)
    result = conection.execute(query).fetchone()

    if result is None:
        return Response(status_code=404)
    else:
        user = Product(id=result.id, name=result.name, price=result.price, imageUrl=result.imageUrl)
        return user


@router.post("/", tags=["products"], response_model=Product, description="Create a new product")
def create_product(product: Product):
    new_product = {"name": product.name, "price": product.price, "imageUrl": product.imageUrl}
    
    result = conection.execute(products.insert().values(new_product))
    return conection.execute(products.select().where(products.c.id == result.lastrowid)).first()
def create_product(product: Product):
    new_product = {
        "name": product.name,
        "price": product.price,
        "imageUrl": product.imageUrl,
    }
    
    result = conection.execute(products.insert().values(new_product))
    
    user_id = result.lastrowid
    print(user_id)

    new_product["id"] = user_id
    return Product(**new_product)


@router.put(
    "products/{id}", tags=["products"], response_model=Product, description="Update a Product by Id"
)
def update_product(product: Product, id: int):
    conection.execute(
        products.update()
        .values(name=product.name, price=product.price, imageUrl=product.imageUrl)
        .where(products.c.id == id)
    )
    return conection.execute(products.select().where(products.c.id == id)).first()


@router.delete("/{id}", tags=["products"], status_code=HTTP_204_NO_CONTENT)
def delete_product(id: int):
    conection.execute(products.delete().where(products.c.id == id))
    return conection.execute(products.select().where(products.c.id == id)).first()

routes = router.routes