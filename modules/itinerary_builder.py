from typing import Dict, Any, List
from .vector_store import TravelVectorStore
from .weather_tool import WeatherTool
from .places_tool import PlacesTool
from .calculator_tool import TravelBudgetCalculator
from .knowledge_base import generate_dynamic_city_data

class ItineraryBuilder:
    """
    Synthesizes FAISS vector retrieval, live Weather API, Places API, and
    Budget Calculator into a cohesive 3-day travel itinerary.
    """
    def __init__(self, vector_store: TravelVectorStore, weather_tool: WeatherTool, places_tool: PlacesTool, calculator: TravelBudgetCalculator):
        self.vector_store = vector_store
        self.weather_tool = weather_tool
        self.places_tool = places_tool
        self.calculator = calculator

    def build_itinerary(
        self,
        destination: str,
        total_budget: float,
        currency: str = "USD",
        travel_style: str = "balanced",
        interests: List[str] = None,
        travelers: int = 1
    ) -> Dict[str, Any]:
        destination = destination.strip()
        interests = interests or ["Culture", "Sightseeing", "Food"]

        # 1. Geocode & Fetch Live Weather
        geo_info = self.places_tool.geocode(destination)
        lat = geo_info["lat"] if geo_info else None
        lon = geo_info["lon"] if geo_info else None
        
        weather_data = self.weather_tool.get_weather(destination, lat=lat, lon=lon)
        dest_lat = weather_data.get("latitude", 48.8566)
        dest_lon = weather_data.get("longitude", 2.3522)

        # 2. Vector Retrieval with FAISS (using nomic-embed-text)
        query = f"3-day trip in {destination} within budget for {travel_style} traveler interested in {', '.join(interests)}"
        retrieved_docs = self.vector_store.search(query, top_k=10, destination_filter=destination)

        # If few or no results found, dynamically generate & index travel documents for this city
        if len(retrieved_docs) < 4:
            dynamic_docs = generate_dynamic_city_data(destination)
            self.vector_store.add_documents(dynamic_docs, persist=True)
            retrieved_docs = self.vector_store.search(query, top_k=10, destination_filter=destination)

        # 3. Fetch Map Places & POIs
        places_list = self.places_tool.get_city_places(destination, dest_lat, dest_lon)

        # 4. Partition retrieved docs into Days 1, 2, 3 and general
        day_buckets = {1: [], 2: [], 3: []}
        general_docs = []

        for doc in retrieved_docs:
            d_num = doc.get("day")
            if d_num in [1, 2, 3]:
                day_buckets[d_num].append(doc)
            else:
                general_docs.append(doc)

        # Fill any missing days from dynamic fallback to ensure complete 3-day coverage
        dyn_backup = generate_dynamic_city_data(destination)
        for backup_doc in dyn_backup:
            b_day = backup_doc.get("day")
            if b_day in [1, 2, 3] and len(day_buckets[b_day]) < 3:
                day_buckets[b_day].append(backup_doc)

        # 5. Build Day-by-Day Itinerary structure with Weather Adaptation
        days_forecast = weather_data.get("forecast", [])
        itinerary_days = []
        total_attraction_costs_usd = 0

        slot_times = ["Morning (09:00 - 12:30)", "Afternoon (14:00 - 17:30)", "Evening & Dinner (18:30 - 21:30)"]

        for day_num in [1, 2, 3]:
            day_forecast = days_forecast[day_num - 1] if len(days_forecast) >= day_num else {}
            is_rainy = day_forecast.get("is_rainy", False)
            day_items = day_buckets.get(day_num, [])[:3]

            activities = []
            day_cost = 0

            for slot_idx, item in enumerate(day_items):
                slot_label = slot_times[slot_idx] if slot_idx < len(slot_times) else "Night Event"
                cost = float(item.get("cost_usd", 10))
                day_cost += cost
                total_attraction_costs_usd += cost

                # Weather adaptation notice
                activity_note = ""
                if is_rainy and "outdoor" in [t.lower() for t in item.get("tags", [])]:
                    activity_note = "🌦️ Weather Notice: Rain expected today; indoor exhibits & covered walkways recommended."

                activities.append({
                    "time_slot": slot_label,
                    "title": item.get("title", f"Explore {destination}"),
                    "category": item.get("category", "Attraction"),
                    "description": item.get("content", ""),
                    "cost_usd": cost,
                    "note": activity_note,
                    "tags": item.get("tags", [])
                })

            # Calculate transit recommendation for the day
            transit_tip = f"Use local metro/tram 24h pass (~$6) or explore central {destination} on foot."

            itinerary_days.append({
                "day_number": day_num,
                "title": f"Day {day_num}: {self._get_day_theme(day_num, destination)}",
                "weather": day_forecast,
                "activities": activities,
                "estimated_day_cost_usd": day_cost,
                "transit_tip": transit_tip
            })

        # 6. Budget Calculator Tool execution
        calc_result = self.calculator.calculate_budget(
            total_budget=total_budget,
            currency=currency,
            travelers=travelers,
            travel_style=travel_style,
            accommodation_per_night=45.0 if travel_style == "budget" else (85.0 if travel_style == "balanced" else 180.0),
            attractions_cost=total_attraction_costs_usd,
            dining_cost_per_day=25.0 if travel_style == "budget" else (45.0 if travel_style == "balanced" else 95.0),
            transport_cost=20.0,
            contingency_percent=10.0
        )

        return {
            "destination": destination,
            "coordinates": {"lat": dest_lat, "lon": dest_lon},
            "travel_style": travel_style,
            "travelers": travelers,
            "interests": interests,
            "days": itinerary_days,
            "budget": calc_result,
            "weather": weather_data,
            "places": places_list,
            "vector_search_audit": [
                {
                    "title": d.get("title"),
                    "category": d.get("category"),
                    "score": round(d.get("score", 0.0), 4),
                    "tags": d.get("tags", []),
                    "content_snippet": d.get("content", "")[:120] + "..."
                }
                for d in retrieved_docs[:6]
            ]
        }

    def _get_day_theme(self, day_num: int, city: str) -> str:
        themes = {
            1: f"Historic Landmarks & Cultural Foundations",
            2: f"Neighborhood Exploration, Panoramas & Local Delights",
            3: f"Iconic Treasures, Artisan Markets & Farewell Evening"
        }
        return themes.get(day_num, f"Exploring {city}")
