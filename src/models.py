from pydantic import BaseModel, Field
from typing import List, Optional

class RealEstateQueryState(BaseModel):
    """State model for real estate search queries."""
    query: str = Field(..., description="User's natural language query for real estate search.")
    city_state: Optional[str] = Field(None, description="Extracted city and state from the query.")
    zip_codes: List[str] = Field(default_factory=list, description="List of ZIP codes for search.")
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms specified in the query.")
    price_min: Optional[int] = Field(None, description="Minimum price/rent range from the query.")
    price_max: Optional[int] = Field(None, description="Maximum price/rent range from the query.")
    amenities: List[str] = Field(default_factory=list, description="List of preferred amenities.")
    listings: List[dict] = Field(default_factory=list, description="List of real estate property results.")

    def dict(self, **kwargs):
        """Override dict() to filter out None values when serializing."""
        return {k: v for k, v in super().dict(**kwargs).items() if v is not None}
