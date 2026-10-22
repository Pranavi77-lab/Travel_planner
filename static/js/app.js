// Frontend Application Logic for Travel Planning Assistant
let currentItinerary = null;
let leafletMap = null;
let mapMarkers = [];
let routeLine = null;
let budgetChart = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    loadPresets();
    loadSystemStats();
    setupEventListeners();
    // Auto-load initial itinerary for Tokyo to wow user immediately
    runPlanning("Tokyo", 950, "USD", "balanced", 1, ["Culture", "Food", "Sightseeing"]);
});

function setupEventListeners() {
    const planForm = document.getElementById('trip-form');
    if (planForm) {
        planForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const destination = document.getElementById('input-destination').value.trim();
            const budget = parseFloat(document.getElementById('input-budget').value) || 1000;
            const currency = document.getElementById('input-currency').value;
            const travelStyle = document.querySelector('input[name="travel_style"]:checked')?.value || "balanced";
            const travelers = parseInt(document.getElementById('input-travelers').value) || 1;
            
            const selectedInterests = Array.from(document.querySelectorAll('.interest-checkbox:checked'))
                .map(cb => cb.value);

            if (!destination) {
                alert("Please enter a destination city.");
                return;
            }

            runPlanning(destination, budget, currency, travelStyle, travelers, selectedInterests);
        });
    }

    // Tab Navigation
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.nav-tab-btn').forEach(b => {
                b.classList.remove('active', 'border-indigo-600', 'text-indigo-600');
                b.classList.add('border-transparent', 'text-slate-500');
            });
            btn.classList.add('active', 'border-indigo-600', 'text-indigo-600');
            btn.classList.remove('border-transparent', 'text-slate-500');

            const tabId = btn.getAttribute('data-tab');
            document.querySelectorAll('.tab-content-panel').forEach(panel => {
                panel.classList.add('hidden');
            });
            const targetPanel = document.getElementById(`tab-${tabId}`);
            if (targetPanel) {
                targetPanel.classList.remove('hidden');
            }

            if (tabId === 'map' && leafletMap) {
                setTimeout(() => {
                    leafletMap.invalidateSize();
                }, 200);
            }
        });
    });

    // Budget sliders live update
    ['slider-acc', 'slider-dining', 'slider-attractions', 'slider-transport', 'slider-contingency'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', recalculateCustomBudget);
        }
    });

    // Vector search sandbox
    const vsBtn = document.getElementById('btn-vector-query');
    if (vsBtn) {
        vsBtn.addEventListener('click', runVectorSandboxQuery);
    }
}

async function loadPresets() {
    try {
        const res = await fetch('/api/destinations');
        const data = await res.json();
        const container = document.getElementById('preset-chips');
        if (!container || !data.destinations) return;

        container.innerHTML = data.destinations.map(p => `
            <button type="button" onclick="selectPreset('${p.city}', ${p.budget}, '${p.currency}')"
                class="px-3 py-1.5 bg-white border border-slate-200 hover:border-indigo-500 rounded-full text-xs font-semibold text-slate-700 shadow-sm transition-all hover:bg-indigo-50 flex items-center space-x-1.5">
                <span>📍 ${p.city}</span>
                <span class="text-indigo-600 font-bold">(${p.currency === 'EUR' ? '€' : (p.currency === 'GBP' ? '£' : '$')}${p.budget})</span>
            </button>
        `).join('');
    } catch (err) {
        console.error("Failed to load presets:", err);
    }
}

function selectPreset(city, budget, currency) {
    document.getElementById('input-destination').value = city;
    document.getElementById('input-budget').value = budget;
    document.getElementById('input-currency').value = currency;
    runPlanning(city, budget, currency, "balanced", 1, ["Culture", "Food", "Sightseeing"]);
}

async function loadSystemStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        const statEl = document.getElementById('system-stats-badge');
        if (statEl) {
            statEl.innerHTML = `
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-ping"></span>
                    FAISS: ${data.total_documents} Docs Indexed
                </span>
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                    ⚡ ${data.model} (${data.vector_dimensions}-dim)
                </span>
            `;
        }
    } catch (err) {
        console.warn("Stats load error:", err);
    }
}

