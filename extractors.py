from __future__ import annotations

from typing import Any, Dict, List

from playwright.async_api import Page


async def extract_search_results_duckduckgo(page: Page, limit: int = 5) -> List[Dict[str, str]]:
	# DuckDuckGo SERP layout is relatively stable and friendly
	results = []
	elements = await page.query_selector_all("#links .nrn-react-div div[data-nrn='result'] a[href]")
	for el in elements[:limit]:
		href = await el.get_attribute("href")
		title = (await el.inner_text()) or ""
		if href:
			results.append({"title": title.strip(), "url": href})
	return results


async def extract_generic_list(page: Page, item_selector: str, limit: int = 10) -> List[str]:
	items = await page.query_selector_all(item_selector)
	texts: List[str] = []
	for el in items[:limit]:
		text = await el.inner_text()
		if text:
			texts.append(text.strip())
	return texts


async def extract_amazon_products(page: Page, limit: int = 5) -> List[Dict[str, str]]:
	"""Extract laptop products from Amazon search results."""
	products = []
	
	# Try multiple selectors for Amazon containers
	selectors = [
		"[data-component-type='s-search-result']",
		".s-result-item",
		"[data-asin]",
		".s-widget-container"
	]
	
	containers = []
	for selector in selectors:
		containers = await page.query_selector_all(selector)
		if containers:
			break
	
	for container in containers[:limit]:
		try:
			# Product title - try multiple selectors
			title = "N/A"
			title_selectors = [
				"h2 a span",
				"h2 span",
				".s-size-mini .s-color-base",
				"[data-cy='title-recipe-title']",
				".a-size-medium"
			]
			for sel in title_selectors:
				title_el = await container.query_selector(sel)
				if title_el:
					title = await title_el.inner_text()
					if title and title.strip():
						break
			
			# Price - try multiple selectors
			price = "N/A"
			price_selectors = [
				".a-price-whole",
				".a-offscreen",
				".a-price-range",
				".a-price .a-offscreen",
				".a-price-symbol"
			]
			for sel in price_selectors:
				price_el = await container.query_selector(sel)
				if price_el:
					price = await price_el.inner_text()
					if price and price.strip():
						break
			
			# URL
			url = ""
			link_selectors = ["h2 a", "a[href*='/dp/']", ".s-link-style"]
			for sel in link_selectors:
				link_el = await container.query_selector(sel)
				if link_el:
					href = await link_el.get_attribute("href")
					if href:
						url = f"https://amazon.in{href}" if href.startswith("/") else href
						break
			
			if title != "N/A" and price != "N/A" and len(title) > 10:
				products.append({
					"title": title.strip(),
					"price": price.strip(),
					"rating": "N/A",
					"url": url,
					"site": "Amazon"
				})
		except Exception as e:
			continue
	
	return products


async def extract_flipkart_products(page: Page, limit: int = 5) -> List[Dict[str, str]]:
	"""Extract laptop products from Flipkart search results."""
	products = []
	
	# Try multiple selectors for Flipkart containers
	selectors = [
		"[data-id]",
		"._1AtVbE",
		"._13oc-S",
		"div[data-id]"
	]
	
	containers = []
	for selector in selectors:
		containers = await page.query_selector_all(selector)
		if containers:
			break
	
	for container in containers[:limit]:
		try:
			# Product title - try multiple selectors
			title = "N/A"
			title_selectors = [
				"a[title]",
				"._4rR01T",
				".s1Q9rs",
				"._2mylT6",
				".IRpwTa"
			]
			for sel in title_selectors:
				title_el = await container.query_selector(sel)
				if title_el:
					title = await title_el.inner_text()
					if title and title.strip():
						break
			
			# Price - try multiple selectors
			price = "N/A"
			price_selectors = [
				"._30jeq3",
				"._1_WHN1",
				"._25b18c",
				"[class*='_30jeq3']"
			]
			for sel in price_selectors:
				price_el = await container.query_selector(sel)
				if price_el:
					price = await price_el.inner_text()
					if price and price.strip():
						break
			
			# URL
			url = ""
			link_selectors = ["a[href*='/p/']", "a[title]", "a"]
			for sel in link_selectors:
				link_el = await container.query_selector(sel)
				if link_el:
					href = await link_el.get_attribute("href")
					if href:
						url = f"https://flipkart.com{href}" if href.startswith("/") else href
						break
			
			if title != "N/A" and price != "N/A" and len(title) > 10:
				products.append({
					"title": title.strip(),
					"price": price.strip(),
					"rating": "N/A",
					"url": url,
					"site": "Flipkart"
				})
		except Exception as e:
			continue
	
	return products
