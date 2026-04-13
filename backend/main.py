from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import routers
from routes import product_new, ingredient, history

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="CheckKaro API",
    description="Indian product ingredient awareness platform",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_new.router, prefix="/api/product", tags=["Products"])
app.include_router(ingredient.router, prefix="/api/ingredient", tags=["Ingredients"])
app.include_router(history.router, prefix="/api/history", tags=["History"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "CheckKaro API"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CheckKaro API",
        "docs": "/docs",
        "health": "/health"
    }
if __name__ == "__main__":
    import uvicorn
    print("Total products loaded: 118")
    print("Starting CheckKaro API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)