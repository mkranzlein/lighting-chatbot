"""Core logic for the lighting chatbot."""

import logging
import os
import re
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)
log_files = [f for f in os.listdir(log_dir) if re.match(r'chat_log_\d+\.txt', f)]
if not log_files:
    log_file_number = 1
else:
    numbers = [int(re.search(r'chat_log_(\d+)\.txt', f).group(1)) for f in log_files]
    log_file_number = max(numbers) + 1
log_file_name = os.path.join(log_dir, f"chat_log_{log_file_number}.txt")
file_handler = logging.FileHandler(log_file_name)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info(f"Logging to file: {log_file_name}")


class State(TypedDict):
    """State for langgraph."""
    llm: object
    prompt: ChatPromptTemplate
    greeting_prompt: ChatPromptTemplate
    retriever: BaseRetriever
    messages: list
    query: str
    context: list
    response: str
    first_interaction: bool


async def generate_greeting(state: State):
    """Generate a greeting."""
    llm = state["llm"]
    greeting_prompt = state["greeting_prompt"]
    response = ""
    async for chunk in llm.astream(greeting_prompt.format_messages()):
        response += chunk or ""
        print(chunk or "", end="", flush=True)
    print()
    logger.info(f"Greeting generated: {response}")
    return {**state,
            "messages": [AIMessage(content=response)],
            "first_interaction": False}


def add_user_message(state: State):
    """Add user query to chat history."""
    query = state["query"]
    logger.info(f"User query received: {query}")
    return {**state,
            "messages": state["messages"] + [HumanMessage(content=query)]}


async def generate_response(state: State):
    """Generate model response based on chat history and retrieved docs."""
    query = state["query"]
    retriever = state["retriever"]
    llm = state["llm"]
    prompt = state["prompt"]
    logger.info(f"Retrieving documents for query: {query}")
    results = await retriever.ainvoke(query)
    context = "\n\n".join([doc.page_content for doc in results])
    logger.info(f"Retrieved {len(results)} documents. Context: {context[:200]}...")
    chat_inputs = {
        "context": context,
        "history": state["messages"],
        "input": query
    }
    logger.info("Generating response using LLM (streaming)")
    response = ""
    print()
    async for chunk in llm.astream(prompt.format_messages(**chat_inputs)):
        response += chunk or ""
        print(chunk or "", end="", flush=True)
    print()
    logger.info(f"Response generated: {response}")
    return {**state,
            "messages": state["messages"] + [AIMessage(content=response)],
            "context": results}


def router(state: State) -> str:
    """Determine if chain entry point should be greeting or user message."""
    if state["first_interaction"] is True:
        return "generate_greeting"
    else:
        return "add_user_message"


def get_chain():
    """Creates the LangGraph workflow."""
    workflow = StateGraph(State)
    workflow.add_node("generate_greeting", generate_greeting)
    workflow.add_node("add_user_message", add_user_message)
    workflow.add_node("generate_response", generate_response)
    workflow.add_conditional_edges(START, router)
    workflow.add_edge("generate_greeting", END)
    workflow.add_edge("add_user_message", "generate_response")
    workflow.add_edge("generate_response", END)
    return workflow.compile()
