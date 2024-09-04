
import chainlit as cl
import os
from dotenv import load_dotenv
from chainlit.input_widget import Select

from langchain.memory import ConversationBufferMemory

from tirith_copilot.agent import agent_executor

load_dotenv()
memory= ConversationBufferMemory()
@cl.on_chat_start
async def starter():
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message("Welcome to Tirith-Copilot").send()
    cl.user_session.set("memory", [])

@cl.on_message
async def main(message: cl.Message):
    memory = cl.user_session.get('memory')
    
    result = agent_executor.invoke({"input": message.content, "chat_history": memory})

    await cl.Message(result['output']).send()
    memory.append((message.content, result['output']))

@cl.password_auth_callback
def auth(username: str, password: str):
    data = [("admin", "admin@123")]
    if (username, password) in data:
        return cl.User(identifier=username,
                       metadata={"role": "admin", "provider": "credentials"})

