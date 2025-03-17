import asyncio
import json
import logging
from apify import Actor
from src.tools import search_real_estate
from src.models import RealEstateQueryState
from src.ppe_utils import charge_for_actor_start

#  Configure Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def save_report(state):
    """Save the real estate search report in markdown format & store in Apify KV Store."""
    report_content = f"""# 🏡 AI Real Estate Search Report

## 📍 Search Details
- **Query:** `{state.get("query", "N/A")}`

## 🔍 Results
{format_listings(state.get("listings", []))}

---
📌 *This report was generated automatically. Please verify details before making decisions.*
    """

    #  Store report in Apify Key-Value Store
    store = await Actor.open_key_value_store()
    await store.set_value("report.md", report_content)
    Actor.log.info('Saved the "report.md" file into the key-value store!')

def format_listings(listings):
    """Format Zillow listings into markdown."""
    if not listings:
        return "**No properties found matching your criteria.**"

    formatted_listings = ""
    for listing in listings[:5]:  # Limit to top 5 results
        formatted_listings += f"""
### 🏠 {listing.get("statusText", "Property for Sale/Rent")}
- **📍 Address:** [{listing.get("address", "N/A")}]({listing.get("detailUrl", "#")})
- **💰 Price:** {listing.get("price", "N/A")}
- **🛏 Bedrooms:** {listing.get("beds", "N/A")}
- **🛁 Bathrooms:** {listing.get("baths", "N/A")}
- **📏 Area:** {listing.get("area", "N/A")} sq ft
- **📅 Days on Zillow:** {listing.get("variableData", {}).get("text", "N/A")}
- **🖼 Image:** ![Listing Image]({listing.get("imgSrc", "#")})
---
"""
    return formatted_listings

async def main():
    """Runs the AI Real Estate search workflow."""
    async with Actor:
        actor_input = await Actor.get_input() or {}
        logger.info(f"Received input: {actor_input}")
        
        count = (Actor.get_env()['memory_mbytes'] or 1024 + 1023) // 1024
        await Actor.charge(event_name='actor-start-gb', count=count)

        #  Initialize State
        real_estate_query = RealEstateQueryState(**actor_input)

        #  Execute search
        final_state = search_real_estate(real_estate_query.query)
        logger.info(f"Workflow completed. Final state: {final_state}")

        #  Save the final report
        await save_report(final_state)

        #  Push data to Apify dataset
        await Actor.push_data(final_state)

if __name__ == "__main__":
    asyncio.run(main())
