"""
VM 2026 demo-data. Brukes når API-nøkler ikke er konfigurert.
Lag, grupper og ratinger er basert på kjente kvalifiserte lag.
"""

GROUPS = {
    "A": ["USA", "Ecuador", "South Korea", "Serbia"],
    "B": ["Canada", "Colombia", "Morocco", "Denmark"],
    "C": ["Mexico", "Venezuela", "Japan", "Scotland"],
    "D": ["Brazil", "Panama", "Senegal", "Austria"],
    "E": ["Argentina", "Jamaica", "Cameroon", "Turkey"],
    "F": ["France", "Uruguay", "South Africa", "Croatia"],
    "G": ["Germany", "Costa Rica", "Nigeria", "Australia"],
    "H": ["Spain", "Honduras", "Ivory Coast", "Iran"],
    "I": ["Portugal", "El Salvador", "Egypt", "Saudi Arabia"],
    "J": ["England", "New Zealand", "Algeria", "Switzerland"],
    "K": ["Netherlands", "China", "Tunisia", "Hungary"],
    "L": ["Italy", "Ukraine", "Uzbekistan", "Iraq"],
}

# attack = forventet mål scoret per kamp (1.0 = snitt)
# defense = forventet mål sluppet inn per kamp (lavere = bedre, 1.0 = snitt)
TEAM_RATINGS = {
    "Brazil":        {"attack": 1.90, "defense": 0.72, "elo": 2050},
    "France":        {"attack": 1.82, "defense": 0.70, "elo": 2010},
    "Argentina":     {"attack": 1.85, "defense": 0.75, "elo": 2030},
    "Spain":         {"attack": 1.78, "defense": 0.68, "elo": 1990},
    "England":       {"attack": 1.72, "defense": 0.74, "elo": 1960},
    "Germany":       {"attack": 1.65, "defense": 0.78, "elo": 1940},
    "Portugal":      {"attack": 1.70, "defense": 0.80, "elo": 1950},
    "Netherlands":   {"attack": 1.60, "defense": 0.83, "elo": 1930},
    "Italy":         {"attack": 1.42, "defense": 0.70, "elo": 1900},
    "Croatia":       {"attack": 1.35, "defense": 0.85, "elo": 1870},
    "Colombia":      {"attack": 1.52, "defense": 0.90, "elo": 1860},
    "Uruguay":       {"attack": 1.42, "defense": 0.83, "elo": 1850},
    "Denmark":       {"attack": 1.35, "defense": 0.80, "elo": 1840},
    "Morocco":       {"attack": 1.30, "defense": 0.76, "elo": 1830},
    "Japan":         {"attack": 1.35, "defense": 0.86, "elo": 1820},
    "Serbia":        {"attack": 1.32, "defense": 0.93, "elo": 1800},
    "Mexico":        {"attack": 1.30, "defense": 0.93, "elo": 1790},
    "USA":           {"attack": 1.25, "defense": 0.93, "elo": 1780},
    "South Korea":   {"attack": 1.25, "defense": 0.93, "elo": 1770},
    "Ecuador":       {"attack": 1.20, "defense": 0.98, "elo": 1750},
    "Canada":        {"attack": 1.20, "defense": 0.98, "elo": 1740},
    "Turkey":        {"attack": 1.22, "defense": 1.00, "elo": 1730},
    "Austria":       {"attack": 1.20, "defense": 0.98, "elo": 1720},
    "Senegal":       {"attack": 1.20, "defense": 0.93, "elo": 1710},
    "Switzerland":   {"attack": 1.15, "defense": 0.90, "elo": 1700},
    "Venezuela":     {"attack": 1.10, "defense": 1.05, "elo": 1680},
    "Scotland":      {"attack": 1.10, "defense": 1.03, "elo": 1670},
    "Ukraine":       {"attack": 1.10, "defense": 1.05, "elo": 1660},
    "Hungary":       {"attack": 1.05, "defense": 1.08, "elo": 1640},
    "Australia":     {"attack": 1.05, "defense": 1.08, "elo": 1630},
    "Cameroon":      {"attack": 1.05, "defense": 1.10, "elo": 1620},
    "Iran":          {"attack": 1.00, "defense": 1.10, "elo": 1610},
    "Nigeria":       {"attack": 1.12, "defense": 1.06, "elo": 1620},
    "Ivory Coast":   {"attack": 1.12, "defense": 1.04, "elo": 1625},
    "Algeria":       {"attack": 1.05, "defense": 1.06, "elo": 1615},
    "Tunisia":       {"attack": 1.00, "defense": 1.08, "elo": 1600},
    "Egypt":         {"attack": 1.05, "defense": 1.04, "elo": 1610},
    "South Africa":  {"attack": 0.95, "defense": 1.10, "elo": 1580},
    "Saudi Arabia":  {"attack": 1.00, "defense": 1.10, "elo": 1590},
    "Costa Rica":    {"attack": 0.90, "defense": 1.08, "elo": 1570},
    "Honduras":      {"attack": 0.85, "defense": 1.18, "elo": 1540},
    "Jamaica":       {"attack": 0.85, "defense": 1.18, "elo": 1530},
    "Panama":        {"attack": 0.88, "defense": 1.14, "elo": 1550},
    "Iraq":          {"attack": 0.90, "defense": 1.14, "elo": 1560},
    "China":         {"attack": 0.85, "defense": 1.18, "elo": 1530},
    "Uzbekistan":    {"attack": 0.90, "defense": 1.14, "elo": 1555},
    "El Salvador":   {"attack": 0.75, "defense": 1.28, "elo": 1490},
    "New Zealand":   {"attack": 0.75, "defense": 1.28, "elo": 1480},
}

