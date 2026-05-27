"""
VM 2026 demo-data. Grupper og lag basert på offisiell trekning (5. des 2025).
Brukes som fallback når API-nøkler ikke er konfigurert.
"""

GROUPS = {
    "A": ["Mexico",    "South Africa",        "South Korea",  "Czech Republic"],
    "B": ["Canada",    "Bosnia & Herzegovina", "Qatar",        "Switzerland"],
    "C": ["Brazil",    "Morocco",             "Haiti",        "Scotland"],
    "D": ["USA",       "Paraguay",            "Australia",    "Turkey"],
    "E": ["Germany",   "Curaçao",             "Ivory Coast",  "Ecuador"],
    "F": ["Netherlands","Japan",              "Sweden",       "Tunisia"],
    "G": ["Belgium",   "Egypt",               "Iran",         "New Zealand"],
    "H": ["Spain",     "Cape Verde",          "Saudi Arabia", "Uruguay"],
    "I": ["France",    "Senegal",             "Iraq",         "Norway"],
    "J": ["Argentina", "Algeria",             "Austria",      "Jordan"],
    "K": ["Portugal",  "DR Congo",            "Uzbekistan",   "Colombia"],
    "L": ["England",   "Croatia",             "Ghana",        "Panama"],
}

# attack = forventet mål scoret per kamp (1.0 = snitt)
# defense = forventet mål sluppet inn per kamp (lavere = bedre)
TEAM_RATINGS = {
    # Topp-tier
    "Brazil":               {"attack": 1.90, "defense": 0.72, "elo": 2050},
    "Argentina":            {"attack": 1.85, "defense": 0.75, "elo": 2030},
    "France":               {"attack": 1.82, "defense": 0.70, "elo": 2010},
    "Spain":                {"attack": 1.78, "defense": 0.68, "elo": 1990},
    "Belgium":              {"attack": 1.72, "defense": 0.78, "elo": 1960},
    "England":              {"attack": 1.72, "defense": 0.74, "elo": 1960},
    "Germany":              {"attack": 1.65, "defense": 0.78, "elo": 1940},
    "Portugal":             {"attack": 1.70, "defense": 0.80, "elo": 1950},
    "Netherlands":          {"attack": 1.60, "defense": 0.83, "elo": 1930},
    # Andrenivå
    "Norway":               {"attack": 1.52, "defense": 0.90, "elo": 1820},
    "Sweden":               {"attack": 1.42, "defense": 0.88, "elo": 1800},
    "Morocco":              {"attack": 1.30, "defense": 0.76, "elo": 1830},
    "Japan":                {"attack": 1.35, "defense": 0.86, "elo": 1820},
    "Croatia":              {"attack": 1.35, "defense": 0.85, "elo": 1870},
    "Colombia":             {"attack": 1.52, "defense": 0.90, "elo": 1860},
    "Uruguay":              {"attack": 1.42, "defense": 0.83, "elo": 1850},
    "USA":                  {"attack": 1.25, "defense": 0.93, "elo": 1780},
    "Mexico":               {"attack": 1.30, "defense": 0.93, "elo": 1790},
    "South Korea":          {"attack": 1.25, "defense": 0.93, "elo": 1770},
    "Ecuador":              {"attack": 1.20, "defense": 0.98, "elo": 1750},
    "Czech Republic":       {"attack": 1.25, "defense": 0.95, "elo": 1740},
    "Canada":               {"attack": 1.20, "defense": 0.98, "elo": 1740},
    "Turkey":               {"attack": 1.22, "defense": 1.00, "elo": 1730},
    "Austria":              {"attack": 1.20, "defense": 0.98, "elo": 1720},
    "Senegal":              {"attack": 1.20, "defense": 0.93, "elo": 1710},
    "Switzerland":          {"attack": 1.15, "defense": 0.90, "elo": 1700},
    "Paraguay":             {"attack": 1.18, "defense": 1.02, "elo": 1680},
    "Bosnia & Herzegovina": {"attack": 1.20, "defense": 1.02, "elo": 1650},
    "Algeria":              {"attack": 1.05, "defense": 1.06, "elo": 1615},
    "Ivory Coast":          {"attack": 1.12, "defense": 1.04, "elo": 1625},
    "Ghana":                {"attack": 1.10, "defense": 1.08, "elo": 1620},
    "DR Congo":             {"attack": 1.08, "defense": 1.06, "elo": 1580},
    "Tunisia":              {"attack": 1.00, "defense": 1.08, "elo": 1600},
    "Egypt":                {"attack": 1.05, "defense": 1.04, "elo": 1610},
    "South Africa":         {"attack": 0.95, "defense": 1.10, "elo": 1580},
    "Scotland":             {"attack": 1.10, "defense": 1.03, "elo": 1670},
    "Australia":            {"attack": 1.05, "defense": 1.08, "elo": 1630},
    "Uzbekistan":           {"attack": 0.90, "defense": 1.14, "elo": 1555},
    "Iraq":                 {"attack": 0.90, "defense": 1.14, "elo": 1560},
    "Saudi Arabia":         {"attack": 1.00, "defense": 1.10, "elo": 1590},
    "Iran":                 {"attack": 1.00, "defense": 1.10, "elo": 1610},
    "Cape Verde":           {"attack": 0.95, "defense": 1.10, "elo": 1560},
    "Jordan":               {"attack": 0.80, "defense": 1.18, "elo": 1500},
    "Qatar":                {"attack": 0.80, "defense": 1.18, "elo": 1530},
    "New Zealand":          {"attack": 0.75, "defense": 1.28, "elo": 1480},
    "Panama":               {"attack": 0.88, "defense": 1.14, "elo": 1550},
    "Haiti":                {"attack": 0.68, "defense": 1.32, "elo": 1440},
    "Curaçao":              {"attack": 0.60, "defense": 1.42, "elo": 1380},
}

