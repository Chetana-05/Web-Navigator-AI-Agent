
# Web Navigator AI Agent

A simple web automation agent that searches for products on e-commerce websites using local AI and browser automation. This project demonstrates how to combine a local language model with web scraping to create an intelligent shopping assistant.

## Team Information

- **Team Name:** AgentXplorer
- **Team Members:** K. Chetana, M. Anusha, M. Pujitha, G. Ramya, A. Sowmya

## What This Project Does

The agent takes a simple instruction like "search for laptops under 50k" and automatically:
1. Opens a web browser
2. Visits Amazon and Flipkart
3. Searches for the requested products
4. Extracts product details (names, prices, specifications)
5. Returns a structured list of results

## Technical Overview

- **AI Planning**: Uses Ollama (local LLM) to understand instructions and plan actions
- **Browser Control**: Uses Playwright to automate web browsing
- **Data Extraction**: Scrapes product information from e-commerce sites
- **Output Format**: Returns results as structured JSON data

## Prerequisites

Before running this project, you need:

### 1. Python Installation
- Python 3.10 or higher
- pip package manager

### 2. Ollama Setup
Download and install Ollama from: https://ollama.com/download

After installation:
```bash
# Start Ollama server
ollama serve

# Download a model (in a new terminal)
ollama pull phi3
```

### 3. Project Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Installation Steps

1. **Clone or download this project**
2. **Open terminal/command prompt in the project folder**
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Playwright browser**:
   ```bash
   python -m playwright install chromium
   ```
5. **Start Ollama server**:
   ```bash
   ollama serve
   ```
6. **Download a model** (in new terminal):
   ```bash
   ollama pull phi3
   ```

## How to Run

### Basic Usage
```bash
python -m web_agent.cli --goal "search for laptops under 50k and list top 5"
```

### Command Options
- `--goal`: Your search instruction (required)
- `--model`: Ollama model to use (default: phi3)
- `--headed`: Show browser window (default: headless)
- `--max-steps`: Maximum planning steps (default: 12)

### Example Commands
```bash
# Search for laptops under 50000
python -m web_agent.cli --goal "search for laptops under 50k and list top 5" --model phi3 --headed

# Search for phones under 30000
python -m web_agent.cli --goal "find smartphones under 30000" --model phi3

# Search for gaming laptops
python -m web_agent.cli --goal "search for gaming laptops under 60000" --model phi3 --headed
```

## Project Structure

```
web_agent/
├── __init__.py          # Package initialization
├── agent.py             # Main agent coordination
├── browser.py           # Browser automation
├── cli.py               # Command line interface
├── extractors.py        # Web scraping functions
├── ollama_client.py     # AI model communication
└── planner.py           # Task planning logic
```

## How It Works

1. **Input Processing**: Takes your natural language instruction
2. **AI Planning**: Uses local LLM to understand what you want
3. **Browser Automation**: Opens browser and navigates to websites
4. **Data Extraction**: Finds and extracts product information
5. **Result Formatting**: Organizes data into structured JSON output

## Example Output

When you search for laptops, the agent returns:
```json
{
  "status": "ok",
  "result": {
    "goal": "search for laptops under 50k and list top 5",
    "total_products": 3,
    "products": [
      {
        "title": "HP 15, 13th Gen Intel Core i5-1334U...",
        "price": "50,990",
        "site": "Amazon"
      }
    ],
    "sites_visited": ["amazon.in", "flipkart.com"]
  }
}
```

## Output Screenshots

The following screenshots demonstrate the agent's operation when searching for laptops under 50,000:

### Amazon Search Results Page

The agent navigates to Amazon India and performs a search for "laptops under 50000". The screenshot shows the search results page with various laptop listings and filtering options.

**Key Features Visible:**
- Browser address bar shows: `amazon.in/s?k=laptops+under+50000`
- Search results display "1-16 of over 3,000 results for 'laptops under 50000'"
- Left sidebar contains filters for:
  - Deals & Discounts (Great Indian Festival)
  - Delivery Day options
  - Brands (HP, ASUS, Lenovo, Dell, acer, amazon basics, Portronics)
  - RAM Size (16 GB, 8 GB, 4 GB)
- Main content area features "Bestseller HP laptops with intel core 13th gen" section
- Product listings show:
  - HP OmniBook 5: ₹54,990.00 (originally ₹81,202.00, -32% off) with 4-star rating
  - HP 15, 13th Gen Intel Core i5-1334U: ₹50,990.00 (originally ₹73,920.00) with 3.7-star rating
- Both products are "prime" eligible
- "Great Indian Festival Live now" banner is visible

### Flipkart Search Results Page

The agent also visits Flipkart and searches for "laptops under 50000". The screenshot shows the Flipkart search results page with comprehensive filtering options.

**Key Features Visible:**
- Browser address bar shows: `flipkart.com/search?q=laptops+under+50000`
- Search results display "Showing 1-24 of 2,723 results for 'laptops under 50000'"
- Left sidebar contains filters for:
  - CATEGORIES (Computers > Laptops)
  - PRICE filter with slider control
  - BRAND options
  - TYPE options
  - PROCESSOR options (Core i5, Core i3)
- Main content area shows:
  - Breadcrumb navigation: "Home > Computers > Laptops"
  - Sort options: Relevance, Popularity, Price (Low to High), Price (High to Low), Newest First
- Product listings include:
  - Acer Aspire 3: ₹35,989 (originally ₹66,999, 46% off) with 4.3-star rating
  - DELL 15 AMD Ryzen 5: ₹39,990 (originally ₹56,919, 29% off) with 4.3-star rating
- Products show "Flipkart Assured" badges and exchange offers
- "Top Discount of the Sale" tags are visible

These screenshots demonstrate the agent's successful navigation to both major e-commerce platforms and its ability to extract product information from the search results pages.

## Troubleshooting

### Common Issues

1. **Ollama not running**
   - Solution: Start Ollama server with `ollama serve`

2. **Browser fails to launch**
   - Solution: Reinstall Playwright browsers with `python -m playwright install chromium`

3. **No products found**
   - Some websites may block automated access
   - Try different search terms or wait a few minutes

4. **Model not found**
   - Download the model with `ollama pull phi3`

### Getting Help

If you encounter issues:
1. Check that Ollama server is running
2. Verify Python dependencies are installed
3. Ensure Playwright browsers are installed
4. Try running with `--headed` to see browser behavior

## Learning Objectives

This project teaches:
- Web automation with Playwright
- Local AI integration with Ollama
- Web scraping and data extraction
- Command line interface development
- Python async programming
- JSON data handling

## Next Steps

To extend this project:
1. Add more e-commerce websites
2. Implement product comparison features
3. Add price tracking capabilities
4. Create a web interface
5. Add more search categories

## License

This project is for educational purposes. Please respect website terms of service when scraping data.