from dotenv import load_dotenv

load_dotenv()

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
from pocket_researcher.agents.paper_maker_from_abstract_agent import (
    paper_maker_from_abstract_agent,
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
    prompt = """
        # 背景
        犬猫は人気だがAI分類は完璧でなく、多くの人が関心を持つため重要だ。

        # 目的
        最新深層学習で超高精度な犬猫分類AIを開発する。ネット画像で多様な
        モデルを試し、ほぼ100%精度を目指す。多くの人に喜ばれる成果を期待する。
    """
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

    # レスポンスが 2000 文字以上である
    assert len(result.final_output) >= 2000

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
    assert len(result.final_output) >= 100

    # レスポンスが 2000 文字以下である
    assert len(result.final_output) <= 2000

    # それっぽい記載があるか確認
    assert re.match(
        ".*(機械学習|時系列|深層学習|推定値).*",
        result.final_output,
        re.MULTILINE | re.DOTALL,
    )


def test_paper_maker_from_abstract_agent(trace_info):
    """
    アブストラクトから論文を書く
    """
    prompt = """
        本研究は、近年急速に発展しているAIエージェント技術の中で、柔軟か
        つ高効率な開発ツールとして注目されるOpenAI Agents SDKの利用事例
        および関連技術情報を、体系的に収集・分類し、社会実装に向けた具体
        的な応用候補を抽出することを目的とする。従来、エージェントシステ
        ムは各分野における実装例や評価基準が分散しており、市場ニーズや
        技術的実現性、さらに独自性とのバランスが十分に検証されてこな
        かった。本研究では、学術文献、業界レポート、オープンソース情報、
        インタビューおよびアンケート調査を組み合わせた複合的手法により、
        金融、医療、交通、カスタマーサポート、エンターテイメント等、
        複数の領域での利用事例を網羅的に収集し、各事例の特性や課題、成
        功要因を詳細に整理した。さらに、定量的および定性的評価指標を構
        築し、市場ニーズ、技術的実現性および独自性の三軸から各事例を評価
        することで、特に実用化に向けて有望な応用シナリオを明らかにした。
        分析結果は、各分野ごとに要求される安全性、信頼性、柔軟性のバラン
        スを踏まえた実装戦略の構築に寄与するものであり、今後のAIエー
        ジェントシステムの標準化や広範な実社会への展開に向けた具体的な指
        針を提供する。
    """
    print(f"{prompt=}")
    with trace(TRACE_NAME, trace_id=trace_info.trace_id):
        result = Runner.run_sync(paper_maker_from_abstract_agent, prompt)
    print(f"{result.final_output=}")

    # レスポンスがある
    assert len(result.final_output) > 0

    # レスポンスが 3000 文字以上である
    assert len(result.final_output) >= 1000

    # レスポンスが 50000 文字以下である
    assert len(result.final_output) <= 50000

    # それっぽい記載があるか確認
    assert re.match(
        ".*(エージェント|信頼性|OpenAI).*",
        result.final_output,
        re.MULTILINE | re.DOTALL,
    )
