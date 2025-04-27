from src.prompts import query_analysis_prompt, summarizer_prompt
from langchain_openai import ChatOpenAI
from src.models import QueryAnalysisOutput, SummarizerOutput

llm = ChatOpenAI(model="gpt-4o-mini")

query_analysis_structured = llm.with_structured_output(QueryAnalysisOutput)
query_analysis_chain = query_analysis_prompt | query_analysis_structured

summarizer_structured = llm.with_structured_output(SummarizerOutput)
summarizer_chain = summarizer_prompt | summarizer_structured