# Kommende gruppe-kamper (første runde, eksempel)
import datetime

def get_group_fixtures():
    fixtures = []
    base = datetime.date(2026, 6, 11)
    match_id = 1
    for group, teams in GROUPS.items():
        # Hver gruppe: 3 kamper (4 lag → runde-robin 3 runder, 2 kamper per dag)
        combos = [(teams[0], teams[1]), (teams[2], teams[3]),
                  (teams[0], teams[2]), (teams[1], teams[3]),
                  (teams[0], teams[3]), (teams[1], teams[2])]
        for i, (home, away) in enumerate(combos):
            day_offset = (i // 2) * 2
            fixtures.append({
                "id": match_id,
                "group": group,
                "home": home,
                "away": away,
                "date": str(base + datetime.timedelta(days=day_offset)),
                "home_score": None,
                "away_score": None,
                "stage": "Gruppe"
            })
            match_id += 1
    return fixtures

# Historiske VM-resultater (forenklet) for modellkalibrering
HISTORICAL_WC_RESULTS = [
    # WC 2022 utvalg
    {"home": "Argentina", "away": "France",      "home_score": 3, "away_score": 3},
    {"home": "France",    "away": "Morocco",     "home_score": 2, "away_score": 0},
    {"home": "Brazil",    "away": "Croatia",     "home_score": 1, "away_score": 1},
    {"home": "England",   "away": "France",      "home_score": 1, "away_score": 2},
    {"home": "Germany",   "away": "Japan",       "home_score": 1, "away_score": 2},
    {"home": "Spain",     "away": "Germany",     "home_score": 1, "away_score": 1},
    {"home": "Portugal",  "away": "Morocco",     "home_score": 0, "away_score": 1},
    {"home": "Netherlands","away": "Argentina",  "home_score": 2, "away_score": 2},
    {"home": "USA",       "away": "Iran",        "home_score": 1, "away_score": 0},
    {"home": "Australia", "away": "Denmark",     "home_score": 1, "away_score": 0},
    {"home": "Japan",     "away": "Spain",       "home_score": 2, "away_score": 1},
    {"home": "Morocco",   "away": "Belgium",     "home_score": 2, "away_score": 0},
    {"home": "Senegal",   "away": "Ecuador",     "home_score": 2, "away_score": 1},
    {"home": "Croatia",   "away": "Canada",      "home_score": 4, "away_score": 1},
    {"home": "Uruguay",   "away": "South Korea", "home_score": 0, "away_score": 0},
    # WC 2018 utvalg
    {"home": "France",    "away": "Croatia",     "home_score": 4, "away_score": 2},
    {"home": "England",   "away": "Croatia",     "home_score": 1, "away_score": 2},
    {"home": "Germany",   "away": "Mexico",      "home_score": 0, "away_score": 1},
    {"home": "Brazil",    "away": "Belgium",     "home_score": 1, "away_score": 2},
    {"home": "Spain",     "away": "Russia",      "home_score": 1, "away_score": 1},
    {"home": "Argentina", "away": "Croatia",     "home_score": 0, "away_score": 3},
    {"home": "Japan",     "away": "Senegal",     "home_score": 2, "away_score": 2},
    {"home": "Uruguay",   "away": "Portugal",    "home_score": 2, "away_score": 1},
]

# Demo bookmaker-odds for kommende kamper (1X2)
DEMO_ODDS = {
    ("Brazil",       "Panama"):      {"home": 1.15, "draw": 8.00, "away": 18.0},
    ("France",       "Uruguay"):     {"home": 1.55, "draw": 4.00, "away": 6.50},
    ("Argentina",    "Jamaica"):     {"home": 1.12, "draw": 9.00, "away": 22.0},
    ("Germany",      "Costa Rica"):  {"home": 1.30, "draw": 5.50, "away": 10.0},
    ("Spain",        "Honduras"):    {"home": 1.18, "draw": 7.50, "away": 16.0},
    ("England",      "New Zealand"): {"home": 1.20, "draw": 7.00, "away": 14.0},
    ("Netherlands",  "China"):       {"home": 1.25, "draw": 6.50, "away": 12.0},
    ("Portugal",     "El Salvador"): {"home": 1.14, "draw": 8.50, "away": 20.0},
    ("Italy",        "Ukraine"):     {"home": 1.65, "draw": 3.80, "away": 5.50},
    ("USA",          "Ecuador"):     {"home": 1.80, "draw": 3.60, "away": 4.80},
    ("Mexico",       "Venezuela"):   {"home": 1.50, "draw": 4.20, "away": 7.00},
    ("Canada",       "Colombia"):    {"home": 2.10, "draw": 3.40, "away": 3.60},
    ("South Korea",  "Serbia"):      {"home": 2.30, "draw": 3.20, "away": 3.20},
    ("Japan",        "Scotland"):    {"home": 1.75, "draw": 3.70, "away": 5.00},
    ("Morocco",      "Denmark"):     {"home": 2.40, "draw": 3.20, "away": 3.00},
    ("Senegal",      "Austria"):     {"home": 2.00, "draw": 3.30, "away": 4.00},
    ("Turkey",       "Cameroon"):    {"home": 1.85, "draw": 3.50, "away": 4.50},
    ("Nigeria",      "Australia"):   {"home": 1.90, "draw": 3.40, "away": 4.20},
    ("Ivory Coast",  "Iran"):        {"home": 1.75, "draw": 3.70, "away": 5.00},
    ("Egypt",        "Saudi Arabia"):{"home": 1.95, "draw": 3.30, "away": 4.00},
    ("Algeria",      "Switzerland"): {"home": 2.80, "draw": 3.10, "away": 2.60},
    ("Tunisia",      "Hungary"):     {"home": 2.20, "draw": 3.30, "away": 3.30},
    ("South Africa", "Croatia"):     {"home": 4.00, "draw": 3.50, "away": 1.90},
    ("Panama",       "Ecuador"):     {"home": 3.50, "draw": 3.30, "away": 2.10},
    ("Uzbekistan",   "Iraq"):        {"home": 2.10, "draw": 3.20, "away": 3.60},
}
