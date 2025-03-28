import logging

from agents import Runner, gen_trace_id, trace

from pocket_researcher.agents.background_objective_maker_agent import (
    background_objective_maker_agent,
)


class PocketResearchManager:
    """
    デモ用の最小限のリサーチマネージャー。
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def run(self, query: str) -> None:
        self.logger.info(f"Running research for query: {query}")

        with trace("リサーチサービス", trace_id=gen_trace_id()):

            result = await Runner.run(
                background_objective_maker_agent,
                input=query,
            )

            self.logger.info(
                "背景と目的と指摘事項:\n" f"{result.final_output}"
            )
        self.logger.info("Research completed.")
