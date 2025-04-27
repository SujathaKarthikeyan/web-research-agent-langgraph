from pydantic import BaseModel, Field
from typing import Optional, List


class Filters(BaseModel):
    timeframe: Optional[str] = Field(
        description="Time-based filter for search results (e.g., 'past year', '2024', 'none').",
    )
    language: Optional[str] = Field(
        description="Language preference for search results (e.g., 'English', 'Spanish', 'any').",
    )
    region: Optional[str] = Field(
        description="Geographic region filter for search results (e.g., 'United States', 'Europe', 'any').",
    )


class QueryAnalysisOutput(BaseModel):
    intent: str = Field(
        ...,
        description="The primary intent of the user query (e.g., Informational, Comparative, Exploratory, Analytical, Investigative).",
    )
    topics: List[str] = Field(
        ...,
        description="Main topics mentioned in the query (e.g., technologies, organizations, people, events).",
    )
    actions: List[str] = Field(
        ...,
        description="Specific actions the user wants to perform (e.g., summarize, compare, list, extract).",
    )
    timeframe: Optional[str] = Field(
        description="Timeframe referenced in the query, or 'not specified' if none is mentioned.",
    )
    info_type: str = Field(
        ...,
        description="Type of information needed (e.g., Factual, Opinion, Trend/Recent News, Historical, Comparative, Statistical).",
    )
    search_queries: List[str] = Field(
        ...,
        description="Maximum of 2 Generated search queries to find relevant information.",
    )
    target_sources: List[str] = Field(
        ...,
        description="Suggested types of sources to prioritize (e.g., news articles, academic papers, technical blogs, forums).",
    )
    filters: Filters = Field(
        ...,
        description="Filters to apply during the web search, such as timeframe, language, and region.",
    )


class SummarizerOutput(BaseModel):
    summary: str = Field(
        ...,
        description="Summary of the articles",
    )
