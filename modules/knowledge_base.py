from typing import List, Dict, Any

# Curated high-fidelity travel data for initial FAISS indexing
CURATED_TRAVEL_DATA: List[Dict[str, Any]] = [
    # ==================== TOKYO, JAPAN ====================
    {
        "id": "tokyo_overview",
        "destination": "Tokyo",
        "category": "Destination",
        "day": None,
        "title": "Tokyo Budget & Travel Overview",
        "content": "Tokyo is vibrant, clean, and surprisingly budget-friendly if using the 72-hour Tokyo Subway Ticket ($10) and eating at authentic ramen-ya or conveyor belt sushi ($7-$12 per meal). Hostels in Asakusa or Shinjuku capsule hotels cost $35-$55/night, mid-range hotels $80-$130/night.",
        "cost_usd": 0,
        "tags": ["overview", "budget", "japan", "transit"]
    },
    {
        "id": "tokyo_d1_m",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 1,
        "title": "Senso-ji Temple & Nakamise-dori in Asakusa",
        "content": "Visit Tokyo's oldest Buddhist temple founded in 645 AD. Stroll the Nakamise shopping street for fresh melonpan and ningyo-yaki sweets. Free admission to grounds.",
        "cost_usd": 5,
        "tags": ["culture", "history", "temple", "free", "day 1"]
    },
    {
        "id": "tokyo_d1_a",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 1,
        "title": "Ueno Park & Tokyo National Museum",
        "content": "Expansive public park with ponds and premier national museum showcasing samurai armor, kimonos, and ancient artifacts. Entry ~$7 (1000 JPY).",
        "cost_usd": 7,
        "tags": ["museum", "nature", "history", "day 1"]
    },
    {
        "id": "tokyo_d1_e",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 1,
        "title": "Akihabara Electric Town & Retro Gaming",
        "content": "Explore neon-drenched streets packed with multi-floor anime shops, Super Potato retro arcade, and electronics gadgets. Free entry, spend ~$10 on gachapon and arcade games.",
        "cost_usd": 10,
        "tags": ["nightlife", "anime", "neon", "day 1"]
    },
    {
        "id": "tokyo_d2_m",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 2,
        "title": "Meiji Jingu Shrine & Yoyogi Park",
        "content": "Serene Shinto shrine enveloped in an evergreen forest of 120,000 trees. Walk through towering cedar torii gates. Completely free entry.",
        "cost_usd": 0,
        "tags": ["spiritual", "nature", "shrine", "free", "day 2"]
    },
    {
        "id": "tokyo_d2_a",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 2,
        "title": "Harajuku Takeshita Street & Shibuya Scramble Crossing",
        "content": "Experience Harajuku youth fashion and quirky crepes ($6), then walk through Cat Street to Shibuya to watch the world-famous Shibuya Scramble Crossing and visit Hachiko statue.",
        "cost_usd": 12,
        "tags": ["culture", "shopping", "landmark", "day 2"]
    },
    {
        "id": "tokyo_d2_e",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 2,
        "title": "Shibuya Sky Observation Deck",
        "content": "360-degree open-air rooftop observation deck overlooking Tokyo skyline, Tokyo Tower, and Mount Fuji at golden hour. Online reservation ~$15.",
        "cost_usd": 15,
        "tags": ["viewpoint", "skyline", "sunset", "day 2"]
    },
    {
        "id": "tokyo_d3_m",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 3,
        "title": "Tsukiji Outer Market Food Crawl",
        "content": "Lively morning market with stalls selling fresh sushi bowls, wagyu skewers, tamagoyaki (sweet egg omelet), and matcha soft serve.",
        "cost_usd": 22,
        "tags": ["food", "market", "breakfast", "day 3"]
    },
    {
        "id": "tokyo_d3_a",
        "destination": "Tokyo",
        "category": "Attraction",
        "day": 3,
        "title": "teamLab Planets Immersive Digital Art",
        "content": "Walk barefoot through water, mirror rooms, and floating flower gardens in this sensory museum. Advance ticket ~$26.",
        "cost_usd": 26,
        "tags": ["art", "modern", "interactive", "day 3"]
    },
    {
        "id": "tokyo_d3_e",
        "destination": "Tokyo",
        "category": "Dining",
        "day": 3,
        "title": "Shinjuku Omoide Yokocho (Memory Lane) Dinner",
        "content": "Atmospheric alleyway lined with tiny yakitori stalls and lantern glow. Enjoy charcoal grilled chicken skewers and cold draft beer for ~$20.",
        "cost_usd": 20,
        "tags": ["dinner", "nightlife", "food", "day 3"]
    },
    {
        "id": "tokyo_hotel_budget",
        "destination": "Tokyo",
        "category": "Hotel",
        "day": None,
        "title": "Tokyo Budget Accommodation: Capsule & Boutique Hostel",
        "content": "Capsule hotels in Shinjuku or design hostels in Kuramae/Asakusa like Nui. Hostel or Mustard Hotel. Average nightly rate: $45.",
        "cost_usd": 45,
        "tags": ["hotel", "budget", "hostel"]
    },

    # ==================== PARIS, FRANCE ====================
    {
        "id": "paris_overview",
        "destination": "Paris",
        "category": "Destination",
        "day": None,
        "title": "Paris 3-Day Budget Explorer Guide",
        "content": "Explore Paris efficiently on a budget with a Navigo Easy pass for metro trips ($2.30/ticket), boulangerie lunches (baguette sandwich + pastry for $7), and free admission to public gardens and banks of the Seine. Budget stays: $70-$95/night in 11th or 18th arrondissement.",
        "cost_usd": 0,
        "tags": ["overview", "budget", "france", "europe"]
    },
    {
        "id": "paris_d1_m",
        "destination": "Paris",
        "category": "Attraction",
        "day": 1,
        "title": "Île de la Cité & Notre-Dame Cathedral",
        "content": "Walk the historic heart of Paris on the Seine. Admire the restored gothic facade of Notre-Dame and stroll the flower market. Free exterior walk.",
        "cost_usd": 0,
        "tags": ["history", "gothic", "architecture", "day 1"]
    },
    {
        "id": "paris_d1_a",
        "destination": "Paris",
        "category": "Attraction",
        "day": 1,
        "title": "Louvre Museum & Tuileries Garden",
        "content": "Masterpieces of world art including Mona Lisa and Venus de Milo. Book timed ticket ($20). Afterwards relax by Tuileries fountains with coffee.",
        "cost_usd": 20,
        "tags": ["museum", "art", "culture", "day 1"]
    },
    {
        "id": "paris_d1_e",
        "destination": "Paris",
        "category": "Dining",
        "day": 1,
        "title": "Latin Quarter Traditional Bistro Dinner",
        "content": "Charming cobblestone Latin Quarter streets. Order a 3-course fixed prix-fixe menu (onion soup, boeuf bourguignon, crème brûlée) for $22.",
        "cost_usd": 22,
        "tags": ["dining", "french", "bistro", "day 1"]
    },
    {
        "id": "paris_d2_m",
        "destination": "Paris",
        "category": "Attraction",
        "day": 2,
        "title": "Montmartre Hill & Sacré-Cœur Basilica",
        "content": "Climb through the artistic bohemian village of Montmartre, visit the marble-domed Sacré-Cœur with sweeping views over all Paris. Free basilica entry.",
        "cost_usd": 4,
        "tags": ["viewpoint", "church", "romantic", "day 2"]
    },
    {
        "id": "paris_d2_a",
        "destination": "Paris",
        "category": "Attraction",
        "day": 2,
        "title": "Musée d'Orsay Impressionist Masters",
        "content": "Housed in a grand Beaux-Arts railway station, featuring world's finest Monet, Van Gogh, Renoir, and Degas collections. Ticket: $17.",
        "cost_usd": 17,
        "tags": ["art", "museum", "impressionism", "day 2"]
    },
    {
        "id": "paris_d2_e",
        "destination": "Paris",
        "category": "Attraction",
        "day": 2,
        "title": "Eiffel Tower Sunset & Champ de Mars Picnic",
        "content": "Grab French wine, fresh baguette, camembert cheese and grapes ($12) for a classic sunset lawn picnic as Eiffel Tower sparkles every hour. Summit ticket optional $20.",
        "cost_usd": 20,
        "tags": ["landmark", "picnic", "eiffel", "day 2"]
    },
    {
        "id": "paris_d3_m",
        "destination": "Paris",
        "category": "Attraction",
        "day": 3,
        "title": "Sainte-Chapelle Stained Glass Marvel",
        "content": "Stunning 13th-century royal chapel with 1,113 stained glass windows depicting biblical scenes. Advance entry ~$13.",
        "cost_usd": 13,
        "tags": ["gothic", "stained-glass", "culture", "day 3"]
    },
    {
        "id": "paris_d3_a",
        "destination": "Paris",
        "category": "Attraction",
        "day": 3,
        "title": "Le Marais Historic District & Place des Vosges",
        "content": "Trendy historic neighborhood with 17th-century mansions, courtyard cafes, indie boutiques, and renowned L'As du Fallafel sandwich lunch ($10).",
        "cost_usd": 10,
        "tags": ["shopping", "architecture", "food", "day 3"]
    },
    {
        "id": "paris_d3_e",
        "destination": "Paris",
        "category": "Attraction",
        "day": 3,
        "title": "Seine River Evening Cruise",
        "content": "1-hour twilight cruise along the Seine under Pont Alexandre III and past illuminated riverside monuments. Ticket ~$16.",
        "cost_usd": 16,
        "tags": ["cruise", "scenic", "river", "romantic", "day 3"]
    },

    # ==================== ROME, ITALY ====================
    {
        "id": "rome_overview",
        "destination": "Rome",
        "category": "Destination",
        "day": None,
        "title": "Rome 3-Day Budget & Ancient Wonders",
        "content": "Rome is an open-air museum where most magnificent sights (Pantheon exterior, Trevi Fountain, Piazza Navona, Spanish Steps) are free. Eat pizza al taglio and pasta cacio e pepe for $8-$14. 72-hour transit pass ~$20. Guesthouse/Hostel ~$60/night.",
        "cost_usd": 0,
        "tags": ["overview", "budget", "italy", "history"]
    },
    {
        "id": "rome_d1_m",
        "destination": "Rome",
        "category": "Attraction",
        "day": 1,
        "title": "Colosseum & Roman Forum",
        "content": "Step onto the arena where gladiators fought and wander the political epicenter of ancient Rome. Combined ticket ~$20.",
        "cost_usd": 20,
        "tags": ["ancient", "history", "landmark", "day 1"]
    },
    {
        "id": "rome_d1_a",
        "destination": "Rome",
        "category": "Attraction",
        "day": 1,
        "title": "Palatine Hill & Circus Maximus",
        "content": "Pine-shaded ruins of imperial palaces with panoramic views over the Roman Forum and ancient chariot racing arena.",
        "cost_usd": 0,
        "tags": ["views", "ruins", "day 1"]
    },
    {
        "id": "rome_d1_e",
        "destination": "Rome",
        "category": "Dining",
        "day": 1,
        "title": "Monti Neighborhood Trattoria Dinner",
        "content": "Hip cobblestone quarter near the Colosseum. Enjoy homemade pasta carbonara and house red wine for $18.",
        "cost_usd": 18,
        "tags": ["pasta", "dinner", "local", "day 1"]
    },
    {
        "id": "rome_d2_m",
        "destination": "Rome",
        "category": "Attraction",
        "day": 2,
        "title": "Vatican City & St. Peter's Basilica",
        "content": "World's largest church with Michelangelo's Pietà and dome. Basilica admission is free. Vatican Museums & Sistine Chapel entry ~$22.",
        "cost_usd": 22,
        "tags": ["vatican", "art", "church", "day 2"]
    },
    {
        "id": "rome_d2_a",
        "destination": "Rome",
        "category": "Attraction",
        "day": 2,
        "title": "Castel Sant'Angelo & Ponte Sant'Angelo",
        "content": "Hadrian's fortress tomb on Tiber River with angel statues and riverside terrace views towards the Vatican. Exterior free, ticket $14.",
        "cost_usd": 14,
        "tags": ["castle", "scenic", "day 2"]
    },
    {
        "id": "rome_d2_e",
        "destination": "Rome",
        "category": "Attraction",
        "day": 2,
        "title": "Trastevere Evening Stroll & Gelato",
        "content": "Lively bohemian neighborhood with ivy-draped alleyways, street buskers, artisan pizza, and artisanal pistachio gelato ($4).",
        "cost_usd": 15,
        "tags": ["nightlife", "gelato", "bohemian", "day 2"]
    },
    {
        "id": "rome_d3_m",
        "destination": "Rome",
        "category": "Attraction",
        "day": 3,
        "title": "Pantheon & Piazza Navona",
        "content": "Best preserved ancient Roman monument with world's largest unreinforced concrete dome and oculus ($5 entry). Walk to Bernini's Fountain of Four Rivers.",
        "cost_usd": 5,
        "tags": ["architecture", "pantheon", "piazza", "day 3"]
    },
    {
        "id": "rome_d3_a",
        "destination": "Rome",
        "category": "Attraction",
        "day": 3,
        "title": "Trevi Fountain Coin Toss & Spanish Steps",
        "content": "Toss a coin into the baroque Trevi Fountain to guarantee your return to Rome. Continue to Spanish Steps for city panoramas. Completely free.",
        "cost_usd": 0,
        "tags": ["baroque", "landmark", "free", "day 3"]
    },
    {
        "id": "rome_d3_e",
        "destination": "Rome",
        "category": "Dining",
        "day": 3,
        "title": "Campo de' Fiori Farewell Aperitivo & Roman Pizza",
        "content": "Square filled with life. Savor Aperol spritz with bruschetta aperitivo board and crisp thin-crust Roman pizza for $20.",
        "cost_usd": 20,
        "tags": ["farewell", "dinner", "pizza", "day 3"]
    },

    # ==================== NEW YORK CITY, USA ====================
    {
        "id": "nyc_overview",
        "destination": "New York",
        "category": "Destination",
        "day": None,
        "title": "New York City 3-Day Budget Explorer",
        "content": "NYC can be tackled affordably with 7-day Unlimited MetroCard ($34), famous $1.50 pizza slices, Chinatown dumplings, and world-class free attractions like Central Park, High Line, and Staten Island Ferry. Budget hotels/pods in Long Island City or Midtown: $110-$160/night.",
        "cost_usd": 0,
        "tags": ["overview", "budget", "usa", "nyc"]
    },
    {
        "id": "nyc_d1_m",
        "destination": "New York",
        "category": "Attraction",
        "day": 1,
        "title": "Central Park & Museum Mile",
        "content": "Walk Bethesda Terrace, Bow Bridge, and the Strawberry Fields memorial. Visit Met Museum or Guggenheim. Strolling park is free.",
        "cost_usd": 15,
        "tags": ["nature", "park", "museum", "day 1"]
    },
    {
        "id": "nyc_d1_a",
        "destination": "New York",
        "category": "Attraction",
        "day": 1,
        "title": "Times Square & Midtown Architecture Walk",
        "content": "See Grand Central Terminal ceiling, New York Public Library, Bryant Park, and the bustling energy of Times Square billboards.",
        "cost_usd": 5,
        "tags": ["midtown", "landmark", "free", "day 1"]
    },
    {
        "id": "nyc_d1_e",
        "destination": "New York",
        "category": "Dining",
        "day": 1,
        "title": "Hell's Kitchen International Food Crawl",
        "content": "Diverse culinary street along 9th Avenue. Savor Thai noodles, Mexican tacos, or classic NYC burger for ~$18.",
        "cost_usd": 18,
        "tags": ["dining", "food", "dinner", "day 1"]
    },
    {
        "id": "nyc_d2_m",
        "destination": "New York",
        "category": "Attraction",
        "day": 2,
        "title": "High Line Elevated Park & Chelsea Market",
        "content": "Stroll 1.45-mile historic freight rail line transformed into a lush public park above Manhattan streets. Free entry, sample snacks at Chelsea Market.",
        "cost_usd": 12,
        "tags": ["park", "modern", "market", "day 2"]
    },
    {
        "id": "nyc_d2_a",
        "destination": "New York",
        "category": "Attraction",
        "day": 2,
        "title": "Greenwich Village & Washington Square Park",
        "content": "Brownstone tree-lined streets, jazz clubs, chess players, and the Washington Square Arch. Grab Joe's Pizza slice ($4).",
        "cost_usd": 8,
        "tags": ["culture", "bohemian", "walk", "day 2"]
    },
    {
        "id": "nyc_d2_e",
        "destination": "New York",
        "category": "Attraction",
        "day": 2,
        "title": "Top of the Rock or Summit One Vanderbilt",
        "content": "Spectacular sunset skyline views looking directly at Empire State Building and Central Park. Ticket ~$38.",
        "cost_usd": 38,
        "tags": ["viewpoint", "skyline", "sunset", "day 2"]
    },
    {
        "id": "nyc_d3_m",
        "destination": "New York",
        "category": "Attraction",
        "day": 3,
        "title": "Staten Island Ferry & Statue of Liberty View",
        "content": "Take the free 25-minute commuter ferry through New York Harbor for dramatic, unobstructed views of Lady Liberty and Financial District skyline. $0 cost.",
        "cost_usd": 0,
        "tags": ["ferry", "liberty", "free", "scenic", "day 3"]
    },
    {
        "id": "nyc_d3_a",
        "destination": "New York",
        "category": "Attraction",
        "day": 3,
        "title": "Brooklyn Bridge Walk & DUMBO",
        "content": "Walk across the iconic suspension bridge to Brooklyn. Capture the classic Manhattan Bridge photo in DUMBO and relax at Brooklyn Bridge Park waterfront.",
        "cost_usd": 0,
        "tags": ["brooklyn", "bridge", "views", "photo", "day 3"]
    },
    {
        "id": "nyc_d3_e",
        "destination": "New York",
        "category": "Dining",
        "day": 3,
        "title": "Chinatown & Little Italy Feast",
        "content": "Feast on steaming soup dumplings (xiao long bao) in Chinatown followed by cannoli at Ferrara Bakery. Total feast ~$18.",
        "cost_usd": 18,
        "tags": ["dumplings", "chinatown", "dinner", "day 3"]
    },

    # ==================== BALI, INDONESIA ====================
    {
        "id": "bali_overview",
        "destination": "Bali",
        "category": "Destination",
        "day": None,
        "title": "Bali Budget Paradise 3-Day Guide",
        "content": "Bali is an affordable tropical haven. Scooter rental costs $6/day, traditional Warung meals (nasi campur, mie goreng) cost $2-$4, and boutique tropical villas with pools cost $30-$55/night.",
        "cost_usd": 0,
        "tags": ["overview", "budget", "asia", "tropical"]
    },
    {
        "id": "bali_d1_m",
        "destination": "Bali",
        "category": "Attraction",
        "day": 1,
        "title": "Ubud Sacred Monkey Forest Sanctuary",
        "content": "Enchanting moss-covered jungle sanctuary home to over 1,000 Balinese long-tailed macaques and ancient stone shrines. Ticket: ~$6 (80k IDR).",
        "cost_usd": 6,
        "tags": ["nature", "wildlife", "jungle", "day 1"]
    },
    {
        "id": "bali_d1_a",
        "destination": "Bali",
        "category": "Attraction",
        "day": 1,
        "title": "Tegalalang Rice Terraces & Jungle Swing",
        "content": "Emerald green stepped valleys carved with UNESCO subak irrigation system. Walk paths and enjoy coconut water. Entry: $4.",
        "cost_usd": 4,
        "tags": ["scenic", "nature", "photo", "day 1"]
    },
    {
        "id": "bali_d1_e",
        "destination": "Bali",
        "category": "Dining",
        "day": 1,
        "title": "Ubud Art Market & Organic Warung Dinner",
        "content": "Shop woven rattan bags and sarongs, then dine on crispy duck (bebek betutu) or vegan gado-gado in a bamboo pavilion for $7.",
        "cost_usd": 7,
        "tags": ["dinner", "market", "organic", "day 1"]
    },
    {
        "id": "bali_d2_m",
        "destination": "Bali",
        "category": "Attraction",
        "day": 2,
        "title": "Tirta Empul Holy Water Spring Temple",
        "content": "Sacred water temple where Balinese Hindus and travelers take part in spiritual cleansing melukat ritual. Entry + sarong rental: $5.",
        "cost_usd": 5,
        "tags": ["spiritual", "temple", "water", "day 2"]
    },
    {
        "id": "bali_d2_a",
        "destination": "Bali",
        "category": "Attraction",
        "day": 2,
        "title": "Tegenungan Waterfall Canyon Swim",
        "content": "Dramatic cascading waterfall nestled in a jungle valley. Swim in natural pool and relax at bamboo daybed cafe. Entry: $3.",
        "cost_usd": 3,
        "tags": ["waterfall", "swim", "adventure", "day 2"]
    },
    {
        "id": "bali_d2_e",
        "destination": "Bali",
        "category": "Dining",
        "day": 2,
        "title": "Jimbaran Bay Beachfront Seafood BBQ",
        "content": "Candlelit wooden tables on the sand as the sun sinks into the Indian Ocean. Fresh grilled snapper with sambal matah and rice: $14.",
        "cost_usd": 14,
        "tags": ["seafood", "beach", "sunset", "dinner", "day 2"]
    },
    {
        "id": "bali_d3_m",
        "destination": "Bali",
        "category": "Attraction",
        "day": 3,
        "title": "Canggu Beach & Surf Lesson",
        "content": "Catch beginner-friendly waves with a local surf instructor on Batu Bolong beach. 2-hour board + coaching: $15.",
        "cost_usd": 15,
        "tags": ["beach", "surf", "sports", "day 3"]
    },
    {
        "id": "bali_d3_a",
        "destination": "Bali",
        "category": "Attraction",
        "day": 3,
        "title": "Tanah Lot Sea Temple",
        "content": "Ancient offshore pilgrimage shrine perched on a craggy rock battered by ocean waves. Magnificent coastal backdrop. Entry: $4.",
        "cost_usd": 4,
        "tags": ["temple", "coastal", "iconic", "day 3"]
    },
    {
        "id": "bali_d3_e",
        "destination": "Bali",
        "category": "Attraction",
        "day": 3,
        "title": "Uluwatu Clifftop Temple & Kecak Fire Dance",
        "content": "Perched 70 meters above roaring surf on sheer limestone cliff. Watch the hypnotic Kecak dance chant at dusk against blazing orange sunset. Ticket: $10.",
        "cost_usd": 10,
        "tags": ["dance", "culture", "sunset", "clifftop", "day 3"]
    },

    # ==================== LONDON, UK ====================
    {
        "id": "london_overview",
        "destination": "London",
        "category": "Destination",
        "day": None,
        "title": "London 3-Day Budget Explorer",
        "content": "London offers extraordinary value because world-class national museums (British Museum, Tate Modern, Natural History) have completely free general admission! Tap contactless card on Tube/buses with daily caps ($11/day). Budget hotels: $85-$125/night.",
        "cost_usd": 0,
        "tags": ["overview", "budget", "uk", "transit"]
    },
    {
        "id": "london_d1_m",
        "destination": "London",
        "category": "Attraction",
        "day": 1,
        "title": "British Museum & Great Court",
        "content": "Explore Rosetta Stone, Parthenon Sculptures, and Egyptian mummies beneath Norman Foster's glass domed ceiling. Free admission.",
        "cost_usd": 0,
        "tags": ["museum", "history", "free", "day 1"]
    },
    {
        "id": "london_d1_a",
        "destination": "London",
        "category": "Attraction",
        "day": 1,
        "title": "Covent Garden & Westminster Abbey Walk",
        "content": "Street performers at Covent Garden piazza, walk down Whitehall past Downing Street to Big Ben and Parliament Square.",
        "cost_usd": 5,
        "tags": ["architecture", "walk", "landmark", "day 1"]
    },
    {
        "id": "london_d1_e",
        "destination": "London",
        "category": "Dining",
        "day": 1,
        "title": "Historic Riverside Pub Dinner & Ale",
        "content": "16th-century timber pub along the Thames. Savor crisp golden fish & chips with mushy peas and craft bitter for $18.",
        "cost_usd": 18,
        "tags": ["pub", "fishandchips", "dinner", "day 1"]
    },
    {
        "id": "london_d2_m",
        "destination": "London",
        "category": "Attraction",
        "day": 2,
        "title": "Tower Bridge & Tower of London",
        "content": "Walk across Victorian gothic Tower Bridge (free) and view the historic castle fortress and Crown Jewels. Ticket ~$36 or exterior stroll.",
        "cost_usd": 15,
        "tags": ["bridge", "history", "castle", "day 2"]
    },
    {
        "id": "london_d2_a",
        "destination": "London",
        "category": "Attraction",
        "day": 2,
        "title": "Borough Market Food Feast & Tate Modern",
        "content": "London's oldest food market: sausage rolls, paella, raclette cheese ($10), followed by modern art at Tate Modern boiler house (free).",
        "cost_usd": 12,
        "tags": ["market", "art", "modern", "day 2"]
    },
    {
        "id": "london_d2_e",
        "destination": "London",
        "category": "Attraction",
        "day": 2,
        "title": "South Bank Cultural Walk & London Eye View",
        "content": "Evening stroll along South Bank lights, skate parks, bookstalls, and illuminated London Eye across the river.",
        "cost_usd": 0,
        "tags": ["scenic", "river", "walk", "night", "day 2"]
    },
    {
        "id": "london_d3_m",
        "destination": "London",
        "category": "Attraction",
        "day": 3,
        "title": "Buckingham Palace & St. James's Park",
        "content": "Watch the Changing of the Guard ceremony (free, 11:00 AM) and walk the royal park with pelicans and flower beds.",
        "cost_usd": 0,
        "tags": ["royal", "ceremony", "free", "day 3"]
    },
    {
        "id": "london_d3_a",
        "destination": "London",
        "category": "Attraction",
        "day": 3,
        "title": "Camden Market & Regent's Canal Walk",
        "content": "Eclectic music stalls, vintage leather jackets, cyberpunk fashion, and global street food stalls along the locks.",
        "cost_usd": 12,
        "tags": ["market", "canal", "vintage", "day 3"]
    },
    {
        "id": "london_d3_e",
        "destination": "London",
        "category": "Dining",
        "day": 3,
        "title": "Soho & Chinatown Farewell Dinner",
        "content": "Bustling nightlife epicenter with dim sum or cozy Italian pasta on Dean Street for ~$20.",
        "cost_usd": 20,
        "tags": ["soho", "dinner", "farewell", "day 3"]
    }
]

