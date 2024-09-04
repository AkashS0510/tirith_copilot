#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langserve import add_routes

from tirith_copilot.agent import agent_executor

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)


# Adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
# /stream_events
add_routes(
    app,
    agent_executor
)


def run_server():
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
