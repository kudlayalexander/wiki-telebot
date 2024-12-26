
from llm.cohere_requests import CohereRequests
import logging

logger = logging.getLogger("CohereRequests")


class CohereService():
    def __init__(self, cohere_requests: CohereRequests):
        self.cohere_requests = cohere_requests

    async def summarize_text(self, wiki_text: str) -> str:
        try:
            logger.info("Trying to summarize text")

            if wiki_text is None:
                raise ValueError("Wiki text can not be empty.")

            if not isinstance(wiki_text, str):
                raise TypeError("Wiki text must be of type string")

            request_text = "Summarize this text, write not more than 700 symbols:"

            summarized_text = await self.cohere_requests.make_request(request_text, wiki_text)

            return summarized_text
        except Exception as exc:
            logger.error(f"Failed to summarize text: {exc}")
            return "FAILED"
