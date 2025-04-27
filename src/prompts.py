"""Prompts used in this project."""

from langchain_core.prompts import PromptTemplate

QUERY_ANALYSIS_PROMPT = """
You are an expert digital research agent tasked with preparing research-ready search queries.

Given a user query, your responsibilities are:
1. **Understand and Analyze the Query**:
    - Classify the **Intent**: [Informational, Comparative, Exploratory, Analytical, Investigative, etc].
    - Identify the main **Topics** (technologies, organizations, people, events, etc.).
    - Extract the **Actions** the user wants (e.g., summarize, compare, list, extract).
    - Detect any **Timeframe** mentioned (e.g., "in 2024", "recent", "historical").
    - Classify the **Information Type** needed: [Factual, Opinion, Trend/Recent News, Historical, Comparative, Statistical].

2. **Plan Search Queries**:
    - Generate a **list of search queries** or phrases that would best find the needed information.
    - Recommend **Source Types** to prioritize (e.g., news articles, academic papers, technical blogs, forums).
    - Suggest any **Filters** (e.g., timeframe restrictions, language, specific regions) to refine the search.

INPUT USER QUERY: {user_query}
"""

query_analysis_prompt = PromptTemplate(
    template=QUERY_ANALYSIS_PROMPT, input_variables=["user_query"]
)

SUMMARIZER_PROMPT = """
You are a research assistant. Summarize the following articles that were scraped for a user query into a concise paragraph. Include quotes and references to the original sources (cite the URLs).

User Query:
{user_query}

Articles:
{articles}

Return a structured summary."""

summarizer_prompt = PromptTemplate(
    template=SUMMARIZER_PROMPT, input_variables=["user_query", "articles"]
)
