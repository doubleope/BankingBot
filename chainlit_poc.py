from langchain.llms import OpenAI
from langchain_experimental.agents import create_csv_agent
import chainlit as cl
from prompts import prompt


data_path = "data/cleaned_data.csv"


@cl.on_chat_start
def query_llm():
    llm = OpenAI(temperature=0)
    agent_executer = create_csv_agent(llm, path=data_path, verbose=True, allow_dangerous_code=True)
    cl.user_session.set("agent_executer", agent_executer)


@cl.on_message
async def handle_message(message: cl.Message):
    agent_executer = cl.user_session.get("agent_executer")
    response = await agent_executer.acall(prompt + message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])

    await cl.Message(response["output"]).send()
