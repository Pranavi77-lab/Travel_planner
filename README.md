# Project 7: Travel Planning Assistant

An AI-powered, interactive 3-day travel itinerary planning application designed to craft optimized journeys within a traveler's budget. Built with **FAISS vector database**, **nomic-embed-text** embeddings (768 dimensions), **live Open-Meteo Weather API**, **OpenStreetMap Places API**, and an interactive financial budget calculator.

---

## 🌟 Key Features

1. **Vector Database with FAISS (`faiss-cpu`)**:
   - Indexed using Inner Product on L2-normalized dense embeddings (`faiss.IndexFlatIP`) for exact cosine similarity.
   - Embeds destination highlights, cultural points of interest, budget dining spots, hotels, and transit recommendations.
   - Includes a **FAISS Vector DB Inspector & Sandbox** in the UI to inspect retrieved chunks and similarity percentages.

2. **Embedding Model (`nomic-embed-text`)**:
   - Produces 768-dimensional dense vector embeddings.
   - Multi-tier resilient support:
     * Nomic API via official `nomic` SDK / key
     * Local Ollama (`nomic-embed-text`)
     * High-fidelity 768-dim deterministic semantic projection fallback for 100% offline reliability.

3. **Live Weather API (Open-Meteo)**:
   - Live 3-day forecast with temperatures (°C and °F), weather codes, conditions, and precipitation probability.
   - Weather adaptation logic: Automatically flags rainy days and advises indoor museums/activities vs. sunny rooftop viewpoints.
   - Smart packing & clothing suggestions based on temperature and rain probability.

4. **Places API (OpenStreetMap Nominatim & Overpass)**:
   - Live geocoding of destinations.
   - Interactive Leaflet.js map with color-coded day pins (Day 1: Blue, Day 2: Emerald, Day 3: Amber), popups with costs, and route polyline.

5. **Financial Budget Calculator**:
   - Itemized breakdown: Accommodation (3 nights), Dining (3 days), Attractions & Passes, Local Transit, and 10% Emergency Contingency buffer.
   - Real-time interactive sliders allowing travelers to tweak expenses and watch the budget re-balance live with a Chart.js doughnut chart.
   - Multi-currency support: USD, EUR, GBP, JPY, INR, AUD, CAD.
   - Burn rate and per-person cost calculations.

6. **Interactive UI & Export**:
   - Single-page application styled with Tailwind CSS and glassmorphism.
   - 1-Click popular city presets (Tokyo, Paris, Rome, NYC, Bali, London) plus support for **any** city worldwide!
   - Export to PDF / Print-friendly travel guide and 1-click clipboard copy.

---

## 🚀 Quick Start

### 1. Requirements
Ensure Python 3.10+ is installed. Dependencies:
```bash
pip install -r requirements.txt
```
*(Dependencies include `flask`, `flask-cors`, `faiss-cpu`, `nomic`, `requests`, `numpy`, `pydantic`)*

### 2. Run the Application
In your terminal:
```bash
python app.py
```
Or double-click `run.bat` (Windows).

### 3. Open in Browser
Visit:
```
http://127.0.0.1:5000
```

---

## 📂 Project Architecture

```
travel_planning_assistant/
├── app.py                      # Flask REST API and web application server
├── requirements.txt            # Python dependencies
├── run.bat                     # 1-click Windows start script
├── run.ps1                     # PowerShell start script
├── README.md                   # Documentation
├── modules/
│   ├── embeddings.py           # nomic-embed-text wrapper (768-dim)
│   ├── vector_store.py         # FAISS vector store with cosine search
│   ├── weather_tool.py         # Live Open-Meteo weather API tool
│   ├── places_tool.py          # Geocoding & POI places tool
│   ├── calculator_tool.py      # Budget breakdown & financial analytics
│   ├── itinerary_builder.py    # Multi-tool synthesizer engine
│   └── knowledge_base.py       # Curated & dynamic travel records
├── templates/
│   └── index.html              # Modern, responsive single-page dashboard
└── static/
    ├── css/
    │   └── custom.css          # Glassmorphism, animations, print styling
    └── js/
        └── app.js              # Leaflet map, Chart.js, sliders, reactive UI
```
