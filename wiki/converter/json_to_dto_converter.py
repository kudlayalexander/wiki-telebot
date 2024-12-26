from typing import List

from wiki.dto.wiki_search_dtos import SearchResponse, SearchResultElement


class WikiResponseConverter():
    @staticmethod
    async def convert_search_response(search_response: SearchResponse) -> List[SearchResultElement]:
        if search_response is None:
            return []
        
        search_results = []
        for i in range(len(search_response.titles)):
            search_results.append(
                SearchResultElement(
                    title=search_response.titles[i],
                    short_description=search_response.short_descriptions[i],
                    url=search_response.urls[i],
                    ident=search_response.titles[i].replace(" ", "_")
                )
            )

        return search_results