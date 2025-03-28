"""
このモジュールはアブストラクトから論文を書くエージェントを定義します。
"""

import os

from agents import Agent

# アブストラクトから、論文を書かせる
PAPER_FROM_ABSTRACT_PROMPT = """
### 役割
あなたは有能な研究者です。
### 依頼
ユーザーは論文アブストラクトを提示します。アブストラクトから本論文を完成してください。
### 条件
- 推定値で研究を作成しているため、先行研究から得られる値は代入してください。
- 先行研究などの参考文献が得られることを期待しています。信頼性が高いものを選んでください
- 新規性の検討等、論文としてのロバスト性を高めてください
"""

paper_maker_from_abstract_agent = Agent(
    name="アブストラクトから論文を作るエージェント",
    instructions=PAPER_FROM_ABSTRACT_PROMPT,
    model=os.getenv("PAPER_FROM_ABSTRACT_MODEL", "o3-mini"),
)
