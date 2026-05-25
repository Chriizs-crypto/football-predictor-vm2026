def pct(value: float, decimals: int = 1) -> str:
    return f"{value * 100:.{decimals}f}%"


def odds_to_implied(odds: float) -> float:
    return round(1.0 / odds, 4) if odds > 0 else 0.0


def flag_emoji(team: str) -> str:
    flags = {
        "Brazil": "🇧🇷", "France": "🇫🇷", "Argentina": "🇦🇷", "Spain": "🇪🇸",
        "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Germany": "🇩🇪", "Portugal": "🇵🇹", "Netherlands": "🇳🇱",
        "Italy": "🇮🇹", "Croatia": "🇭🇷", "Colombia": "🇨🇴", "Uruguay": "🇺🇾",
        "Denmark": "🇩🇰", "Morocco": "🇲🇦", "Japan": "🇯🇵", "Serbia": "🇷🇸",
        "Mexico": "🇲🇽", "USA": "🇺🇸", "South Korea": "🇰🇷", "Ecuador": "🇪🇨",
        "Canada": "🇨🇦", "Turkey": "🇹🇷", "Austria": "🇦🇹", "Senegal": "🇸🇳",
        "Switzerland": "🇨🇭", "Venezuela": "🇻🇪", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Ukraine": "🇺🇦",
        "Hungary": "🇭🇺", "Australia": "🇦🇺", "Cameroon": "🇨🇲", "Iran": "🇮🇷",
        "Nigeria": "🇳🇬", "Ivory Coast": "🇨🇮", "Algeria": "🇩🇿", "Tunisia": "🇹🇳",
        "Egypt": "🇪🇬", "South Africa": "🇿🇦", "Saudi Arabia": "🇸🇦",
        "Costa Rica": "🇨🇷", "Honduras": "🇭🇳", "Jamaica": "🇯🇲", "Panama": "🇵🇦",
        "Iraq": "🇮🇶", "China": "🇨🇳", "Uzbekistan": "🇺🇿",
        "El Salvador": "🇸🇻", "New Zealand": "🇳🇿",
    }
    return flags.get(team, "🏳️")


def format_match_title(home: str, away: str) -> str:
    return f"{flag_emoji(home)} {home} vs {away} {flag_emoji(away)}"
