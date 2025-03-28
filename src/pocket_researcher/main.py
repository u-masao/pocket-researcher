import asyncio
import sys

from .manager import PocketResearchManager

# ポケットリサーチャーの例のエントリーポイント。
# `python -m src.pocket-researcher.main` として実行し、
# リサーチクエリを入力します。例えば：
# "再生可能エネルギー投資の最近の動向を分析してください。"


USAGE = """
========================================================
このアプリケーションはあなたのリサーチを助けるものです。
考えたいことや調べたいことを入力することで、論文の形式で
リサーチ結果を返します。
========================================================
"""


async def main() -> None:
    print(USAGE)
    print("考えたいことや調べたいことの背景と目的を書いて:")
    query = sys.stdin.readlines()
    mgr = PocketResearchManager()
    await mgr.run("\n".join(query))


if __name__ == "__main__":
    asyncio.run(main())
