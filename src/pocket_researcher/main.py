import asyncio

from .manager import PocketResearchManager

# ポケットリサーチャーの例のエントリーポイント。


async def main() -> None:
    mgr = PocketResearchManager()
    result = await mgr.run()
    print(f"=========================\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
