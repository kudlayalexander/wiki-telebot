from dataclasses import dataclass
from typing import List

@dataclass
class SearchResponse():
    searched_string: str
    titles: List[str]
    short_descriptions: List[str]
    urls: List[str]

@dataclass
class SearchResultElement():
    title: str
    short_description: str
    url: str
    ident: str

