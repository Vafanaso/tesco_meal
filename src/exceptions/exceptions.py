"""Project-specific exceptions."""


class InvalidSearchResult(Exception):
    """Raised when SerpAPI returns no usable organic results for a query."""
