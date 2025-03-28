import asyncio

from dotenv import load_dotenv

load_dotenv()
from .manager import PocketResearchManager  # noqa: E402

# ポケットリサーチャーの例のエントリーポイント。


async def main() -> None:
    mgr = PocketResearchManager()
    result = await mgr.run()
    print(f"=========================\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
