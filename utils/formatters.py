def pct(value: float, decimals: int = 1) -> str:
    return f"{value * 100:.{decimals}f}%"


def odds_to_implied(odds: float) -> float:
    return round(1.0 / odds, 4) if odds > 0 else 0.0


def flag_emoji(team: str) -> str:
    flags = {
        # VM 2026 — alle 48 kvalifiserte lag
        "Brazil": "🇧🇷", "France": "🇫🇷", "Argentina": "🇦🇷", "Spain": "🇪🇸",
        "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Germany": "🇩🇪", "Portugal": "🇵🇹", "Netherlands": "🇳🇱",
        "Belgium": "🇧🇪", "Croatia": "🇭🇷", "Colombia": "🇨🇴", "Uruguay": "🇺🇾",
        "Norway": "🇳🇴", "Sweden": "🇸🇪", "Morocco": "🇲🇦", "Japan": "🇯🇵",
        "Mexico": "🇲🇽", "USA": "🇺🇸", "South Korea": "🇰🇷", "Ecuador": "🇪🇨",
        "Canada": "🇨🇦", "Turkey": "🇹🇷", "Austria": "🇦🇹", "Senegal": "🇸🇳",
        "Switzerland": "🇨🇭", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Australia": "🇦🇺", "Iran": "🇮🇷",
        "Ivory Coast": "🇨🇮", "Algeria": "🇩🇿", "Tunisia": "🇹🇳", "Egypt": "🇪🇬",
        "South Africa": "🇿🇦", "Saudi Arabia": "🇸🇦", "Panama": "🇵🇦", "Iraq": "🇮🇶",
        "Uzbekistan": "🇺🇿", "New Zealand": "🇳🇿", "Paraguay": "🇵🇾",
        "Czech Republic": "🇨🇿", "Bosnia & Herzegovina": "🇧🇦", "Qatar": "🇶🇦",
        "Haiti": "🇭🇹", "Curaçao": "🇨🇼", "Sweden": "🇸🇪", "Ghana": "🇬🇭",
        "DR Congo": "🇨🇩", "Cape Verde": "🇨🇻", "Jordan": "🇯🇴",
        # Ekstra / historiske
        "Denmark": "🇩🇰", "Italy": "🇮🇹", "Serbia": "🇷🇸", "Ukraine": "🇺🇦",
        "Nigeria": "🇳🇬", "Cameroon": "🇨🇲", "China": "🇨🇳",
    }
    return flags.get(team, "🏳️")


def format_match_title(home: str, away: str) -> str:
    return f"{flag_emoji(home)} {home} vs {away} {flag_emoji(away)}"
