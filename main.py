from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Langchain Streaming Orchestrator")

class QueryRequest(BaseModel):
    query: str

# Base LLM with streaming enabled
llm = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)

@app.get("/health")
def health():
    return {"status": "healthy"}
