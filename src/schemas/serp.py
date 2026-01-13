from typing import List, Optional

from pydantic import BaseModel

class Extensions(BaseModel):
    price: Optional[float] = None
    currency: Optional[str] = None

class Bottom(BaseModel):
    detected_extensions: Optional[Extensions] = None
class RichSnippet(BaseModel):
    bottom: Optional[Bottom] = None

class OrganicResults(BaseModel):
    position:int
    title:str
    snippet:str
    rich_snippet: Optional[RichSnippet] = None
class SerpResults(BaseModel):
    organic_results: List[OrganicResults] = []