"""
このモジュールは背景と目的を作るエージェントを定義します。
"""

from agents import Agent

BACKGROUND_OBJECTIVE_PROMPT = """
あなたは有能な研究者です。実験の計画を立案するためにユーザーに対して的確な
アドバイスをしてください。
ユーザーは論文の背景と目的を下書きしたものを提示します。
これを3〜5行で要約し、内容に飛躍や不足があれば指摘してください。
"""

background_objective_maker_agent = Agent(
    name="背景と目的を作るエージェント",
    instructions=BACKGROUND_OBJECTIVE_PROMPT,
)
