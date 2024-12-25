import asyncio
from dto.wiki_responses_dto import SearchResultElement
from typing import List

class WikiService():
    async def get_pages_by_user_search(self, search_string: str) -> List[SearchResultElement]:
        pass

    async def get_text_from_page(self, page_ident: str) -> str:
        pass