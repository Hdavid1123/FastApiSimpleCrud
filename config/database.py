from sqlalchemy import create_engine, MetaData


DB_URL="postgresql://hdavid1123:hvarkaed13@localhost:5432/fastapicrud"

# Crear engine de conexión a la base de datos

engine = create_engine(DB_URL)

meta = MetaData()

conection = engine.connect()