import asyncio

from .manager import PocketResearchManager

# ポケットリサーチャーの例のエントリーポイント。


async def main() -> None:
    mgr = PocketResearchManager()
    await mgr.run()


if __name__ == "__main__":
    asyncio.run(main())
