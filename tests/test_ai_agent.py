import os
import pytest
from src.ai_agent import AIAgent

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key provided")
def test_generate_insight_report():
    agent = AIAgent(api_key=os.getenv("OPENAI_API_KEY"))
    report = agent.generate_insight_report("Test summary for blockchain analysis")
    assert isinstance(report, str)
    assert len(report) > 0