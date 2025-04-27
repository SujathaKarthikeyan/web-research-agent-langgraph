import pytest
from langsmith import unit
from src.graph import graph


@pytest.mark.asyncio
@unit
async def test_researcher_graph_basic_run() -> None:
    res = await graph.ainvoke(
        {
            "user_query": "Who founded OpenAI and what products have they released?",
        }
    )

    assert res is not None
    assert "summaries" in res

    summary_text = res["summaries"].lower()
    assert any(
        keyword in summary_text
        for keyword in ["openai", "gpt", "sam altman", "chatgpt"]
    )


@pytest.mark.asyncio
@unit
async def test_researcher_handles_multiple_searches() -> None:
    res = await graph.ainvoke(
        {
            "user_query": "Top AI research labs and their contributions in 2024",
        }
    )

    assert res is not None
    assert "summaries" in res
    assert isinstance(res["summaries"], str)

    summary_text = res["summaries"].lower()
    assert any(
        keyword in summary_text
        for keyword in [
            "openai",
            "deepmind",
            "anthropic",
            "meta",
            "mistral",
            "stanford",
        ]
    )
