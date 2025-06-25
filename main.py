from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="FBA Arbitrage Finder API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    title: str
    source_price: float
    amazon_price: float
    source_url: str
    amazon_url: str
    asin: Optional[str]
    estimated_profit: float
    roi_percentage: float
    created_at: datetime = datetime.now()

@app.get("/")
async def root():
    return {"message": "FBA Arbitrage Finder API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze-product")
async def analyze_product(url: str):
    try:
        # This will be implemented to analyze a specific product URL
        return {"message": "Product analysis endpoint"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profitable-products", response_model=List[Product])
async def get_profitable_products(
    min_roi: Optional[float] = 30.0,
    max_price: Optional[float] = 100.0
):
    try:
        # This will be implemented to return a list of profitable products
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 