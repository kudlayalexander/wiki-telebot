from dataclasses import dataclass

@dataclass
class SearchResultElement():
    title: str
    annotation: str
    url: str
    ident: str