async function runPlanning(destination, budget, currency, travelStyle, travelers, interests) {
    const loadingOverlay = document.getElementById('loading-state');
    const resultsContainer = document.getElementById('results-section');
    const loadingStatusText = document.getElementById('loading-status-text');

    if (loadingOverlay) loadingOverlay.classList.remove('hidden');
    if (resultsContainer) resultsContainer.classList.add('opacity-50');

    // Simulate animated pipeline updates
    const steps = [
        "📍 Geocoding Coordinates with Places API...",
        "🌦️ Fetching Live 3-Day Forecast from Open-Meteo...",
        "🧠 Vector Embedding with nomic-embed-text (768-dim)...",
        "⚡ Executing FAISS Cosine Similarity Search...",
        "💰 Calculating Itemized Expenses & Budget Buffer..."
    ];

    let stepIdx = 0;
    const interval = setInterval(() => {
        if (loadingStatusText && stepIdx < steps.length) {
            loadingStatusText.textContent = steps[stepIdx];
            stepIdx++;
        }
    }, 450);

    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                destination,
                budget,
                currency,
                travel_style: travelStyle,
                travelers,
                interests
            })
        });

        const resData = await response.json();
        clearInterval(interval);

        if (!resData.success) {
            alert("Planning Error: " + (resData.error || "Unknown"));
            return;
        }

        currentItinerary = resData.data;
        renderItineraryDashboard(currentItinerary);

    } catch (err) {
        clearInterval(interval);
        console.error("API error:", err);
        alert("Failed to communicate with planning engine. Please check backend connection.");
    } finally {
        if (loadingOverlay) loadingOverlay.classList.add('hidden');
        if (resultsContainer) {
            resultsContainer.classList.remove('opacity-50');
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

function renderItineraryDashboard(data) {
    // 1. Header Overview
    document.getElementById('overview-destination-title').textContent = `${data.destination} 3-Day Smart Itinerary`;
    document.getElementById('overview-vibe-badge').textContent = `${data.travel_style.toUpperCase()} TRAVEL`;
    document.getElementById('overview-travelers-badge').textContent = `${data.travelers} Traveler(s)`;

    const budget = data.budget;
    const budgetBadge = document.getElementById('overview-budget-badge');
    budgetBadge.className = `px-3 py-1 rounded-full text-xs font-bold inline-flex items-center space-x-1 ${
        budget.is_within_budget ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
    }`;
    budgetBadge.innerHTML = `
        <span>${budget.is_within_budget ? '✓' : '⚠️'}</span>
        <span>${budget.status}: ${budget.currency_symbol}${Math.abs(budget.variance)} ${budget.is_within_budget ? 'Surplus' : 'Deficit'}</span>
    `;

    document.getElementById('stat-total-budget').textContent = `${budget.currency_symbol}${budget.total_budget.toLocaleString()}`;
    document.getElementById('stat-estimated-spend').textContent = `${budget.currency_symbol}${budget.grand_total.toLocaleString()}`;
    document.getElementById('stat-daily-burn').textContent = `${budget.currency_symbol}${budget.daily_burn_rate.toLocaleString()}/day`;
    document.getElementById('stat-per-person').textContent = `${budget.currency_symbol}${budget.per_person_total.toLocaleString()}`;

    // 2. Render Day Cards
    renderDayCards(data.days, budget.currency_symbol);

    // 3. Render Weather Cards
    renderWeatherTab(data.weather);

    // 4. Render Leaflet Map
    renderLeafletMap(data.coordinates, data.places);

    // 5. Render Budget Doughnut Chart & Sliders
    renderBudgetCalculator(budget);

    // 6. Render FAISS Vector Inspector
    renderVectorAudit(data.vector_search_audit);
}

function renderDayCards(days, currencySymbol) {
    const container = document.getElementById('days-container');
    if (!container) return;

    container.innerHTML = days.map((day, dIdx) => `
        <div class="glass-card rounded-2xl p-6 border border-slate-200/80 shadow-sm relative overflow-hidden mb-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-100 mb-5">
                <div class="flex items-center space-x-3 mb-2 md:mb-0">
                    <span class="w-9 h-9 rounded-xl day-badge flex items-center justify-center font-bold text-white shadow-md text-sm">
                        D${day.day_number}
                    </span>
                    <div>
                        <h3 class="text-lg font-bold text-slate-800">${day.title}</h3>
                        <p class="text-xs text-slate-500 font-medium">Estimated Day Expenses: ~${currencySymbol}${day.estimated_day_cost_usd} USD equiv.</p>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200/60">
                        <span class="mr-1.5 text-sm">${day.weather?.icon || '☀️'}</span>
                        ${day.weather?.condition || 'Clear'} (${day.weather?.temp_max_c || 22}°C / ${day.weather?.temp_max_f || 72}°F)
                    </span>
                    <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600">
                        💧 Rain: ${day.weather?.rain_probability || 0}%
                    </span>
                </div>
            </div>

            <!-- Activities Timeline -->
            <div class="space-y-4">
                ${day.activities.map((act, aIdx) => `
                    <div class="p-4 rounded-xl bg-slate-50/70 border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/20 transition-all flex flex-col md:flex-row md:items-start justify-between">
                        <div class="space-y-1 md:w-3/4">
                            <div class="flex items-center space-x-2">
                                <span class="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-indigo-100 text-indigo-700">
                                    ${act.time_slot}
                                </span>
                                <span class="text-xs font-semibold text-slate-500">${act.category}</span>
                            </div>
                            <h4 class="text-base font-bold text-slate-800 pt-1">${act.title}</h4>
                            <p class="text-sm text-slate-600 leading-relaxed">${act.description}</p>
                            ${act.note ? `<p class="text-xs text-amber-700 font-medium bg-amber-50 p-2 rounded-lg border border-amber-200 mt-2">${act.note}</p>` : ''}
                            <div class="flex flex-wrap gap-1 pt-1.5">
                                ${act.tags.map(t => `<span class="text-[10px] font-medium bg-white text-slate-500 px-2 py-0.5 rounded-full border border-slate-200">#${t}</span>`).join('')}
                            </div>
                        </div>
                        <div class="mt-3 md:mt-0 text-right shrink-0">
                            <span class="inline-block px-3 py-1 rounded-lg text-xs font-bold ${act.cost_usd === 0 ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-200 text-slate-700'}">
                                ${act.cost_usd === 0 ? 'FREE' : `~$${act.cost_usd}`}
                            </span>
                        </div>
                    </div>
                `).join('')}
            </div>

            <!-- Transit Tip Banner -->
            <div class="mt-4 p-3 rounded-xl bg-slate-100/80 border border-slate-200/60 flex items-center space-x-2 text-xs text-slate-600">
                <span class="text-base">🚇</span>
                <span><strong>Transit Advice:</strong> ${day.transit_tip}</span>
            </div>
        </div>
    `).join('');
}

function renderWeatherTab(weather) {
    const forecastContainer = document.getElementById('weather-cards-container');
    const adviceText = document.getElementById('weather-advice-text');

    if (adviceText) {
        adviceText.textContent = weather.clothing_advice || "Pack versatile layers and comfortable walking shoes.";
    }

    if (!forecastContainer || !weather.forecast) return;

    forecastContainer.innerHTML = weather.forecast.map(f => `
        <div class="glass-card rounded-2xl p-5 border border-slate-200/80 flex flex-col justify-between shadow-sm">
            <div>
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold px-2.5 py-1 rounded-lg bg-indigo-50 text-indigo-700">Day ${f.day_number} (${f.date})</span>
                    <span class="text-2xl">${f.icon}</span>
                </div>
                <h4 class="text-lg font-bold text-slate-800">${f.condition}</h4>
                <div class="flex items-baseline space-x-2 my-2">
                    <span class="text-2xl font-extrabold text-slate-900">${f.temp_max_c}°C</span>
                    <span class="text-sm font-medium text-slate-400">/ ${f.temp_min_c}°C</span>
                    <span class="text-xs text-slate-500 font-semibold ml-2">(${f.temp_max_f}°F)</span>
                </div>
                <div class="space-y-1.5 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <div class="flex justify-between">
                        <span>Precipitation Risk:</span>
                        <span class="font-bold ${f.rain_probability > 30 ? 'text-amber-600' : 'text-slate-700'}">${f.rain_probability}%</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Wind Speed:</span>
                        <span class="font-bold text-slate-700">${f.wind_kmh} km/h</span>
                    </div>
                </div>
            </div>
            <div class="mt-4 p-2.5 rounded-lg bg-slate-50 text-[11px] text-slate-600 border border-slate-100">
                💡 ${f.packing_tip}
            </div>
        </div>
    `).join('');
}

function renderLeafletMap(center, places) {
    if (!places || places.length === 0) return;

    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    if (!leafletMap) {
        leafletMap = L.map('map').setView([center.lat, center.lon], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(leafletMap);
    } else {
        leafletMap.setView([center.lat, center.lon], 12);
    }

    // Clear existing markers
    mapMarkers.forEach(m => leafletMap.removeLayer(m));
    mapMarkers = [];
    if (routeLine) leafletMap.removeLayer(routeLine);

    const colors = { 1: '#3B82F6', 2: '#10B981', 3: '#F59E0B' };
    const latLngs = [];

    places.forEach(p => {
        const markerColor = colors[p.day] || '#6366F1';
        latLngs.push([p.lat, p.lon]);

        const customIcon = L.divIcon({
            className: 'custom-map-pin',
            html: `
                <div style="background-color: ${markerColor}; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
                    D${p.day}
                </div>
            `,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
        });

        const marker = L.marker([p.lat, p.lon], { icon: customIcon }).addTo(leafletMap);
        marker.bindPopup(`
            <div class="p-1">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase text-white" style="background-color: ${markerColor}">Day ${p.day}</span>
                <h4 class="font-bold text-sm text-slate-800 mt-1">${p.name}</h4>
                <p class="text-xs text-slate-500">${p.category}</p>
                <p class="text-xs font-semibold text-emerald-600 mt-1">Cost: ${p.cost}</p>
            </div>
        `);
        mapMarkers.push(marker);
    });

    // Draw route connecting points
    if (latLngs.length > 1) {
        routeLine = L.polyline(latLngs, {
            color: '#6366F1',
            weight: 3,
            dashArray: '6, 8',
            opacity: 0.6
        }).addTo(leafletMap);
        leafletMap.fitBounds(latLngs, { padding: [50, 50] });
    }
}

function renderBudgetCalculator(budget) {
    // Sliders setup
    document.getElementById('slider-acc-val').textContent = `$${document.getElementById('slider-acc').value}/night`;
    document.getElementById('slider-dining-val').textContent = `$${document.getElementById('slider-dining').value}/day`;
    document.getElementById('slider-attractions-val').textContent = `$${document.getElementById('slider-attractions').value}`;
    document.getElementById('slider-transport-val').textContent = `$${document.getElementById('slider-transport').value}`;
    document.getElementById('slider-contingency-val').textContent = `${document.getElementById('slider-contingency').value}%`;

    // Render Breakdown list
    const listEl = document.getElementById('budget-breakdown-list');
    if (listEl && budget.breakdown) {
        listEl.innerHTML = budget.breakdown.map(b => `
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                <div class="flex items-center space-x-2.5">
                    <span class="w-3 h-3 rounded-full" style="background-color: ${b.color}"></span>
                    <span class="text-xs font-bold text-slate-700">${b.category}</span>
                </div>
                <div class="text-right">
                    <span class="text-xs font-extrabold text-slate-900">${budget.currency_symbol}${b.amount.toLocaleString()}</span>
                    <span class="text-[11px] text-slate-400 font-medium ml-1">(${b.percent}%)</span>
                </div>
            </div>
        `).join('');
    }

    // Chart.js Doughnut
    const chartCanvas = document.getElementById('budgetChart');
    if (chartCanvas && budget.breakdown) {
        const labels = budget.breakdown.map(b => b.category);
        const dataVals = budget.breakdown.map(b => b.amount);
        const bgColors = budget.breakdown.map(b => b.color);

        if (budgetChart) {
            budgetChart.destroy();
        }

        budgetChart = new Chart(chartCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataVals,
                    backgroundColor: bgColors,
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { boxWidth: 12, font: { size: 10, family: 'Plus Jakarta Sans' } }
                    }
                },
                cutout: '68%'
            }
        });
    }
}

