from fastapi import FastAPI
from models import User, Item
from router import user, product, auth
from database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0"
)


app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
