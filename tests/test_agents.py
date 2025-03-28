import re

from agents import Runner

from pochet_researcher.agents.background_objective_maker_agent import (
    background_objective_maker_agent,
)


def test_background_objective_maker_agent():
    """
    ツッコミどころのある背景と目的を送信すると、
    エージェントが突っ込んでくれる
    """
    prompt = (
        "# 背景\n\n犬猫は人気だがAI分類は完璧でなく、多くの人が関心を持つため重要だ。"
        "\n\n"
        "# 目的\n\n最新深層学習で超高精度な犬猫分類AIを開発する。ネット画像で多様な"
        "モデルを試し、ほぼ100%精度を目指す。多くの人に喜ばれる成果を期待する。"
    )
    print(f"{prompt=}")
    result = Runner.run_sync(background_objective_maker_agent, prompt)
    print(f"{result.final_output=}")

    # レスポンスがある
    assert len(result.final_output) > 0

    # 100% という記載がある(何回かチェックして毎回突っ込まれる)
    assert re.match(
        ".*(100%|精度|画像).*", result.final_output, re.MULTILINE | re.DOTALL
    )
