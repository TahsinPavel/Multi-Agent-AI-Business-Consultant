"""Orchestrator for coordinating the domain-specific agents.

This module provides a small Orchestrator class that instantiates the
Market, Financial and Strategy agents and exposes helper methods to
process single-agent requests and a comprehensive consultation that
queries all agents and aggregates results.
"""
from typing import Dict
from .financial_analysis_agent import FinancialAnalysisAgent
from .market_analysis_agent import MarketAnalysisAgent
from .strategy_agent import StrategyAgent


class Orchestrator:
	def __init__(self, model: str = "gpt-3.5-turbo"):
		# Create agents; they will use the shared LLM adapter internally
		self.financial = FinancialAnalysisAgent(model=model)
		self.market = MarketAnalysisAgent(model=model)
		self.strategy = StrategyAgent(model=model)

	def process_request(self, agent_type: str, request: str) -> Dict[str, str]:
		"""Route a request to a specific agent and return its response."""
		agent_type = (agent_type or "").lower()
		if agent_type == "market":
			return {"agent": "market", "response": self.market.process_request(request)}
		elif agent_type == "financial":
			return {"agent": "financial", "response": self.financial.process_request(request)}
		elif agent_type == "strategy":
			return {"agent": "strategy", "response": self.strategy.process_request(request)}
		else:
			return {"error": f"Unknown agent type: {agent_type}"}

	def process_comprehensive_consultation(self, request: str) -> Dict[str, Dict[str, str]]:
		"""Run all agents and return their results in a dict.

		Returns a structure like:
		{
			"market": {"agent": "market", "response": "..."},
			"financial": { ... },
			"strategy": { ... }
		}
		"""
		results = {}
		results["market"] = {"agent": "market", "response": self.market.process_request(request)}
		results["financial"] = {"agent": "financial", "response": self.financial.process_request(request)}
		results["strategy"] = {"agent": "strategy", "response": self.strategy.process_request(request)}
		return results


# Expose a singleton orchestrator instance for simple scripts
def create_orchestrator(model: str = "gpt-3.5-turbo") -> Orchestrator:
	return Orchestrator(model=model)
