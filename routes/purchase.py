from fastapi import APIRouter, HTTPException
from schemas.purchase import Purchase
from models.purchase import purchases
from models.user import users
from models.product import products
from config.database import conection

router = APIRouter()

@router.post("/purchases", tags=["purchases"], response_model=Purchase, description="Create a new purchase")
def create_purchase(purchase: Purchase):
    user_query = users.select().where(users.c.id == purchase.usuario_id)
    user_result = conection.execute(user_query).fetchone()
    if user_result is None:
        raise HTTPException(status_code=404, detail="User not found")

    product_query = products.select().where(products.c.id == purchase.producto_id)
    product_result = conection.execute(product_query).fetchone()
    if product_result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Save the purchase
    purchase_data = {
        "usuario_id": purchase.user_id,
        "producto_id": purchase.product_id,
        "total_productos": purchase.Num_products
    }
    result = conection.execute(purchases.insert().values(purchase_data))
    
    purchase_id = result.lastrowid
    purchase_data["id"] = purchase_id
    
    return Purchase(**purchase_data)

routes = router.routes