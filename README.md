# 🏡 AI Real Estate Agent

🚀 **AI Real Estate Agent** is an **Apify Actor** that searches for real estate listings on Zillow based on user queries.  
It extracts ZIP codes using an **LLM (GPT-3.5-Turbo)** and fetches property listings using the **Zillow Scraper**.

---

## 📌 **Features**
✔ **Natural Language Search** – Users can input queries like:  
   _"Find a 2-bedroom apartment in San Francisco, CA, with a rent between $2000 and $4000."_  
✔ **LLM-Powered ZIP Code Extraction** – Extracts ZIP codes directly from the city/state.  
✔ **Zillow Scraper Integration** – Fetches listings for sale or rent.  
✔ **Custom Search Filters** – Supports price range, number of bedrooms, and amenities.  
✔ **Structured Output** – Provides a JSON response with property details.  

---

## 🚀 **How It Works**
1️⃣ **User Input:** _Natural language real estate query._  
2️⃣ **Extract Search Parameters:** _LLM extracts city, state, price, and amenities._  
3️⃣ **Get ZIP Codes:** _LLM finds relevant ZIP codes for the location._  
4️⃣ **Scrape Zillow Listings:** _Apify Zillow scraper retrieves matching properties._  
5️⃣ **Return Structured Results:** _JSON response with listings._  

---

## 📦 **Installation & Setup**
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ai-realestateagent.git
cd ai-realestateagent
```


### 2️⃣ Create a Virtual Environment (Optional)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Keys
Create a `.env` file and add your API keys:
```ini
OPENAI_API_KEY=your-openai-key
```

---

## 🎯 **How to Run Locally**
```bash
apify run --input-file=input.json
```
📜 **Example `input.json`**
```json
{
    "query": "Find a 2-bedroom apartment in San Francisco, CA, with a rent between $2000 and $4000."
}
```

---

## 🛠 **Project Structure**



ai-realestateagent/
│── src/
│   ├── main.py         # Apify Actor entry point
│   ├── tools.py        # LLM-powered search + Zillow scraper integration
│   ├── models.py       # Pydantic models for structured responses
│── .venv/              # Virtual environment (optional)
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
│── input.json          # Example input format
│── .env                # API keys (gitignore this file)

## Sample Report 

# 🏡 AI Real Estate Search Report

## 📍 Search Details
- **Query:** `Searching for a 2-bedroom apartment in San Francisco, CA, with a monthly rent between $2000 and $4000, and preferably featuring amenities such as parking and a gym.`

## 🔍 Results

### 🏠 NEMA
- **📍 Address:** [8 10th St, San Francisco, CA](https://www.zillow.com/apartments/san-francisco-ca/nema/CjpwdL/)
- **💰 Price:** N/A
- **🛏 Bedrooms:** N/A
- **🛁 Bathrooms:** N/A
- **📏 Area:** N/A sq ft
- **📅 Days on Zillow:** N/A
- **🖼 Image:** ![Listing Image](https://photos.zillowstatic.com/fp/f042533625b95dd94fd5f2d0cbeddd3c-p_e.jpg)
---

### 🏠 33 8th at Trinity Place
- **📍 Address:** [33 8th St, San Francisco, CA](https://www.zillow.com/apartments/san-francisco-ca/33-8th-at-trinity-place/CgrBS6/)
- **💰 Price:** N/A
- **🛏 Bedrooms:** N/A
- **🛁 Bathrooms:** N/A
- **📏 Area:** N/A sq ft
- **📅 Days on Zillow:** N/A
- **🖼 Image:** ![Listing Image](https://photos.zillowstatic.com/fp/01ae778a92392c6dcf1a5755615b23d2-p_e.jpg)
---

### 🏠 1190 Mission at Trinity Place
- **📍 Address:** [1190 Mission St, San Francisco, CA](https://www.zillow.com/apartments/san-francisco-ca/1190-mission-at-trinity-place/5XjVtb/)
- **💰 Price:** N/A
- **🛏 Bedrooms:** N/A
- **🛁 Bathrooms:** N/A
- **📏 Area:** N/A sq ft
- **📅 Days on Zillow:** N/A
- **🖼 Image:** ![Listing Image](https://photos.zillowstatic.com/fp/8e5f276f8c442bff35da5d46d96648cc-p_e.jpg)
---

### 🏠 AVA 55 Ninth
- **📍 Address:** [55 9th St, San Francisco, CA](https://www.zillow.com/apartments/san-francisco-ca/ava-55-ninth/5XkH8X/)
- **💰 Price:** N/A
- **🛏 Bedrooms:** N/A
- **🛁 Bathrooms:** N/A
- **📏 Area:** N/A sq ft
- **📅 Days on Zillow:** N/A
- **🖼 Image:** ![Listing Image](https://photos.zillowstatic.com/fp/2c16630f9cdfd68a247d85f4c04e4220-p_e.jpg)
---

### 🏠 1335 Folsom
- **📍 Address:** [1335 Folsom St, San Francisco, CA](https://www.zillow.com/apartments/san-francisco-ca/1335-folsom/CkCNP7/)
- **💰 Price:** N/A
- **🛏 Bedrooms:** N/A
- **🛁 Bathrooms:** N/A
- **📏 Area:** N/A sq ft
- **📅 Days on Zillow:** N/A
- **🖼 Image:** ![Listing Image](https://photos.zillowstatic.com/fp/3fcd39d054b56c6db83b623a49b212d0-p_e.jpg)
---


---
📌 *This report was generated automatically. Please verify details before making decisions.*
    