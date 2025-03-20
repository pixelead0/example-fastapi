import logging
import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.core.config import get_settings
from src.core.exceptions import configure_exception_handlers
from src.product.router import router as product_router
from src.category.router import router as category_router

# Import models to register them with SQLAlchemy metadata
from src.product.models import Product, ProductCategory
from src.category.models import Category
from src.log.models import OperationLog

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Product Management API",
    description="API for managing products and categories",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"Request to {request.url.path} took {process_time:.4f} seconds")
    return response

# Configure exception handlers
configure_exception_handlers(app)

# Include routers with /api prefix
app.include_router(product_router, prefix="/api")
app.include_router(category_router, prefix="/api")

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Product Management API",
        "version": "0.1.0",
        "documentation": "/docs",
        "redoc": "/redoc",
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG) 