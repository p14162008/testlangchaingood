from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Langchain Streaming Orchestrator")

class QueryRequest(BaseModel):
    query: str

llm = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)

# Requirement: Separate Math and General prompts
general_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful general assistant. Prefix with [General]:"),
    ("user", "{query}")
])

math_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math expert. Solve step-by-step. Prefix with [Math]:"),
    ("user", "{query}")
])

async def generate_chat_stream(query: str):
    # Requirement: Topic Routing
    is_math = any(char in query for char in ["+", "-", "*", "/", "math", "calculate"])
    
    selected_prompt = math_prompt if is_math else general_prompt
    chain = selected_prompt | llm | StrOutputParser()
        
    async for chunk in chain.astream({"query": query}):
        yield f"data: {chunk}\n\n"

# Requirement: Endpoint must be POST /ask
@app.post("/ask")
async def ask_endpoint(req: QueryRequest):
    return StreamingResponse(
        generate_chat_stream(req.query), 
        media_type="text/event-stream"
    )
