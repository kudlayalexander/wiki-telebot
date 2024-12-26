import logging
import aiohttp
import json
import asyncio
import dotenv

from wiki.wiki_requests import WikiRequests
from wiki.wiki_service import WikiService

from llm.cohere_service import CohereService
from llm.cohere_requests import CohereRequests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("WikiRequests")

async def test():
    cohere_api_key = dotenv.get_key(dotenv_path=".env",key_to_get="COHERE_API_KEY")
    wiki_api_url = dotenv.get_key(dotenv_path=".env",key_to_get="WIKI_API_URL")

    wiki_requests = WikiRequests(wiki_api_url)
    wiki_service: WikiService = WikiService(wiki_requests)

    cohere_requests = CohereRequests(cohere_api_key)
    cohere_service: CohereService = CohereService(cohere_requests)
    
    res = await wiki_service.get_text_from_page("Ignat")
    print("===================GET TEXT FROM PAGE=================")   
    await asyncio.sleep(1)
    print(res)

    summarized = await cohere_service.summarize_text(res)
    print(summarized)


if __name__ == "__main__":
    asyncio.run(test())

