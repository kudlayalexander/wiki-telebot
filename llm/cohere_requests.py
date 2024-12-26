import asyncio
import cohere
import dotenv
import logging

logger = logging.getLogger("CohereRequests")

class CohereRequests():
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def make_request(self, request_text: str, wiki_text: str) -> str:
        logger.info("Making request to GPT with this text:")
        message = request_text + wiki_text
        logger.debug(message)

        co = cohere.AsyncClientV2(api_key=self.api_key)
        
        res = await co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return res.message.content[0].text