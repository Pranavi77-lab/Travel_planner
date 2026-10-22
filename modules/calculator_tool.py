from typing import Dict, Any, List

CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 155.0,
    "INR": 86.0,
    "AUD": 1.55,
    "CAD": 1.40,
    "SGD": 1.35
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "INR": "₹",
    "AUD": "A$",
    "CAD": "C$",
    "SGD": "S$"
}

class TravelBudgetCalculator:
    """
    Financial and Budget Calculator tool for 3-Day Travel Itineraries.
    Itemizes accommodation, dining, attractions, transport, and contingency buffer.
    """
    def __init__(self):
        pass

    def calculate_budget(
        self,
        total_budget: float,
        currency: str = "USD",
        travelers: int = 1,
        travel_style: str = "balanced",
        accommodation_per_night: float = 65.0,
        attractions_cost: float = 60.0,
        dining_cost_per_day: float = 35.0,
        transport_cost: float = 25.0,
        contingency_percent: float = 10.0
    ) -> Dict[str, Any]:
        """
        Calculates itemized breakdown, burn rates, and budget health for a 3-day trip.
        """
        currency = currency.upper()
        rate = CURRENCY_RATES.get(currency, 1.0)
        symbol = CURRENCY_SYMBOLS.get(currency, "$")
        travelers = max(1, travelers)

        # Style multiplier
        style_factors = {
            "budget": 0.75,
            "balanced": 1.0,
            "luxury": 1.8
        }
        factor = style_factors.get(travel_style.lower(), 1.0)

        # Calculations (in USD base)
        # Accommodation is for 3 nights (shared between couples if travelers > 1, or scaled)
        rooms_needed = (travelers + 1) // 2 if travelers > 1 else 1
        total_accommodation_usd = (accommodation_per_night * factor) * 3 * rooms_needed

        # Food & dining: 3 days * travelers
        total_dining_usd = (dining_cost_per_day * factor) * 3 * travelers

        # Attractions: per person * travelers
        total_attractions_usd = attractions_cost * travelers

        # Transportation: 3-day transit pass + airport transfer per person
        total_transport_usd = transport_cost * travelers

        subtotal_usd = total_accommodation_usd + total_dining_usd + total_attractions_usd + total_transport_usd
        
        # Contingency emergency reserve (10% standard)
        contingency_usd = subtotal_usd * (contingency_percent / 100.0)
        grand_total_usd = subtotal_usd + contingency_usd

        # Convert to user's selected currency
        total_budget_converted = total_budget
        budget_usd = total_budget / rate

        grand_total_user = grand_total_usd * rate
        accommodation_user = total_accommodation_usd * rate
        dining_user = total_dining_usd * rate
        attractions_user = total_attractions_usd * rate
        transport_user = total_transport_usd * rate
        contingency_user = contingency_usd * rate

        variance_user = total_budget_converted - grand_total_user
        variance_usd = budget_usd - grand_total_usd

        # Budget health evaluation
        if variance_user >= (total_budget_converted * 0.15):
            status = "Comfortable Surplus"
            badge = "success"
            message = f"You have {symbol}{round(variance_user, 2):,} remaining! You can upgrade your dining or book an extra excursion."
        elif variance_user >= 0:
            status = "Within Budget"
            badge = "info"
            message = f"Optimally balanced trip. Remaining buffer: {symbol}{round(variance_user, 2):,}."
        elif abs(variance_user) <= (total_budget_converted * 0.15):
            status = "Slightly Over Budget"
            badge = "warning"
            message = f"Exceeds budget by {symbol}{round(abs(variance_user), 2):,}. Consider switching to budget dining or public transit passes."
        else:
            status = "Over Budget"
            badge = "danger"
            message = f"Exceeds budget by {symbol}{round(abs(variance_user), 2):,}. Adjust accommodation or travel style to fit comfortably."

        daily_spend_user = grand_total_user / 3.0
        per_person_total_user = grand_total_user / travelers

        categories = [
            {"category": "Accommodation (3 Nights)", "amount": round(accommodation_user, 2), "percent": round((accommodation_user / grand_total_user) * 100, 1), "color": "#3B82F6"},
            {"category": "Dining & Street Food (3 Days)", "amount": round(dining_user, 2), "percent": round((dining_user / grand_total_user) * 100, 1), "color": "#10B981"},
            {"category": "Attractions & Entry Tickets", "amount": round(attractions_user, 2), "percent": round((attractions_user / grand_total_user) * 100, 1), "color": "#F59E0B"},
            {"category": "Local Transit & Metro Passes", "amount": round(transport_user, 2), "percent": round((transport_user / grand_total_user) * 100, 1), "color": "#8B5CF6"},
            {"category": f"Emergency Contingency ({int(contingency_percent)}%)", "amount": round(contingency_user, 2), "percent": round((contingency_user / grand_total_user) * 100, 1), "color": "#EC4899"}
        ]

        return {
            "currency": currency,
            "currency_symbol": symbol,
            "total_budget": round(total_budget_converted, 2),
            "grand_total": round(grand_total_user, 2),
            "variance": round(variance_user, 2),
            "is_within_budget": variance_user >= 0,
            "status": status,
            "status_badge": badge,
            "message": message,
            "daily_burn_rate": round(daily_spend_user, 2),
            "per_person_total": round(per_person_total_user, 2),
            "travelers_count": travelers,
            "breakdown": categories
        }
