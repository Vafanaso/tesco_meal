from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl, Field

class SearchMetadata(BaseModel):
    id: str
    status: str
    json_endpoint: HttpUrl
    pixel_position_endpoint: HttpUrl
    created_at: str
    processed_at: str
    google_url: HttpUrl
    raw_html_file: HttpUrl
    total_time_taken: float

class SearchParameters(BaseModel):
    engine: str
    q: str
    location_requested: str
    location_used: str
    google_domain: str
    hl: str
    gl: str
    device: str

class SearchInformation(BaseModel):
    query_displayed: str
    total_results: int
    time_taken_displayed: float
    organic_results_state: str

class DetectedExtensions(BaseModel):
    price: Optional[float] = None
    currency: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None

class Bottom(BaseModel):
    detected_extensions: Optional[DetectedExtensions] = None
    extensions: Optional[List[str]] = None

class RichSnippet(BaseModel):
    bottom: Optional[Bottom] = None

class OrganicResult(BaseModel):
    position: int
    title: str
    link: HttpUrl
    redirect_link: HttpUrl
    displayed_link: str
    favicon: Optional[HttpUrl] = None
    snippet: Optional[str] = None
    snippet_highlighted_words: Optional[List[str]] = None
    source: Optional[str] = None
    rich_snippet: Optional[RichSnippet] = None

class Pagination(BaseModel):
    current: int
    next: Optional[HttpUrl] = None
    other_pages: Dict[str, HttpUrl]

class SerpApiPagination(BaseModel):
    current: int
    next_link: Optional[HttpUrl] = None
    next: Optional[HttpUrl] = None
    other_pages: Dict[str, HttpUrl]

class SerpResults(BaseModel):
    search_metadata: SearchMetadata
    search_parameters: SearchParameters
    search_information: SearchInformation
    organic_results: List[OrganicResult] = []
    pagination: Optional[Pagination] = None
    serpapi_pagination: Optional[SerpApiPagination] = None