async function recalculateCustomBudget() {
    if (!currentItinerary) return;

    const budgetVal = currentItinerary.budget.total_budget;
    const currency = currentItinerary.budget.currency;
    const travelers = currentItinerary.travelers;
    const travelStyle = currentItinerary.travel_style;

    const acc = parseFloat(document.getElementById('slider-acc').value);
    const dining = parseFloat(document.getElementById('slider-dining').value);
    const attractions = parseFloat(document.getElementById('slider-attractions').value);
    const transport = parseFloat(document.getElementById('slider-transport').value);
    const contingency = parseFloat(document.getElementById('slider-contingency').value);

    // Update labels
    document.getElementById('slider-acc-val').textContent = `$${acc}/night`;
    document.getElementById('slider-dining-val').textContent = `$${dining}/day`;
    document.getElementById('slider-attractions-val').textContent = `$${attractions}`;
    document.getElementById('slider-transport-val').textContent = `$${transport}`;
    document.getElementById('slider-contingency-val').textContent = `${contingency}%`;

    try {
        const res = await fetch('/api/calculator', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                budget: budgetVal,
                currency: currency,
                travelers: travelers,
                travel_style: travelStyle,
                acc_per_night: acc,
                dining_per_day: dining,
                attractions: attractions,
                transport: transport,
                contingency_percent: contingency
            })
        });

        const newBudget = await res.json();
        currentItinerary.budget = newBudget;

        // Re-render overview budget stats
        document.getElementById('stat-estimated-spend').textContent = `${newBudget.currency_symbol}${newBudget.grand_total.toLocaleString()}`;
        document.getElementById('stat-daily-burn').textContent = `${newBudget.currency_symbol}${newBudget.daily_burn_rate.toLocaleString()}/day`;
        document.getElementById('stat-per-person').textContent = `${newBudget.currency_symbol}${newBudget.per_person_total.toLocaleString()}`;

        const budgetBadge = document.getElementById('overview-budget-badge');
        budgetBadge.className = `px-3 py-1 rounded-full text-xs font-bold inline-flex items-center space-x-1 ${
            newBudget.is_within_budget ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
        }`;
        budgetBadge.innerHTML = `
            <span>${newBudget.is_within_budget ? '✓' : '⚠️'}</span>
            <span>${newBudget.status}: ${newBudget.currency_symbol}${Math.abs(newBudget.variance)} ${newBudget.is_within_budget ? 'Surplus' : 'Deficit'}</span>
        `;

        renderBudgetCalculator(newBudget);
    } catch (err) {
        console.error("Recalculate error:", err);
    }
}

