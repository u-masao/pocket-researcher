import asyncio
from .manager import PocketResearchManager

# Entrypoint for the pocket researcher example.
# Run this as `python -m src.pocket-researcher.main` and enter a
# research query, for example:
# "Analyze the recent trends in renewable energy investments."
async def main() -> None:
    query = input("Enter a research query: ")
    mgr = PocketResearchManager()
    await mgr.run(query)

if __name__ == "__main__":
    asyncio.run(main())
