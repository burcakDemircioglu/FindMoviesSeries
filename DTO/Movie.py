from dataclasses import dataclass

@dataclass
class Movie:
    id: int
    adult: bool
    backdrop_path: str
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    title: str
    video: bool
    vote_average: float
    vote_count: int
    genre_ids: list[int]