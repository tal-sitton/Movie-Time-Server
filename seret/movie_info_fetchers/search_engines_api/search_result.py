import dataclasses


@dataclasses.dataclass
class ScoredSearchResult:
    title: str
    url: str
    description: str
    score: float


@dataclasses.dataclass
class ParsedSearchResult:
    title: str
    url: str
    description: str

    def score(self, score: float) -> ScoredSearchResult:
        return ScoredSearchResult(self.title, self.url, self.description, score)
