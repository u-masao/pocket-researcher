"""
このモジュールはアブストラクトを作成するエージェントを定義します。
"""

import os

from agents import Agent

ABSTRACT_MAKER_PROMPT = """
あなたは優秀な研究者です。
ユーザーは論文の背景と目的を提示しますので、論文のアブストラクトを作成してください。
推定値はアブストラクトに入らないように考慮してください。
出力は日本語とします。
"""

abstract_maker_agent = Agent(
    name="アブストラクト作成エージェント",
    instructions=ABSTRACT_MAKER_PROMPT,
    model=os.getenv("ABSTRACT_MAKER_MODEL", "o3-mini"),
)