function renderVectorAudit(auditList) {
    const container = document.getElementById('faiss-audit-list');
    if (!container) return;

    if (!auditList || auditList.length === 0) {
        container.innerHTML = `<p class="text-sm text-slate-500">No vector retrieval logs available.</p>`;
        return;
    }

    container.innerHTML = auditList.map((item, idx) => `
        <div class="p-4 rounded-xl bg-white border border-slate-200/90 shadow-sm space-y-1.5 hover:border-indigo-300 transition-all">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                    <span class="w-5 h-5 rounded-full bg-indigo-50 text-indigo-700 text-[10px] font-bold flex items-center justify-center">#${idx+1}</span>
                    <h5 class="text-sm font-bold text-slate-800">${item.title}</h5>
                </div>
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-extrabold bg-indigo-50 text-indigo-700 border border-indigo-200/50">
                    Cosine Sim: ${(item.score * 100).toFixed(1)}%
                </span>
            </div>
            <p class="text-xs text-slate-600">${item.content_snippet}</p>
            <div class="flex flex-wrap gap-1 pt-1">
                <span class="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">${item.category}</span>
                ${item.tags.map(t => `<span class="text-[10px] text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">#${t}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

async function runVectorSandboxQuery() {
    const input = document.getElementById('input-vector-sandbox');
    const resultsBox = document.getElementById('sandbox-query-results');
    const query = input.value.trim();

    if (!query) {
        alert("Please enter a search query for FAISS.");
        return;
    }

    resultsBox.innerHTML = `<p class="text-xs text-indigo-600 font-semibold animate-pulse">Searching FAISS Vector Index with nomic-embed-text...</p>`;

    try {
        const res = await fetch('/api/vector-search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, top_k: 4 })
        });
        const data = await res.json();
        
        if (!data.results || data.results.length === 0) {
            resultsBox.innerHTML = `<p class="text-xs text-slate-500">No matching vector embeddings found.</p>`;
            return;
        }

        resultsBox.innerHTML = `
            <div class="space-y-2 mt-3">
                <p class="text-[11px] text-slate-500 font-semibold">Matched ${data.results.length} items from ${data.total_indexed} indexed chunks using ${data.embedding_model}:</p>
                ${data.results.map(r => `
                    <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                        <div class="flex justify-between font-bold text-slate-800">
                            <span>${r.destination} - ${r.title}</span>
                            <span class="text-indigo-600">Sim: ${(r.score * 100).toFixed(1)}%</span>
                        </div>
                        <p class="text-slate-600 text-[11px] mt-1">${r.content}</p>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (err) {
        resultsBox.innerHTML = `<p class="text-xs text-rose-500">Search error: ${err.message}</p>`;
    }
}

function printItinerary() {
    window.print();
}

function copyItineraryText() {
    if (!currentItinerary) return;
    let text = `✈️ 3-DAY ITINERARY: ${currentItinerary.destination.toUpperCase()}\n`;
    text += `Budget: ${currentItinerary.budget.currency_symbol}${currentItinerary.budget.total_budget} | Status: ${currentItinerary.budget.status}\n\n`;

    currentItinerary.days.forEach(d => {
        text += `== DAY ${d.day_number}: ${d.title} ==\n`;
        text += `Weather: ${d.weather?.condition || 'Clear'} (${d.weather?.temp_max_c || 22}°C)\n`;
        d.activities.forEach(a => {
            text += `* ${a.time_slot} - ${a.title} ($${a.cost_usd}): ${a.description}\n`;
        });
        text += `Transit: ${d.transit_tip}\n\n`;
    });

    navigator.clipboard.writeText(text).then(() => {
        alert("Itinerary copied to clipboard!");
    }).catch(() => {
        alert("Could not copy automatically. You can use Print/PDF export.");
    });
}
