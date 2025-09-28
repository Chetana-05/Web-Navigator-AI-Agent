from __future__ import annotations

from typing import Any, Dict, List, Optional

from .ollama_client import OllamaClient, force_json


PLANNER_SYSTEM_PROMPT = (
	"You are a strict planning agent that outputs exactly one JSON object per reply. "
	"The JSON describes a single next ACTION to perform in a browser automation loop. "
	"No prose. No code fences. Only JSON.\n\n"
	"Schema:\n"
	"{\n"
	"  \"action\": one of [\"navigate\", \"type\", \"click\", \"wait\", \"extract\", \"finish\"],\n"
	"  \"target\": optional string (URL, selector, or hint),\n"
	"  \"value\": optional string (text to type, etc.),\n"
	"  \"details\": optional object with extra fields,\n"
	"  \"result\": when action=finish, object containing structured final data\n"
	"}\n\n"
	"Guidelines:\n"
	"- Start from a search engine query if not already on results. Prefer DuckDuckGo.\n"
	"- Use navigate to go to a URL or search engine.\n"
	"- Use type with a target selector for input fields; include value.\n"
	"- Use click with a target selector for buttons/links.\n"
	"- Use wait with details like {\"for\": \"network_idle\", \"seconds\": 1}.\n"
	"- Use extract to request specific data via selectors.\n"
	"- When the goal is satisfied, use finish with a compact result object.\n"
)


class Planner:
	def __init__(self, client: OllamaClient):
		self.client = client

	async def plan(self, goal: str, observation: Dict[str, Any]) -> Dict[str, Any]:
		messages = [
			{"role": "system", "content": PLANNER_SYSTEM_PROMPT},
			{
				"role": "user",
				"content": (
					f"Goal: {goal}\n"
					f"Observation: {observation}\n"
					"Respond with exactly one JSON object per the schema."
				),
			},
		]
		raw = await self.client.chat(messages)
		return force_json(raw)

