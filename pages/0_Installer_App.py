import streamlit as st
import qrcode
import qrcode.image.svg
from io import BytesIO

st.set_page_config(
    page_title="Installer appen — VM 2026",
    page_icon="📲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("📲 Legg appen på hjemskjermen")
st.markdown("Du trenger ikke laste ned noe fra App Store. Appen fungerer som en nettapp — men ser ut og føles som en vanlig app når du legger den på hjemskjermen.")

st.markdown("---")

# ── URL-input ──────────────────────────────────────────────────────────────
st.subheader("Steg 1 — Finn appens URL")
app_url = st.text_input(
    "Lim inn appens URL her (fra adressefeltet i nettleseren)",
    placeholder="https://din-app.streamlit.app",
    help="Åpne appen i nettleseren og kopier URL-en fra adressefeltet",
)

if app_url:
    # ── QR-kode ───────────────────────────────────────────────────────────
    st.subheader("Steg 2 — Scan QR-koden")
    st.caption("Del QR-koden med vennene dine så de kan åpne appen på sin telefon")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(app_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1DB954", back_color="#0E1117")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(buf, use_container_width=True)

    st.markdown("---")

# ── iPhone-instruksjoner ───────────────────────────────────────────────────
st.subheader("📱 iPhone (Safari)")
st.markdown("""
1. Åpne appen i **Safari** (ikke Chrome eller Firefox)
2. Trykk på **Del-ikonet** nederst på skjermen &nbsp;`⬆`
3. Scroll ned og trykk **"Legg til på Hjem-skjerm"**
4. Gi den et navn (f.eks. *VM 2026*) og trykk **Legg til**

Appen vises nå som et ikon på hjemskjermen din — akkurat som en vanlig app. ✅
""")

with st.expander("Se steg-for-steg bilder (tekst)"):
    st.markdown("""
    **I Safari:**
    - Adressefeltet øverst viser URL-en
    - Del-ikonet (firkant med pil opp) er **nederst i midten** av skjermen
    - "Legg til på Hjem-skjerm" finner du ved å scrolle ned i delelisten

    **Tips:** Skru telefonen til liggende modus hvis del-ikonet er vanskelig å se.
    """)

st.markdown("---")

# ── Android-instruksjoner ──────────────────────────────────────────────────
st.subheader("🤖 Android (Chrome)")
st.markdown("""
1. Åpne appen i **Chrome**
2. Trykk på **⋮** (tre prikker øverst til høyre)
3. Trykk **"Legg til på startskjermen"** eller **"Installer app"**
4. Bekreft med **Legg til**

Appen vises nå på hjemskjermen din. ✅
""")

st.markdown("---")

# ── Desktop-snarvei ────────────────────────────────────────────────────────
st.subheader("💻 Desktop (Chrome/Edge)")
st.markdown("""
I Chrome eller Edge kan du installere appen som en desktop-app:

1. Åpne appen i nettleseren
2. Se etter **installasjons-ikonet** (⊕) helt til høyre i adressefeltet
3. Klikk på det og velg **"Installer"**

Appen åpnes da i sitt eget vindu uten nettleser-rammer.
""")

st.markdown("---")
st.caption("VM 2026 Predictor · Poisson + Monte Carlo · Delt med venner via nettlink")
