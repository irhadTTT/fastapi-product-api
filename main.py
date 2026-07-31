from fastapi import FastAPI
from models.user import User
from models.product import Item
from router import user, product, auth, category
from database import Base, engine
from fastapi.staticfiles import StaticFiles



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0"
)


app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(category.router)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "FastAPI Product API"
    }