from dataclasses import dataclass
from typing import List


@dataclass
class SearchResponse():
    searched_string: str
    titles: List[str]
    annotations: List[str]
    urls: List[str]


@dataclass
class SearchResultElement():
    title: str
    annotation: str
    url: str
    ident: str
