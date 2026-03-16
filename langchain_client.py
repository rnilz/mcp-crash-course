import os
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano", api_key=os.getenv("OPEN_API_KEY"))


async def main():
    print("Starting LangChain client")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "C:\\Users\\nilsh\\Projects\\mcp-crash-course\\servers\\math_server.py"
                ],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )

    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    result = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    # content="What is 54 + 2 * 3? use tools to calculate the answer"
                    content="What is the weather in Tokyo? use tools to get the answer"
                )
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