def generate_dynamic_city_data(destination: str) -> List[Dict[str, Any]]:
    """
    Generates realistic, structured 3-day travel intelligence items for any destination
    worldwide to index in FAISS when a user searches for an unseeded city.
    """
    dest = destination.title()
    return [
        {
            "id": f"{dest.lower()}_overview",
            "destination": dest,
            "category": "Destination",
            "day": None,
            "title": f"{dest} 3-Day Travel Overview",
            "content": f"Discover {dest} over three days within budget. Enjoy local transit passes, regional cuisine, historic center walks, and iconic cultural viewpoints.",
            "cost_usd": 0,
            "tags": ["overview", "budget", dest.lower()]
        },
        {
            "id": f"{dest.lower()}_d1_m",
            "destination": dest,
            "category": "Attraction",
            "day": 1,
            "title": f"Historic Old Town & Central Square in {dest}",
            "content": f"Begin your 3-day exploration at the heart of {dest}. Wander cobblestone lanes, iconic municipal buildings, and landmark plazas.",
            "cost_usd": 5,
            "tags": ["history", "culture", "day 1"]
        },
        {
            "id": f"{dest.lower()}_d1_a",
            "destination": dest,
            "category": "Attraction",
            "day": 1,
            "title": f"Premier Art & History Museum of {dest}",
            "content": f"Explore regional artifacts, masterworks, and cultural heritage exhibits preserving the stories of {dest}.",
            "cost_usd": 12,
            "tags": ["museum", "art", "day 1"]
        },
        {
            "id": f"{dest.lower()}_d1_e",
            "destination": dest,
            "category": "Dining",
            "day": 1,
            "title": f"Authentic Local Dinner in {dest}",
            "content": f"Experience traditional culinary specialties and local beverage pairings in a neighborhood tavern.",
            "cost_usd": 18,
            "tags": ["dinner", "local food", "day 1"]
        },
        {
            "id": f"{dest.lower()}_d2_m",
            "destination": dest,
            "category": "Attraction",
            "day": 2,
            "title": f"Scenic Botanical Gardens or Waterfront Promenade",
            "content": f"Fresh morning stroll through lush green landscapes, waterfront docks, and tranquil scenic overlooks.",
            "cost_usd": 4,
            "tags": ["nature", "scenic", "day 2"]
        },
        {
            "id": f"{dest.lower()}_d2_a",
            "destination": dest,
            "category": "Attraction",
            "day": 2,
            "title": f"Architectural Landmark & Panoramic Viewpoint",
            "content": f"Ascend to the highest observation tower, fortress, or hill in {dest} for panoramic 360-degree photography.",
            "cost_usd": 14,
            "tags": ["viewpoint", "photos", "day 2"]
        },
        {
            "id": f"{dest.lower()}_d2_e",
            "destination": dest,
            "category": "Dining",
            "day": 2,
            "title": f"Street Food Market & Nightlife Quarter",
            "content": f"Vibrant evening district lined with lively eateries, artisan food trucks, and acoustic live music.",
            "cost_usd": 16,
            "tags": ["street food", "nightlife", "day 2"]
        },
        {
            "id": f"{dest.lower()}_d3_m",
            "destination": dest,
            "category": "Attraction",
            "day": 3,
            "title": f"Artisan Craft Market & Souvenir Treasures",
            "content": f"Handmade local crafts, ceramics, regional spices, and textiles directly from independent artisans in {dest}.",
            "cost_usd": 10,
            "tags": ["shopping", "souvenirs", "crafts", "day 3"]
        },
        {
            "id": f"{dest.lower()}_d3_a",
            "destination": dest,
            "category": "Attraction",
            "day": 3,
            "title": f"Cultural Heritage Quarter & Hidden Courtyards",
            "content": f"Uncover peaceful backstreets, historic gates, and quiet spiritual retreats off the beaten tourist path.",
            "cost_usd": 6,
            "tags": ["culture", "hidden gem", "day 3"]
        },
        {
            "id": f"{dest.lower()}_d3_e",
            "destination": dest,
            "category": "Dining",
            "day": 3,
            "title": f"Celebratory Farewell Dinner in {dest}",
            "content": f"Conclude your memorable 3-day journey with a scenic dinner overlooking illuminated monuments.",
            "cost_usd": 22,
            "tags": ["farewell", "dinner", "atmosphere", "day 3"]
        }
    ]
