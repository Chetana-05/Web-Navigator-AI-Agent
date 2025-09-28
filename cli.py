from __future__ import annotations

import asyncio
from typing import Optional

import orjson
import typer
from rich import print

from .agent import Agent


app = typer.Typer(add_completion=False)


@app.command()
def main(
	goal: str = typer.Option(..., "--goal", help="Natural language instruction for the agent"),
	model: str = typer.Option("llama3.1", "--model", help="Ollama model name"),
	headless: bool = typer.Option(True, "--headless/--headed", help="Run browser headless"),
	max_steps: int = typer.Option(12, "--max-steps", min=1, max=50, help="Max planning steps"),
):
	async def run():
		agent = Agent(model=model, headless=headless, max_steps=max_steps)
		result = await agent.run(goal)
		print("[bold green]FINAL RESULT[/bold green]")
		print(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode())

	asyncio.run(run())


if __name__ == "__main__":
	app()
