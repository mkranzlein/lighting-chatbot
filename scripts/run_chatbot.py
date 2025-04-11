"""Script to run the lighting chatbot."""

import asyncio
import sys

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# from lighting_chatbot.unstructured_rag_chatbot import State

from lighting_chatbot.prompt_loader import load_prompt
from lighting_chatbot.unstructured_rag_chatbot import get_chain

# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_chroma import Chroma  # noqa E402


async def ainput_stream():
    """Async generator for user input."""
    while True:
        yield input("\nYou: ")


async def main():
    embeddings_dir = "./data/chroma_db"
    embedding_model_name = "all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vectordb = Chroma(persist_directory=embeddings_dir, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    llm = OllamaLLM(model="hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M")

    system_prompt_text = load_prompt("prompts/system_prompt.txt")
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt_text.format(
            additional_instructions="Context: {context}")),
        MessagesPlaceholder(variable_name="history"),
        HumanMessage(content="{input}")
    ])

    greeting_prompt_text = load_prompt("prompts/greeting_prompt.txt")
    greeting_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt_text.format(
            additional_instructions=greeting_prompt_text))
    ])

    chain = get_chain()

    initial_state = {
        "llm": llm,
        "prompt": prompt,
        "greeting_prompt": greeting_prompt,
        "retriever": retriever,
        "messages": [],
        "query": "",
        "context": [],
        "response": "",
        "first_interaction": True
    }

    state = await chain.ainvoke(initial_state)

    # Chat loop
    async for user_input in ainput_stream():
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Assistant: Goodbye!")
            break

        state["query"] = user_input
        state = await chain.ainvoke(state)
        # The response is now streamed in the generate_response function


if __name__ == "__main__":
    asyncio.run(main())
