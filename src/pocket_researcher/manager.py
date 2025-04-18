import logging
import sys
import textwrap

import mlflow
from agents import Runner, gen_trace_id, trace

from pocket_researcher.custom_agents import (
    abstract_maker_agent,
    background_objective_maker_agent,
    clear_background_and_objective_agent,
    full_paper_maker_from_objective_agent,
    paper_maker_from_abstract_agent,
)

mlflow.set_experiment("PocketResearcher")
mlflow.openai.autolog()

USAGE = """
    > 考えたいことや調べたいことを入力してください。
    > 論文の形式でリサーチ結果を表示します。
"""


class PocketResearchManager:
    """
    デモ用の最小限のリサーチマネージャー。
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        # logging.basicConfig(level=logging.WARNING)

    async def run(self) -> None:
        print(textwrap.dedent(USAGE))

        with trace("リサーチサービス", trace_id=gen_trace_id()):
            objective_draft = await self.input_background_and_objective_draft()
            objective = await self.clear_background_and_objective(
                objective_draft
            )
            full_paper_temp = await self.make_full_paper_from_objective(
                objective
            )
            abstract = await self.make_abstract_from_full_paper(
                full_paper_temp
            )
            paper = await self.make_paper_from_abstract(abstract)

        return paper

    async def read_multiple_input(self) -> str:
        """標準入力を読み取る関数"""
        print(">    (入力終了は Ctrl+D または Ctrl+Z を入力)")
        query = sys.stdin.readlines()
        return "".join(query)

    async def review_background_and_objective_generator(
        self, query: str
    ) -> str:
        """
        背景と目的のテキストをレビューするエージェント
        """
        yield f"### 背景と目的:\n\n```\n{query}\n```"
        yield "### 回答作成中"

        # レビュー生成
        result = await Runner.run(
            background_objective_maker_agent,
            input=query,
        )

        yield f"### 背景と目的と指摘事項:\n\n```\n{result.final_output}\n```"

    async def input_background_and_objective_draft(self) -> str:
        """
        ユーザーから背景と目的のラフを受け取り要約と評価をする。
        標準入力を読み取り完了確認を行う。
        """
        # 終了フラグ
        conferm_background_and_objective = False

        # 終了フラグが立つまでループ
        while not conferm_background_and_objective:

            # 背景と目的のラフを入力
            print("> 考えたいことや調べたいことの背景と目的を書いてください:")
            query = await self.read_multiple_input()

            # レビューを依頼
            results = self.review_background_and_objective_generator(query)

            # 進行状況と結果を表示
            async for result in results:
                print(result)

            # 人間に確認するループ
            while True:
                command = input(
                    "> この後の処理はノンストップです。\n"
                    "> 背景と目的を確定して論文を作成しますか？(yes/no):"
                ).lower()

                # 入力チェック
                if len(command) == 0 or command not in ["yes", "no"]:
                    continue

                # yes で終了フラグを立てる
                if command == "yes":
                    conferm_background_and_objective = True

                # 人間に確認するループを終了
                break

        # 結果を出力
        print(f"> 背景と目的のドラフトが確定しました。\n\n```\n{query}\n```")
        # 最後にユーザーが入力した文章を返す
        return query

    async def clear_background_and_objective(self, draft: str) -> str:
        """
        入力されたテキストを「背景と目的」として清書する。
        """

        print("> 背景と目的を清書中")

        # 背景と目的を清書中
        result = await Runner.run(
            clear_background_and_objective_agent,
            input=draft,
        )
        print(
            f"> 背景と目的を清書しました。\n\n```\n{result.final_output}\n```"
        )

        return result.final_output

    async def make_full_paper_from_objective(self, objective: str) -> str:
        """
        入力された「背景と目的」から仮の論文を作成する。
        """

        print("> 仮の論文を作成中")

        # 仮の論文を作成中
        result = await Runner.run(
            full_paper_maker_from_objective_agent,
            input=objective,
        )

        print(f"> 仮の論文を作成しました。\n\n```\n{result.final_output}\n```")
        return result.final_output

    async def make_abstract_from_full_paper(self, full_paper: str) -> str:
        """
        入力された「仮の論文」からアブストラクトを作成する。
        """

        print("> アブストラクトを作成中")

        # アブストラクトを作成
        result = await Runner.run(
            abstract_maker_agent,
            input=full_paper,
        )

        print(
            f"> アブストラクトを作成しました。\n\n```\n{result.final_output}\n```"
        )
        return result.final_output

    async def make_paper_from_abstract(self, abstract: str) -> str:
        """
        アブストラクトから論文を作成する。
        """

        print("> 論文を作成中")

        # 論文を作成中
        result = await Runner.run(
            paper_maker_from_abstract_agent,
            input=abstract,
        )

        print(f"> 論文を作成しました。\n\n```\n{result.final_output}\n```")
        return result.final_output
