from langgraph.types import Send

from src.chains import query_analysis_chain, summarizer_chain
from src.state import State
from src.utils import scrape_with_robots_check, search_google_custom


async def query_analysis_node(state: State):
    query_analysis_result = await query_analysis_chain.ainvoke(
        {"user_query": state.user_query}
    )
    print(query_analysis_result)
    return {"query_analysis": query_analysis_result}


def split_into_searches(state: State):
    queries = state.query_analysis.search_queries
    return [Send("search_and_scrape", {"search_query": q}) for q in queries]


def search_and_scrape(state: dict):
    search_query = state["search_query"]
    try:
        results = search_google_custom(
            topics=[search_query],
            filters={"language": "English", "region": "any", "timeframe": None},
        )
        top_sites = results[:2]
        scraped = []
        sources = []

        for site in top_sites:
            try:
                content = scrape_with_robots_check(site["url"])
                if content:
                    scraped.append({"url": site["url"], "content": content})
                    sources.append(site["url"])
            except Exception as e:
                print(f"Failed scraping {site['url']}: {e}")

        return {"scraped_contents": scraped, "sources": sources}

    except Exception as e:
        print(f"Search failed for query {search_query}: {e}")
        return {"scraped_contents": [], "sources": []}


async def summarizer_node(state: State):
    # Format the articles nicely
    articles_text = "\n\n".join(
        [
            f"Source: {article['url']}\nContent: {article['content']}"
            for article in state.scraped_contents
        ]
    )

    summarizer_result = await summarizer_chain.ainvoke(
        {"user_query": state.user_query, "articles": articles_text}
    )
    return {"summaries": summarizer_result.summary}
