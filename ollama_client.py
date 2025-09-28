from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class OllamaError(Exception):
	pass


class OllamaClient:
	"""Minimal async client for Ollama chat completions.

	- Uses streaming=false for simpler handling
	- Retries transient HTTP failures
	"""

	def __init__(
		self,
		base_url: str | None = None,
		model: str = "llama3.1",
		temperature: float = 0.2,
		max_tokens: Optional[int] = None,
		timeout_seconds: float = 120.0,
	):
		self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
		self.model = model
		self.temperature = temperature
		self.max_tokens = max_tokens
		self.timeout_seconds = timeout_seconds

	@retry(
		stop=stop_after_attempt(3),
		wait=wait_exponential(multiplier=1, min=1, max=10),
		retry=retry_if_exception_type((aiohttp.ClientError, OllamaError)),
	)
	async def chat(self, messages: List[Dict[str, Any]]) -> str:
		payload = {
			"model": self.model,
			"messages": messages,
			"stream": False,
			"options": {
				"temperature": self.temperature,
			}
		}
		if self.max_tokens is not None:
			payload["options"]["num_predict"] = self.max_tokens

		url = f"{self.base_url.rstrip('/')}/api/chat"
		async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout_seconds)) as session:
			async with session.post(url, json=payload) as resp:
				if resp.status != 200:
					raise OllamaError(f"Ollama HTTP {resp.status}: {await resp.text()}")
				data = await resp.json()
				message = data.get("message", {})
				content = message.get("content", "")
				return content


def force_json(text: str) -> Dict[str, Any]:
	"""Attempt to parse JSON from LLM output, with a simple fallback repair.

	This keeps logic lightweight for hackathon use.
	"""
	text = text.strip()
	# Try direct parse first
	try:
		return json.loads(text)
	except json.JSONDecodeError:
		pass

	# Heuristic: extract first {...} block
	start = text.find("{")
	end = text.rfind("}")
	if start != -1 and end != -1 and end > start:
		snippet = text[start : end + 1]
		try:
			return json.loads(snippet)
		except json.JSONDecodeError:
			pass

	# Last resort
	return {"error": "invalid_json", "raw": text}

