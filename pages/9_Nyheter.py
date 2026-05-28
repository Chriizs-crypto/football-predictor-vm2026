import streamlit as st
import requests
import xml.etree.ElementTree as ET
import datetime

st.set_page_config(page_title="Nyheter – VM 2026", page_icon="📰", layout="centered")

st.markdown("""
<style>
.news-card {
    background: linear-gradient(135deg, #141929 0%, #0f1520 100%);
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.news-source {
    font-size: 0.65rem;
    color: #00dc82;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
}
.news-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f0f4ff;
    margin-bottom: 0.3rem;
    line-height: 1.35;
}
.news-desc {
    font-size: 0.8rem;
    color: #8b9cc3;
    line-height: 1.45;
    margin-bottom: 0.5rem;
}
.news-meta {
    font-size: 0.68rem;
    color: #4a5a7a;
}
.news-link {
    font-size: 0.75rem;
    color: #00dc82;
    text-decoration: none;
    font-weight: 600;
}
.section-banner {
    font-size: 0.72rem;
    color: #00dc82;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.4rem 0 0.7rem 0;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid #1e2d4a;
}
.no-news {
    text-align: center;
    color: #4a5a7a;
    padding: 1.5rem;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📰 Nyheter — VM 2026")
st.caption("Hentes fra BBC Sport og Sky Sports Football · Oppdateres automatisk hvert 30 min")

FEEDS = [
    {
        "name": "BBC Sport",
        "url":  "https://feeds.bbci.co.uk/sport/football/rss.xml",
        "icon": "🔴",
    },
    {
        "name": "Sky Sports Football",
        "url":  "https://www.skysports.com/rss/12040",
        "icon": "🔵",
    },
]

WC_KEYWORDS = [
    "world cup", "vm 2026", "2026", "fifa", "messi", "mbappé", "haaland",
    "ronaldo", "bellingham", "vinicius", "kane", "yamal", "musiala", "gyökeres",
    "england", "brazil", "argentina", "france", "germany", "spain", "portugal",
    "netherlands", "norway", "sweden", "morocco", "japan", "usa", "mexico",
    "injury", "skadet", "lineup", "squad", "tropp", "qualifier",
]


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_rss(url: str) -> list[dict]:
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "VM2026-App/1.0"})
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.content)
        items = []
        ns = {"media": "http://search.yahoo.com/mrss/"}
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            desc  = (item.findtext("description") or "").strip()
            link  = (item.findtext("link") or "").strip()
            pub   = (item.findtext("pubDate") or "").strip()
            items.append({
                "title": title,
                "desc":  desc[:200] + "…" if len(desc) > 200 else desc,
                "link":  link,
                "pub":   pub,
            })
        return items[:30]
    except Exception:
        return []


def is_wc_related(item: dict) -> bool:
    text = (item["title"] + " " + item["desc"]).lower()
    return any(kw in text for kw in WC_KEYWORDS)


# ── Hent og filtrer nyheter ───────────────────────────────────────────────────
filter_wc = st.toggle("Vis kun VM-relaterte nyheter", value=True)
st.markdown("---")

total_shown = 0

for feed in FEEDS:
    with st.spinner(f"Henter {feed['name']}…"):
        articles = fetch_rss(feed["url"])

    if filter_wc:
        articles = [a for a in articles if is_wc_related(a)]

    if not articles:
        continue

    st.markdown(f'<div class="section-banner">{feed["icon"]} {feed["name"]}</div>', unsafe_allow_html=True)

    for a in articles[:8]:
        title = a["title"]
        desc  = a["desc"]
        link  = a["link"]
        pub   = a["pub"]

        st.markdown(f"""
<div class="news-card">
  <div class="news-source">{feed['icon']} {feed['name']}</div>
  <div class="news-title">{title}</div>
  {"<div class='news-desc'>" + desc + "</div>" if desc else ""}
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span class="news-meta">🕐 {pub[:22] if pub else '–'}</span>
    {"<a class='news-link' href='" + link + "' target='_blank'>Les mer →</a>" if link else ""}
  </div>
</div>
""", unsafe_allow_html=True)
        total_shown += 1

if total_shown == 0:
    st.markdown("""
<div class="no-news">
  📡 Ingen nyheter funnet akkurat nå.<br>
  <span style="font-size:0.75rem;">RSS-kilder kan være midlertidig utilgjengelige. Prøv igjen om litt.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="font-size:0.7rem;color:#4a5a7a;text-align:center;">
⚠️ Nyheter hentes direkte fra BBC Sport og Sky Sports via RSS.<br>
Skader, oppstillinger og lagnyheter oppdateres av disse kildene — ikke av appen selv.<br>
For live injury-rapporter: sjekk offisielle FIFA-kanaler.
</div>
""", unsafe_allow_html=True)
