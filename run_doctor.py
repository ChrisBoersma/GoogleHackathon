import asyncio
from Doctor.agent import root_agent
from google.adk.runners import InMemoryRunner

async def main():
    runner = InMemoryRunner()
    await runner.run_async(root_agent)

if __name__ == "__main__":
    asyncio.run(main())
