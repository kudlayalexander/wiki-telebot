import aiohttp
import logging
import json
from lxml import html

from wiki.dto.wiki_search_dtos import SearchResponse

logger = logging.getLogger("WikiRequests")


class WikiRequests():
    def __init__(self, wiki_url: str):
        self.wiki_url = wiki_url

    async def get_full_text_from_page(self, page_ident: str) -> str:
        logger.info(f"Trying to get full text of page: '{
                    page_ident}' from {self.wiki_url}")

        request_params = {
            "action": "parse",
            "page": page_ident,
            "format": "json",
            "prop": "text"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.wiki_url, params=request_params) as response:
                if response.status != 200:
                    logger.error(f"Failed to get page property: {
                                 response.status}")
                    return ""

                logger.debug(f"Status: {response.status}")
                logger.debug(
                    f"Content-type: {response.headers['content-type']}")

                raw_html = await response.json()

                return raw_html["parse"]["text"]["*"]

    async def get_short_text_from_page(self, page_ident: str) -> str:
        logger.info(f"Trying to get short page text : '{
                    page_ident}' from {self.wiki_url}")

        request_params = {
            "action": "parse",
            "page": page_ident,
            "format": "json",
            "prop": "text"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.wiki_url, params=request_params) as response:
                if response.status != 200:
                    logger.error(f"Failed to get page property: {
                                 response.status}")
                    return ""

                logger.debug(f"Status: {response.status}")
                logger.debug(
                    f"Content-type: {response.headers['content-type']}")

                raw_html = await response.json()

                raw_html = raw_html["parse"]["text"]["*"]

                document = html.document_fromstring(raw_html)

                first_p = document.xpath('//p')[0]
                intro_text = first_p.text_content()

                if len(intro_text) > 200:
                    intro_text = intro_text[0:350] + "..."

                return intro_text

    async def get_search_results(self, searched_string: str) -> SearchResponse:
        logger.info(f"Trying to get search results of: '{
                    searched_string}' from {self.wiki_url}")

        request_params = {
            "action": "opensearch",
            "format": "json",
            "namespace": "0",
            "search": searched_string,
            "limit": "10"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.wiki_url, params=request_params) as response:
                if response.status != 200:
                    logger.error(f"Failed to get search results: {
                                 response.status}")
                    return []

                logger.debug(f"Status: {response.status}")
                logger.debug(
                    f"Content-type: {response.headers['content-type']}")

                response_text = await response.text()
                json_response = json.loads(response_text)

                # logger.debug(f"Body: {json_response}")

        return SearchResponse(
            searched_string=json_response[0],
            titles=json_response[1],
            annotations=json_response[2],
            urls=json_response[3]
        )