import datetime

def get_group_fixtures():
    fixtures = []
    base = datetime.date(2026, 6, 11)
    match_id = 1
    for group, teams in GROUPS.items():
        combos = [(teams[0], teams[1]), (teams[2], teams[3]),
                  (teams[0], teams[2]), (teams[1], teams[3]),
                  (teams[0], teams[3]), (teams[1], teams[2])]
        for i, (home, away) in enumerate(combos):
            day_offset = (i // 2) * 2
            fixtures.append({
                "id":         match_id,
                "group":      group,
                "home":       home,
                "away":       away,
                "date":       str(base + datetime.timedelta(days=day_offset)),
                "home_score": None,
                "away_score": None,
                "stage":      "Gruppe",
                "status":     "NS",
            })
            match_id += 1
    return fixtures


HISTORICAL_WC_RESULTS = [
    # WC 2022
    {"home": "Argentina",   "away": "France",      "home_score": 3, "away_score": 3},
    {"home": "France",      "away": "Morocco",     "home_score": 2, "away_score": 0},
    {"home": "Brazil",      "away": "Croatia",     "home_score": 1, "away_score": 1},
    {"home": "England",     "away": "France",      "home_score": 1, "away_score": 2},
    {"home": "Germany",     "away": "Japan",       "home_score": 1, "away_score": 2},
    {"home": "Spain",       "away": "Germany",     "home_score": 1, "away_score": 1},
    {"home": "Portugal",    "away": "Morocco",     "home_score": 0, "away_score": 1},
    {"home": "Netherlands", "away": "Argentina",   "home_score": 2, "away_score": 2},
    {"home": "USA",         "away": "Iran",        "home_score": 1, "away_score": 0},
    {"home": "Australia",   "away": "Denmark",     "home_score": 1, "away_score": 0},
    {"home": "Japan",       "away": "Spain",       "home_score": 2, "away_score": 1},
    {"home": "Morocco",     "away": "Belgium",     "home_score": 2, "away_score": 0},
    {"home": "Senegal",     "away": "Ecuador",     "home_score": 2, "away_score": 1},
    {"home": "Croatia",     "away": "Canada",      "home_score": 4, "away_score": 1},
    {"home": "Uruguay",     "away": "South Korea", "home_score": 0, "away_score": 0},
    # WC 2018
    {"home": "France",      "away": "Croatia",     "home_score": 4, "away_score": 2},
    {"home": "England",     "away": "Croatia",     "home_score": 1, "away_score": 2},
    {"home": "Germany",     "away": "Mexico",      "home_score": 0, "away_score": 1},
    {"home": "Brazil",      "away": "Belgium",     "home_score": 1, "away_score": 2},
    {"home": "Argentina",   "away": "Croatia",     "home_score": 0, "away_score": 3},
    {"home": "Japan",       "away": "Senegal",     "home_score": 2, "away_score": 2},
    {"home": "Uruguay",     "away": "Portugal",    "home_score": 2, "away_score": 1},
]

# Demo-odds for utvalgte gruppekamper (nøkkelkamper per gruppe)
DEMO_ODDS = {
    # Gruppe A
    ("Mexico",      "South Africa"):        {"home": 1.52, "draw": 4.10, "away": 6.50},
    ("South Korea", "Czech Republic"):      {"home": 2.10, "draw": 3.30, "away": 3.60},
    ("Mexico",      "South Korea"):         {"home": 1.75, "draw": 3.60, "away": 5.00},
    # Gruppe B
    ("Canada",      "Bosnia & Herzegovina"):{"home": 1.95, "draw": 3.40, "away": 4.20},
    ("Qatar",       "Switzerland"):         {"home": 5.50, "draw": 4.00, "away": 1.55},
    # Gruppe C
    ("Brazil",      "Morocco"):             {"home": 1.45, "draw": 4.50, "away": 7.50},
    ("Haiti",       "Scotland"):            {"home": 4.20, "draw": 3.50, "away": 1.90},
    ("Brazil",      "Scotland"):            {"home": 1.18, "draw": 7.50, "away": 16.0},
    # Gruppe D
    ("USA",         "Paraguay"):            {"home": 1.70, "draw": 3.70, "away": 5.50},
    ("Australia",   "Turkey"):              {"home": 2.60, "draw": 3.20, "away": 2.70},
    # Gruppe E
    ("Germany",     "Curaçao"):             {"home": 1.08, "draw": 11.0, "away": 30.0},
    ("Ivory Coast", "Ecuador"):             {"home": 2.10, "draw": 3.30, "away": 3.60},
    ("Germany",     "Ivory Coast"):         {"home": 1.40, "draw": 4.80, "away": 8.00},
    # Gruppe F
    ("Netherlands", "Japan"):              {"home": 1.65, "draw": 3.80, "away": 5.50},
    ("Sweden",      "Tunisia"):             {"home": 1.75, "draw": 3.60, "away": 5.00},
    ("Netherlands", "Sweden"):              {"home": 1.80, "draw": 3.60, "away": 4.60},
    # Gruppe G
    ("Belgium",     "Egypt"):               {"home": 1.35, "draw": 5.00, "away": 9.00},
    ("Iran",        "New Zealand"):         {"home": 1.80, "draw": 3.60, "away": 4.80},
    # Gruppe H
    ("Spain",       "Cape Verde"):          {"home": 1.12, "draw": 9.00, "away": 22.0},
    ("Saudi Arabia","Uruguay"):             {"home": 3.10, "draw": 3.20, "away": 2.30},
    ("Spain",       "Uruguay"):             {"home": 1.70, "draw": 3.70, "away": 5.50},
    # Gruppe I
    ("France",      "Senegal"):             {"home": 1.50, "draw": 4.20, "away": 7.00},
    ("Iraq",        "Norway"):              {"home": 4.50, "draw": 3.80, "away": 1.75},
    ("France",      "Norway"):              {"home": 1.60, "draw": 4.00, "away": 6.00},
    # Gruppe J
    ("Argentina",   "Algeria"):             {"home": 1.22, "draw": 6.50, "away": 13.0},
    ("Austria",     "Jordan"):              {"home": 1.55, "draw": 4.00, "away": 6.50},
    # Gruppe K
    ("Portugal",    "DR Congo"):            {"home": 1.30, "draw": 5.50, "away": 10.0},
    ("Uzbekistan",  "Colombia"):            {"home": 3.50, "draw": 3.20, "away": 2.10},
    ("Portugal",    "Colombia"):            {"home": 1.75, "draw": 3.70, "away": 5.00},
    # Gruppe L
    ("England",     "Croatia"):             {"home": 1.65, "draw": 3.80, "away": 5.50},
    ("Ghana",       "Panama"):              {"home": 2.00, "draw": 3.30, "away": 3.80},
    ("England",     "Ghana"):              {"home": 1.40, "draw": 4.80, "away": 8.00},
}
