import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from modules.embeddings import NomicEmbeddingProvider, EMBEDDING_DIM
from modules.vector_store import TravelVectorStore
from modules.weather_tool import WeatherTool
from modules.places_tool import PlacesTool
from modules.calculator_tool import TravelBudgetCalculator
from modules.itinerary_builder import ItineraryBuilder
from modules.knowledge_base import CURATED_TRAVEL_DATA

app = Flask(__name__)
CORS(app)

# Initialize Core AI & Vector Stack
print("[App] Initializing Nomic Embedding Provider...")
embedding_provider = NomicEmbeddingProvider()
print(f"[App] Embedding mode: {embedding_provider.provider_mode} (dim: {EMBEDDING_DIM})")

print("[App] Initializing FAISS Vector Store...")
vector_store = TravelVectorStore(embedding_provider=embedding_provider)

# Seed initial knowledge if empty
if vector_store.total_documents() == 0:
    print(f"[App] Seeding {len(CURATED_TRAVEL_DATA)} curated travel records into FAISS...")
    vector_store.add_documents(CURATED_TRAVEL_DATA, persist=True)

# Initialize Tools
weather_tool = WeatherTool()
places_tool = PlacesTool()
calculator = TravelBudgetCalculator()
itinerary_builder = ItineraryBuilder(vector_store, weather_tool, places_tool, calculator)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/destinations", methods=["GET"])
def get_destinations():
    presets = [
        {"city": "Tokyo", "country": "Japan", "budget": 950, "currency": "USD", "vibe": "Futuristic & Cultural", "tag": "Popular", "img": "tokyo"},
        {"city": "Paris", "country": "France", "budget": 850, "currency": "EUR", "vibe": "Romance & Art", "tag": "Top Pick", "img": "paris"},
        {"city": "Rome", "country": "Italy", "budget": 700, "currency": "EUR", "vibe": "Ancient History & Pasta", "tag": "Historic", "img": "rome"},
        {"city": "New York", "country": "USA", "budget": 1200, "currency": "USD", "vibe": "Skyline & Broadway", "tag": "Iconic", "img": "nyc"},
        {"city": "Bali", "country": "Indonesia", "budget": 450, "currency": "USD", "vibe": "Tropical & Waterfalls", "tag": "Budget Friendly", "img": "bali"},
        {"city": "London", "country": "UK", "budget": 800, "currency": "GBP", "vibe": "Royal & Museums", "tag": "Classic", "img": "london"}
    ]
    return jsonify({"destinations": presets})

@app.route("/api/plan", methods=["POST"])
def plan_trip():
    data = request.get_json() or {}
    destination = data.get("destination", "Tokyo")
    total_budget = float(data.get("budget", 1000))
    currency = data.get("currency", "USD")
    travel_style = data.get("travel_style", "balanced")
    travelers = int(data.get("travelers", 1))
    interests = data.get("interests", ["Culture", "Sightseeing", "Food"])

    try:
        itinerary = itinerary_builder.build_itinerary(
            destination=destination,
            total_budget=total_budget,
            currency=currency,
            travel_style=travel_style,
            interests=interests,
            travelers=travelers
        )
        return jsonify({"success": True, "data": itinerary})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "Tokyo")
    result = weather_tool.get_weather(city)
    return jsonify(result)

@app.route("/api/places", methods=["GET"])
def get_places():
    city = request.args.get("city", "Tokyo")
    geo = places_tool.geocode(city)
    lat = geo["lat"] if geo else 35.6762
    lon = geo["lon"] if geo else 139.6503
    places = places_tool.get_city_places(city, lat, lon)
    return jsonify({"city": city, "center": {"lat": lat, "lon": lon}, "places": places})

@app.route("/api/calculator", methods=["POST"])
def run_calculator():
    data = request.get_json() or {}
    total_budget = float(data.get("budget", 1000))
    currency = data.get("currency", "USD")
    travelers = int(data.get("travelers", 1))
    travel_style = data.get("travel_style", "balanced")
    acc_per_night = float(data.get("acc_per_night", 65))
    attractions = float(data.get("attractions", 60))
    dining = float(data.get("dining_per_day", 35))
    transport = float(data.get("transport", 25))
    contingency = float(data.get("contingency_percent", 10))

    calc_res = calculator.calculate_budget(
        total_budget=total_budget,
        currency=currency,
        travelers=travelers,
        travel_style=travel_style,
        accommodation_per_night=acc_per_night,
        attractions_cost=attractions,
        dining_cost_per_day=dining,
        transport_cost=transport,
        contingency_percent=contingency
    )
    return jsonify(calc_res)

@app.route("/api/vector-search", methods=["POST"])
def vector_search():
    data = request.get_json() or {}
    query = data.get("query", "budget attractions")
    top_k = int(data.get("top_k", 5))
    dest_filter = data.get("destination", None)

    results = vector_store.search(query, top_k=top_k, destination_filter=dest_filter)
    return jsonify({
        "query": query,
        "results": results,
        "total_indexed": vector_store.total_documents(),
        "embedding_model": "nomic-embed-text (768-dim)"
    })

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "total_documents": vector_store.total_documents(),
        "vector_dimensions": EMBEDDING_DIM,
        "index_type": "faiss.IndexFlatIP",
        "embedding_provider": embedding_provider.provider_mode,
        "model": "nomic-embed-text-v1.5"
    })

if __name__ == "__main__":
    print("[App] Server starting on http://127.0.0.1:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=False)
