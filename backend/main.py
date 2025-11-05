from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

app = FastAPI(
    title="Multi-Agent AI Business Consultant",
    description="A multi-agent system for business consulting",
    version="1.0.0"
)

# Initialize the agent orchestrator
from agents.orchestrator import create_orchestrator

# Create a module-level orchestrator instance used by the API endpoints.
# This keeps examples simple; production use should inject dependencies / configure properly.
orchestrator = create_orchestrator()

class BusinessRequest(BaseModel):
    request: str

class ComprehensiveRequest(BaseModel):
    request: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Agent AI Business Consultant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/consult/market")
async def market_consultation(request: BusinessRequest):
    """Get market analysis for a business request"""
    result = orchestrator.process_request("market", request.request)
    return result

@app.post("/consult/financial")
async def financial_consultation(request: BusinessRequest):
    """Get financial analysis for a business request"""
    result = orchestrator.process_request("financial", request.request)
    return result

@app.post("/consult/strategy")
async def strategy_consultation(request: BusinessRequest):
    """Get strategic guidance for a business request"""
    result = orchestrator.process_request("strategy", request.request)
    return result

@app.post("/consult/comprehensive")
async def comprehensive_consultation(request: ComprehensiveRequest):
    """Get comprehensive business consultation using all agents"""
    results = orchestrator.process_comprehensive_consultation(request.request)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)