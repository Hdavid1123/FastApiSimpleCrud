from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import meta, engine

products = Table("products",meta,
    Column("id", Integer, primary_key=True),
    Column(
        "name",
        String(255),
    ),
    Column("price", String(255)),
    Column("imageUrl", String(255)),
)

meta.create_all(engine)