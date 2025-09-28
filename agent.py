from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from .ollama_client import OllamaClient
from .planner import Planner
from .browser import BrowserController
from . import extractors


class Agent:
	def __init__(
		self,
		model: str = "llama3.1",
		headless: bool = True,
		max_steps: int = 12,
	):
		self.client = OllamaClient(model=model)
		self.planner = Planner(self.client)
		self.browser = BrowserController(headless=headless)
		self.max_steps = max_steps

	async def run(self, goal: str) -> Dict[str, Any]:
		async with self.browser.session():
			all_products = []
			sites_to_visit = ["amazon.in", "flipkart.com"]
			
			for site in sites_to_visit:
				try:
					# Navigate to site
					if "amazon" in site:
						url = "https://www.amazon.in/s?k=laptops+under+50000"
						await self.browser.navigate(url)
					elif "flipkart" in site:
						url = "https://www.flipkart.com/search?q=laptops+under+50000"
						await self.browser.navigate(url)
					
					await self.browser.wait(3)
					
					# Extract products from current site
					if "amazon" in site:
						products = await extractors.extract_amazon_products(self.browser.page)
					elif "flipkart" in site:
						products = await extractors.extract_flipkart_products(self.browser.page)
					
					all_products.extend(products[:3])  # Top 3 from each site
					
				except Exception as e:
					print(f"Error on {site}: {e}")
					continue
			
			# Return consolidated results
			return {
				"status": "ok", 
				"result": {
					"goal": goal,
					"total_products": len(all_products),
					"products": all_products[:5],  # Top 5 overall
					"sites_visited": sites_to_visit
				}, 
				"steps": 1
			}
