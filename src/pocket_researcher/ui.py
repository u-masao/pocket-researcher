from typing import Any, Dict, List, Literal

from dotenv import load_dotenv

load_dotenv()

import gradio as gr
import mlflow
from agents import gen_trace_id, trace

from pocket_researcher.manager import PocketResearchManager

mlflow.set_experiment("PocketResearcher")
mlflow.openai.autolog()


async def review_draft(text, history):
    """
    レビュー依頼の処理
    """

    def append_message(
        role: Literal["user", "assistant", "system"],
        message: str,
        metadata: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """
        Chatbot の history に対してメッセージを追加する
        """
        history.append(
            gr.ChatMessage(
                role=role,
                content=message,
                metadata=metadata,
            )
        )
        return history

    # バリデーションチェック
    if len(text.strip()) == 0:
        raise gr.Error("背景と目的のテキストを入力して下さい", duration=2)

    # ユーザーのメッセージをチャットに表示
    yield append_message("user", "背景と目的をレビューして")

    # エージェントクラスを初期化
    manager = PocketResearchManager()

    # レビューを実施して結果をジェネレーターで取得
    with trace("リサーチサービス", trace_id=gen_trace_id()):
        responses = manager.review_background_and_objective_generator(
            text.strip()
        )
        async for response in responses:
            yield append_message("assistant", response)


async def research(text, history):
    """
    調査とレポート作成処理
    """

    def append_message(
        role: Literal["user", "assistant", "system"],
        message: str,
        metadata: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """
        Chatbot の history に対してメッセージを追加する
        """
        history.append(
            gr.ChatMessage(
                role=role,
                content=message,
                metadata=metadata,
            )
        )
        return history

    # 簡単な入力チェック
    if len(text.strip()) == 0:
        raise gr.Error("背景と目的のテキストを入力して下さい", duration=2)

    # ユーザーのメッセージをチャットに表示
    yield append_message("user", "調査してレポートを作って")

    # エージェントクラスを初期化
    manager = PocketResearchManager()
    with trace("リサーチサービス", trace_id=gen_trace_id()):

        title = "背景と目的を清書"
        yield append_message("assistnat", f"{title}します")
        objective = await manager.clear_background_and_objective(text.strip())
        yield append_message("assistant", objective, metadata={"title": title})

        title = "仮の論文を作成"
        yield append_message("assistnat", f"{title}します")
        full_paper_temp = await manager.make_full_paper_from_objective(
            objective
        )
        yield append_message(
            "assistant", full_paper_temp, metadata={"title": title}
        )

        title = "アブストラクトを作成"
        yield append_message("assistnat", f"{title}します")
        abstract = await manager.make_abstract_from_full_paper(full_paper_temp)
        yield append_message("assistant", abstract, metadata={"title": title})

        title = "レポートを作成"
        yield append_message("assistnat", f"{title}します")
        paper = await manager.make_paper_from_abstract(abstract)
        yield append_message("assistant", "# レポート(完成)")
        gr.Info("レポートが完成しました！", duration=5)
        yield append_message("assistant", paper)


EXAMPLES = [
    [
        """家庭で手軽にチョコレートが作れるのか気になって眠れない。
手軽に発酵済みカカオ豆からチョコレートを作る方法を調べる。"""
    ],
]
with gr.Blocks(fill_width=True) as demo:
    with gr.Row():
        chatbot = gr.Chatbot(height=600, type="messages")
        with gr.Column():
            input_text = gr.Textbox(lines=20, label="背景と目的")
            examples = gr.Examples(EXAMPLES, input_text)
            with gr.Row():
                review_button = gr.Button("レビュー")
                research_button = gr.Button("調査開始")

    # レビュー用コールバック設定
    gr.on(
        review_button.click,
        fn=review_draft,
        inputs=[input_text, chatbot],
        outputs=[chatbot],
    )

    # レポート作成用コールバック設定
    gr.on(
        research_button.click,
        fn=research,
        inputs=[input_text, chatbot],
        outputs=[chatbot],
    )

if __name__ == "__main__":
    demo.launch(share=False, debug=True)
