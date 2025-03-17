import json
from apify_client import ApifyClient
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from apify import Actor
import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)

# Zillow Scraper Actor ID
ZILLOW_ACTOR_ID = "maxcopell/zillow-zip-search"

# Initialize Apify Client
apify_client = ApifyClient(APIFY_TOKEN)


#  Step 1: Extract City & State
def extract_city_state(query: str) -> str:
    """Extracts city and state from a user query using LLM."""
    Actor.log.info(f"Extracting city and state from query: {query}")

    location_prompt = ChatPromptTemplate.from_template("""
        Extract the city and state from the following real estate query:
        ---
        **Query**: {query}  

        Return only the city and state in the format: "City, State" (e.g., "San Francisco, CA").
    """)

    response = location_prompt | llm
    extracted_location = response.invoke({"query": query}).content.strip()

    if not extracted_location or "," not in extracted_location:
        Actor.log.error(f"Invalid city/state extracted: {extracted_location}")
        return ""

    Actor.log.info(f"Extracted city & state: {extracted_location}")
    return extracted_location


#  Step 2: Get ZIP Codes using LLM
#  Step 2: Get ZIP Codes using LLM
def get_zip_codes(city_state: str) -> list:
    """Uses LLM to extract ZIP codes for a given city & state."""
    if not city_state:
        Actor.log.error("No city/state provided for ZIP code lookup.")
        return []

    Actor.log.info(f"Fetching ZIP codes for {city_state} using LLM")

    zip_prompt = ChatPromptTemplate.from_template("""
        Provide exactly **2 ZIP codes** for the given city and state.
        ---
        **City & State**: {city_state}

        **Return a valid JSON list, exactly like this:**
        ```
        ["94102", "94103"]
        ```
    """)

    response = zip_prompt | llm
    extracted_zip_codes = response.invoke({"city_state": city_state}).content.strip()

    # 🔹 Log the raw response before parsing
    Actor.log.info(f"Raw ZIP code response: {extracted_zip_codes}")

    try:
        zip_codes = json.loads(extracted_zip_codes)

        #  Validate that it's a list of strings
        if isinstance(zip_codes, list) and all(isinstance(zip, str) for zip in zip_codes):
            zip_codes = zip_codes[:2]  #  Limit to 2 ZIP codes
            Actor.log.info(f"Selected ZIP codes: {zip_codes}")
            return zip_codes
        else:
            Actor.log.error("Invalid ZIP code format received from LLM.")
    except json.JSONDecodeError:
        Actor.log.error("Failed to parse ZIP codes from LLM response.")

    return []


#  Step 3: Extract Search Parameters from Query
def extract_search_params(query: str) -> dict:
    """Extracts structured real estate search parameters from a user query."""
    Actor.log.info(f"Extracting search parameters from query: {query}")

    city_state = extract_city_state(query)
    if not city_state:
        Actor.log.error("City/state extraction failed, aborting search parameters extraction.")
        return {}

    prompt = ChatPromptTemplate.from_template("""
        Extract structured real estate search parameters from the query.
        ---
        **User Query**: {query}  
        **Extracted City & State**: {city_state}  

        Return a JSON object with:
        - price_min (int)
        - price_max (int)
        - bedrooms (int)
        - amenities (list of strings)
    """)

    response = prompt | llm
    extracted_params = response.invoke({"query": query, "city_state": city_state}).content

    try:
        parsed_params = json.loads(extracted_params)
        Actor.log.info(f"Extracted parameters: {parsed_params}")
        return {"city_state": city_state, **parsed_params}
    except json.JSONDecodeError:
        Actor.log.error("Failed to parse extracted parameters.")
        return {}


#  Step 4: Fetch Zillow Listings Using ApifyClient
def search_real_estate(query: str) -> dict:
    """Searches Zillow properties using ApifyClient based on extracted search parameters."""
    Actor.log.info(f"Starting real estate search for query: {query}")

    params = extract_search_params(query)
    if not params or "city_state" not in params:
        return {"error": "Invalid search query"}

    zip_codes = get_zip_codes(params["city_state"])
    if not zip_codes:
        return {"error": "No ZIP codes found for location"}

    # Prepare Zillow Scraper input
    zillow_input = {
        "zipCodes": zip_codes,
        "priceMax": params.get("price_max", ""),
        "priceMin": params.get("price_min", ""),
        "forRent": True,  # Searching for rentals
        "forSaleByAgent": False,
        "forSaleByOwner": False,
        "sold": False,
    }

    Actor.log.info(f"Running Zillow Scraper with input: {zillow_input}")

    try:
        run = apify_client.actor(ZILLOW_ACTOR_ID).call(run_input=zillow_input)
        listings = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())

        Actor.log.info(f"Total properties found: {len(listings)}")
        return {"query": query, "listings": listings}
    except Exception as e:
        Actor.log.error(f"Error fetching data from Zillow scraper: {str(e)}")
        return {"error": "Failed to fetch Zillow listings"}
