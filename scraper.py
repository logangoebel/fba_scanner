import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict, Optional
import re
import json
from amazon_paapi5_python_sdk import DefaultApi as AmazonAPI
import os
from dotenv import load_dotenv

load_dotenv()

class ProductScraper:
    def __init__(self):
        self.setup_amazon_client()
        self.setup_selenium()

    def setup_amazon_client(self):
        self.amazon = AmazonAPI(
            os.getenv('AMAZON_ACCESS_KEY'),
            os.getenv('AMAZON_SECRET_KEY'),
            os.getenv('AMAZON_PARTNER_TAG'),
            os.getenv('AMAZON_PARTNER_TYPE', 'Associates'),
            os.getenv('AMAZON_MARKETPLACE', 'US'),
            throttling=0.9
        )

    def setup_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def get_amazon_product_data(self, asin: str) -> Dict:
        try:
            response = self.amazon.get_items(asin)
            if response.items:
                item = response.items[0]
                return {
                    "title": item.item_info.title.display_value,
                    "price": float(item.offers.listings[0].price.amount),
                    "url": item.detail_page_url,
                    "asin": item.asin
                }
        except Exception as e:
            print(f"Error fetching Amazon product data: {e}")
            return None

    def calculate_fba_fees(self, price: float, weight: float, dimensions: Dict) -> float:
        # Basic FBA fee calculation (simplified version)
        # You should implement a more detailed calculation based on 
        # Amazon's fee structure and product category
        base_fee = 2.41  # Basic fulfillment fee
        weight_fee = weight * 0.40  # $0.40 per pound
        return base_fee + weight_fee

    def calculate_profit_margins(
        self,
        source_price: float,
        amazon_price: float,
        weight: float = 1.0,
        dimensions: Optional[Dict] = None
    ) -> Dict:
        if dimensions is None:
            dimensions = {"length": 10, "width": 10, "height": 5}

        fba_fees = self.calculate_fba_fees(amazon_price, weight, dimensions)
        
        # Calculate costs and profits
        total_cost = source_price + fba_fees
        profit = amazon_price - total_cost
        roi = (profit / total_cost) * 100

        return {
            "source_price": source_price,
            "amazon_price": amazon_price,
            "fba_fees": fba_fees,
            "total_cost": total_cost,
            "profit": profit,
            "roi_percentage": roi
        }

    def analyze_product_url(self, url: str) -> Dict:
        try:
            # Add specific scraping logic for different sources
            # This is a placeholder that should be implemented based on
            # the specific websites you want to scrape
            return {
                "title": "Sample Product",
                "source_price": 19.99,
                "source_url": url,
                "weight": 1.0,
                "dimensions": {
                    "length": 10,
                    "width": 10,
                    "height": 5
                }
            }
        except Exception as e:
            print(f"Error analyzing product URL: {e}")
            return None

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit() 