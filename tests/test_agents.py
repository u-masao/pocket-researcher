import re
from pathlib import Path

import pytest
from agents import Runner, gen_trace_id, trace
from pydantic import BaseModel

from pocket_researcher.agents.abstract_maker_agent import abstract_maker_agent
from pocket_researcher.agents.background_objective_maker_agent import (
    background_objective_maker_agent,
)
from pocket_researcher.agents.clear_background_and_objective_agent import (
    clear_background_and_objective_agent,
)
from pocket_researcher.agents.full_paper_maker_from_objective_agent import (
    full_paper_maker_from_objective_agent,
)

# 実行中のファイル名から拡張子を除いた部分を取得
TRACE_NAME = Path(__file__).stem


class TraceInfo(BaseModel):
    """
    trace_id を保持するクラス
    """

    trace_id: str


@pytest.fixture(scope="module")
def trace_info():
    """
    TraceInfo インスタンスを作成して返す
    """
    return TraceInfo(trace_id=gen_trace_id())


def test_background_objective_maker_agent(trace_info):
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
    with trace(TRACE_NAME, trace_id=trace_info.trace_id):
        result = Runner.run_sync(background_objective_maker_agent, prompt)

    print(f"{result.final_output=}")

    # レスポンスがある
    assert len(result.final_output) > 0

    # それっぽい記載があるか確認
    assert re.match(
        ".*(100%|精度|画像).*", result.final_output, re.MULTILINE | re.DOTALL
    )


def test_clera_background_and_objective_agent(trace_info):
    """
    背景と目的を清書する
    """
    prompt = (
        "従来の機械学習モデルときたら、複雑なデータにゃ精度向上の限界が見え"
        "隠れするのよね。そこで本研究、新アルゴリズムを引っさげ、時系列予測"
        "ってやつをググっと向上させるのが目的なの。具体的には、曜日とか祝日"
        "とかのデータをこねくり回し、深層学習モデルって秘密兵器で高精度な予"
        "測モデルを錬成しちゃうわよ。"
    )

    print(f"{prompt=}")
    with trace(TRACE_NAME, trace_id=trace_info.trace_id):
        result = Runner.run_sync(clear_background_and_objective_agent, prompt)
    print(f"{result.final_output=}")

    # レスポンスがある
    assert len(result.final_output) > 0

    # レスポンスが 3000 文字以上である
    assert len(result.final_output) >= 200

    # レスポンスが 50000 文字以下である
    assert len(result.final_output) <= 600

    # それっぽい記載があるか確認
    assert re.match(
        ".*(機械学習|時系列|深層学習).*",
        result.final_output,
        re.MULTILINE | re.DOTALL,
    )


def test_full_paper_maker_from_objective_agent(trace_info):
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
    with trace(TRACE_NAME, trace_id=trace_info.trace_id):
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


def test_abstract_maker_agent(trace_info):
    """
    背景と目的をもとに推定値いりのアブストラクトを書く
    """
    prompt = (
        "従来の機械学習モデルは、複雑なデータに対して精度向上の限界が見られる。"
        "本研究では、新たなアルゴリズムを導入し、特に時系列予測の分野における"
        "予測精度を大幅に向上させることを目的とする。具体的には、曜日と祝日の"
        "データを組み合わせ、深層学習モデルを用いて高精度な予測モデルを構築する。"
    )
    print(f"{prompt=}")
    with trace(TRACE_NAME, trace_id=trace_info.trace_id):
        result = Runner.run_sync(abstract_maker_agent, prompt)
    print(f"{result.final_output=}")

    # レスポンスがある
    assert len(result.final_output) > 0

    # レスポンスが 200 文字以上である
    assert len(result.final_output) >= 200

    # レスポンスが 2000 文字以下である
    assert len(result.final_output) <= 2000

    # それっぽい記載があるか確認
    assert re.match(
        ".*(機械学習|時系列|深層学習|推定値).*",
        result.final_output,
        re.MULTILINE | re.DOTALL,
    )
