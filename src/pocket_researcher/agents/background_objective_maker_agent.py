"""
このモジュールは背景と目的を作るエージェントを定義します。
"""

import os

from agents import Agent

BACKGROUND_OBJECTIVE_MAKER_PROMPT = """
あなたは有能な研究者です。実験の計画を立案するためにユーザーに対して的確な
アドバイスをしてください。
ユーザーは論文の背景と目的を下書きしたものを提示します。
これを3〜5行で要約し、内容に飛躍や不足があれば明確に指摘してください。
出力は日本語とします。
"""

background_objective_maker_agent = Agent(
    name="背景と目的を作るエージェント",
    instructions=BACKGROUND_OBJECTIVE_MAKER_PROMPT,
    model=os.getenv("BACKGROUND_OBJECTIVE_MAKER_MODEL", "o3-mini"),
)
