import logging
import sys
import textwrap

from agents import Runner, gen_trace_id, trace

from pocket_researcher.agents.background_objective_maker_agent import (
    background_objective_maker_agent,
)

USAGE = """
    ========================================================
    このアプリケーションはあなたのリサーチを助けるものです。
    考えたいことや調べたいことを入力することで、論文の形式で
    リサーチ結果を返します。
    ========================================================
"""


def read_multiple_input() -> str:
    """標準入力を読み取る関数"""
    print("    (入力終了は Ctrl+D または Ctrl+Z を入力)")
    query = sys.stdin.readlines()
    return "".join(query)


class PocketResearchManager:
    """
    デモ用の最小限のリサーチマネージャー。
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.WARNING)

    async def run(self) -> None:
        # print usage
        print(textwrap.dedent(USAGE))

        with trace("リサーチサービス", trace_id=gen_trace_id()):

            conferm_background_and_objective = False
            while not conferm_background_and_objective:
                # 背景と目的のラフを入力
                print(">>> 考えたいことや調べたいことの背景と目的を書いて:")
                query = read_multiple_input()
                print(f">>> 背景と目的:\n\n```\n{query}\n```")
                print(">>> 回答作成中")

                # レビュー生成
                result = await Runner.run(
                    background_objective_maker_agent,
                    input=query,
                )
                print(
                    f">>> 背景と目的と指摘事項:\n\n```\n{result.final_output}\n```"
                )

                # 人間に確認
                while True:
                    command = input(
                        ">>> 背景と目的を清書しますか？(yes/no)"
                    ).lower()
                    if command == "yes":
                        conferm_background_and_objective = True
                    elif len(command) > 0:
                        continue

        print(f"背景と目的が確定しました。\n\n```\n{query}\n```")
        print("Research completed.")
