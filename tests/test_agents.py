import re

from agents import Runner

from pochet_researcher.agents.background_objective_maker_agent import (
    background_objective_maker_agent,
)
from pochet_researcher.agents.full_paper_maker_from_objective_agent import (
    full_paper_maker_from_objective_agent,
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

    # それっぽい記載があるか確認
    assert re.match(
        ".*(100%|精度|画像).*", result.final_output, re.MULTILINE | re.DOTALL
    )


def test_full_paper_maker_from_objective_agent():
    """
    背景と目的を送信すると1万字の論文を書く
    """
    prompt = (
        "従来の機械学習モデルは、複雑なデータに対して精度向上の限界が見られる。"
        "本研究では、新たなアルゴリズムを導入し、特に時系列予測の分野における"
        "予測精度を大幅に向上させることを目的とする。具体的には、曜日と祝日の"
        "データを組み合わせ、深層学習モデルを用いて高精度な予測モデルを構築する。"
    )
    print(f"{prompt=}")
    result = Runner.run_sync(full_paper_maker_from_objective_agent, prompt)
    print(f"{result.final_output=}")

    # レスポンスがある
    assert len(result.final_output) > 0

    # レスポンスが 3000 文字以上である
    assert len(result.final_output) >= 3000

    # レスポンスが 50000 文字以下である
    assert len(result.final_output) <= 50000

    # それっぽい記載があるか確認
    assert re.match(
        ".*(機械学習|時系列|深層学習).*",
        result.final_output,
        re.MULTILINE | re.DOTALL,
    )
