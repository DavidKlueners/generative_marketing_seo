from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any, Optional


### Models for structured output chain
class SEOKeywords(BaseModel):
    """SEO keywords are words, that can be used in website content for SEO purposes."""

    seo_keywords: List[str] = Field(
        ...,
        description=(
            "SEO keywords are words, that can be used in website content for SEO purposes."
        ),
    )


class SEOMetadata(BaseModel):
    """SEOMetadata represents the SEO title and description for a webpage or document."""

    seo_title: str = Field(
        ...,
        description="The SEO title is a concise summary of the content and is important for search engine rankings.",
    )
    seo_description: str = Field(
        ...,
        description="The SEO description provides a brief overview of the content, used in search engine results.",
    )

class ImprovedWebsiteContent(BaseModel):
    """ImprovedWebsiteContent represents a webpage's content after being optimized for SEO purposes."""

    improved_website_content: str = Field(
        ...,
        description="A markdown formatted string representing the webpage's content after SEO improvements."
    )