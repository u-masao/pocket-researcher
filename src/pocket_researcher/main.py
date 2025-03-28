import asyncio

from .manager import PocketResearchManager

# ポケットリサーチャーの例のエントリーポイント。
# `python -m src.pocket-researcher.main` として実行し、
# リサーチクエリを入力します。例えば：
# "再生可能エネルギー投資の最近の動向を分析してください。"


async def main() -> None:
    query = input("Enter a research query: ")
    mgr = PocketResearchManager()
    await mgr.run(query)


if __name__ == "__main__":
    asyncio.run(main())
