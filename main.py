from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.exception import (
    AppException,
    app_exception_handler,
)
from core.middleware import log_requests
from database import Base, engine
from limiter import limiter
from router import (
    auth,
    category,
    inventory_report,
    product,
    refresh_token,
    stock_movement,
    user,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StockFlow API project")

Instrumentator().instrument(app).expose(app)

app.middleware("http")(log_requests)

app.add_exception_handler(AppException, app_exception_handler)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(stock_movement.router)
app.include_router(refresh_token.router)
app.include_router(inventory_report.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "StockflowAPI Project"}
