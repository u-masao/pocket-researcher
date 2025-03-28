import asyncio
import logging


class PocketResearchManager:
    """
    デモ用の最小限のリサーチマネージャー。
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def run(self, query: str) -> None:
        self.logger.info(f"Running research for query: {query}")
        # 簡単なリサーチプロセスをシミュレート
        await asyncio.sleep(1)
        self.logger.info("Research completed.")
