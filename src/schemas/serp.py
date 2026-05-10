"""Pydantic models for the SerpAPI Google-search JSON response.

Only ``organic_results`` is consumed by the rest of the codebase, but we
declare the surrounding envelope so we can opt into stricter validation later.
All non-essential fields are ``Optional`` because SerpAPI responses vary
depending on the query.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, HttpUrl


class DetectedExtensions(BaseModel):
    """Structured price/rating data extracted by SerpAPI."""

    price: Optional[float] = None
    currency: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None


class Bottom(BaseModel):
    """The lower section of a Google rich snippet."""

    detected_extensions: Optional[DetectedExtensions] = None
    extensions: Optional[List[str]] = None


class RichSnippet(BaseModel):
    """A Google rich snippet attached to an organic result."""

    bottom: Optional[Bottom] = None


class OrganicResult(BaseModel):
    """One organic result row from SerpAPI."""

    position: int
    title: str
    link: Optional[HttpUrl] = None
    redirect_link: Optional[HttpUrl] = None
    displayed_link: Optional[str] = None
    favicon: Optional[HttpUrl] = None
    snippet: Optional[str] = None
    snippet_highlighted_words: Optional[List[str]] = None
    source: Optional[str] = None
    rich_snippet: Optional[RichSnippet] = None


class Pagination(BaseModel):
    """Google-style pagination block."""

    current: int
    next: Optional[HttpUrl] = None
    other_pages: Dict[str, HttpUrl] = {}


class SerpApiPagination(BaseModel):
    """SerpAPI's own pagination block (different shape from Google's)."""

    current: int
    next_link: Optional[HttpUrl] = None
    next: Optional[HttpUrl] = None
    other_pages: Dict[str, HttpUrl] = {}


class SerpResults(BaseModel):
    """Top-level SerpAPI response envelope.

    The metadata blocks that used to live on this class are dropped because
    we never read them and SerpAPI's exact field set varies by query.
    """

    organic_results: List[OrganicResult] = []
    pagination: Optional[Pagination] = None
    serpapi_pagination: Optional[SerpApiPagination] = None
