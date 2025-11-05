from pathlib import Path
from .base_agent import BaseAgent


class StrategyAgent(BaseAgent):
	def __init__(self, model: str = "gpt-3.5-turbo"):
		super().__init__(name="strategy", model=model)
		prompts_dir = Path(__file__).parents[1] / "prompts"
		prompt_path = prompts_dir / "strategy_prompt.txt"
		try:
			self.template = prompt_path.read_text(encoding="utf-8")
		except Exception:
			self.template = "You are a business strategy expert. Analyze the following business request:\n\n{request}"

	def process_request(self, request: str) -> str:
		prompt = self.template.format(request=request)
		messages = [{"role": "user", "content": prompt}]
		return self._call_llm(messages)


if __name__ == "__main__":
	a = StrategyAgent()
	print(a.process_request("Test: growth strategy for a SaaS B2B startup."))
