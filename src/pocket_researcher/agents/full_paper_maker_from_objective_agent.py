"""
このモジュールは仮の全体像を書かせるエージェントを定義します。
"""

import os

from agents import Agent

# 背景と目的から全体像を書かせるプロンプト
FULL_PAPER_MAKER_FROM_OBJECTIVE_PROMPT = """
あなたは有能な研究者です。
ユーザーは論文の背景と目的の部分を提示します。これをもとに、論文を完成させてください。
- 最新の研究成果を利用するためにインターネットの情報を積極的に利用してください
- 論文の構成は 1.背景 2.目的 3.材料と方法 4.結果 5.考察 6.結論のように、形式を守ってください
- 不明な数値があれば、不正確な値を入れずフェルミ推定などの推定を行い、推定値を代入してくだ>さい
- ただし、推定値には必ず（推定値）と明記してください
- 文字数はおよそ1万文字とします
"""

full_paper_maker_from_objective_agent = Agent(
    name="背景と目的から全体像を作るエージェント",
    instructions=FULL_PAPER_MAKER_FROM_OBJECTIVE_PROMPT,
    model=os.getenv("FULL_PAPER_MAKER_FROM_OBJECTIVE_MODEL", "o3-mini"),
)
