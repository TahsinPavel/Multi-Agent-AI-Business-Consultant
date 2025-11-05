from agents.orchestrator import create_orchestrator
import json

orc = create_orchestrator()
result = orc.process_comprehensive_consultation("Test business idea: local bakery expansion")
print(json.dumps(result, indent=2))
