from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from playwright.async_api import async_playwright, Page, Browser


class BrowserController:
	def __init__(self, headless: bool = True):
		self.headless = headless
		self._browser: Optional[Browser] = None
		self._page: Optional[Page] = None

	@asynccontextmanager
	async def session(self):
		async with async_playwright() as p:
			browser = await p.chromium.launch(headless=self.headless)
			page = await browser.new_page()
			self._browser = browser
			self._page = page
			try:
				yield self
			finally:
				await page.close()
				await browser.close()

	@property
	def page(self) -> Page:
		assert self._page is not None, "Browser session not started"
		return self._page

	async def navigate(self, url: str):
		await self.page.goto(url, wait_until="domcontentloaded")

	async def type_text(self, selector: str, value: str, press_enter: bool = False):
		await self.page.fill(selector, value)
		if press_enter:
			await self.page.keyboard.press("Enter")

	async def click(self, selector: str):
		await self.page.click(selector)

	async def wait(self, seconds: float = 1.0):
		await self.page.wait_for_timeout(int(seconds * 1000))

	async def get_observation(self, max_text_len: int = 5000) -> Dict[str, Any]:
		title = await self.page.title()
		url = self.page.url
		# Extract visible text snippet for planner context
		content = await self.page.content()
		text = await self.page.evaluate("() => document.body.innerText.slice(0, 10000)")
		if text and len(text) > max_text_len:
			text = text[:max_text_len]
		return {"title": title, "url": url, "text": text}

