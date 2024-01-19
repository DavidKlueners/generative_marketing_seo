from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any, Optional


### Model for structured output chain
class SEOKeywords(BaseModel):
    """SEO keywords are words, that can be used in website content for SEO purposes."""

    seo_keywords: List[str] = Field(
        ...,
        description=(
            "SEO keywords are words, that can be used in website content for SEO purposes."
        ),
    )
