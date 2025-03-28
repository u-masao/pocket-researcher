"""
このモジュールは背景と目的を清書するエージェントを定義します。
"""

import os

from agents import Agent

CLEAR_BACKGROUND_AND_OBJECTIVE_PROMPT = """
あなたは有能な研究者です。
ユーザーは論文の背景と目的を下書きしたものを提示します。
これを清書し、背景および目的として完成させてください。
"""
clear_background_and_objective_agent = Agent(
    name="背景と目的を清書するエージェント",
    instructions=CLEAR_BACKGROUND_AND_OBJECTIVE_PROMPT,
    model=os.getenv("CLEAR_BACKGROUND_AND_OBJECTIVE_MODEL", "o3-mini"),
)
