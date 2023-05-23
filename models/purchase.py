from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import meta, engine

purchases = Table("purchases",meta,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("product_id", Integer),
    Column("Num_products", Integer),
)

meta.create_all(engine)