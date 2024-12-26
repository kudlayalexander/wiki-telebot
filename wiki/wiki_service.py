import asyncio
from typing import List

from wiki.wiki_requests import WikiRequests

from wiki.converter.json_to_dto_converter import WikiResponseConverter
from wiki.dto.wiki_search_dtos import SearchResultElement, SearchResponse

import logging
logger = logging.getLogger("WikiService")

class WikiService():
    def __init__(self, wiki_requests: WikiRequests): 
        self.wiki_requests = wiki_requests

    async def get_pages_by_user_search(self, search_string: str) -> List[SearchResultElement]:
        try:
            if search_string is None:
                raise ValueError("Search string can not be empty.")
            
            if not isinstance(search_string, str):
                raise TypeError("Search string must be of type string")

            found_pages_response: SearchResponse = await self.wiki_requests.get_search_results(search_string)
        
            found_pages: List[SearchResultElement] = await WikiResponseConverter.convert_search_response(found_pages_response)

            for page in found_pages:
                page.short_description = await self.wiki_requests.get_short_text_from_page(page.ident)
            
        except Exception as exc:
            logger.error(f"Failed to get pages by user search: {exc}")
            return []

        return found_pages


    async def get_text_from_page(self, page_ident: str) -> str:
        try:
            if page_ident is None:
                raise ValueError("Page ident can not be empty.")
            
            if not isinstance(page_ident, str):
                raise TypeError("Page ident must be of type string")

            page_text: SearchResponse = await self.wiki_requests.get_full_text_from_page(page_ident)
        
            return page_text
        except Exception as exc:
            logger.error(f"Failed to get page text: {exc}")
            return "FAILED"