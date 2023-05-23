from pydantic import BaseModel

class Purchase(BaseModel):
    user_id: int
    product_id: int
    Num_products: int
