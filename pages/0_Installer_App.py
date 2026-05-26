import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Installer appen — VM 2026",
    page_icon="📲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("📲 Legg appen på hjemskjermen")
st.markdown("Ingen App Store nødvendig. Scan QR-koden eller følg instruksjonene under.")

st.markdown("---")

# ── Auto QR-kode (henter sin egen URL via JavaScript) ───────────────────────
st.subheader("📷 QR-kode — scan med telefonen")
st.caption("Koden genereres automatisk for denne siden")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  body { background: #0E1117; display: flex; flex-direction: column;
         align-items: center; justify-content: center; margin: 0; padding: 16px; }
  #qrcode canvas, #qrcode img { border-radius: 12px; }
  #url-label { color: #888; font-size: 0.78rem; margin-top: 10px;
                font-family: sans-serif; word-break: break-all; text-align: center; max-width: 260px; }
  #status { color: #1DB954; font-size: 0.85rem; font-family: sans-serif; margin-bottom: 8px; }
</style>
</head>
<body>
<div id="status">Genererer QR-kode...</div>
<div id="qrcode"></div>
<div id="url-label"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script>
  // Hent URL fra foreldrevinduet (Streamlit-appen)
  var appUrl = "";
  try {
    appUrl = window.parent.location.href.split("?")[0].split("#")[0];
    // Fjern /0_Installer_App-segmentet for å få rot-URL
    appUrl = appUrl.replace(/\\/0_Installer_App$/, "").replace(/\\/0_Installer_App\\/$/, "");
  } catch(e) {
    appUrl = window.location.href;
  }

  var el = document.getElementById("qrcode");
  var lbl = document.getElementById("url-label");
  var status = document.getElementById("status");

  if (appUrl && appUrl.startsWith("http")) {
    new QRCode(el, {
      text: appUrl,
      width: 220,
      height: 220,
      colorDark: "#1DB954",
      colorLight: "#0E1117",
      correctLevel: QRCode.CorrectLevel.M
    });
    lbl.textContent = appUrl;
    status.textContent = "✅ Scan med telefonen din";
  } else {
    status.textContent = "Kunne ikke hente URL automatisk";
    status.style.color = "#ff4b4b";
  }
</script>
</body>
</html>
""", height=320)

st.markdown("---")

# ── Enhetsdeteksjon + instruksjoner ──────────────────────────────────────────
# JavaScript-basert enhetsdeteksjon som viser riktig instruksjon
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  body { background: #0E1117; font-family: sans-serif; color: #FAFAFA;
         margin: 0; padding: 8px 0; }
  .card { background: #1A1D27; border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; }
  .card h3 { margin: 0 0 0.7rem 0; font-size: 1.05rem; color: #1DB954; }
  .step { display: flex; gap: 10px; margin-bottom: 0.5rem; font-size: 0.9rem; line-height: 1.4; }
  .num { background: #1DB954; color: #000; border-radius: 50%; width: 22px; height: 22px;
         display: flex; align-items: center; justify-content: center;
         font-weight: 700; font-size: 0.8rem; flex-shrink: 0; margin-top: 1px; }
  .tip { font-size: 0.8rem; color: #888; margin-top: 0.6rem; }
  .highlight { color: #1DB954; font-weight: 600; }
</style>
</head>
<body>
<div id="instructions"></div>
<script>
  var ua = navigator.userAgent;
  var isIOS = /iPad|iPhone|iPod/.test(ua);
  var isAndroid = /Android/.test(ua);
  var el = document.getElementById("instructions");

  if (isIOS) {
    el.innerHTML = `
      <div class="card">
        <h3>📱 iPhone / iPad — Safari</h3>
        <div class="step"><div class="num">1</div><div>Åpne appen i <span class="highlight">Safari</span> — ikke Chrome eller Firefox</div></div>
        <div class="step"><div class="num">2</div><div>Trykk på <span class="highlight">Del-ikonet ⬆</span> nederst på skjermen</div></div>
        <div class="step"><div class="num">3</div><div>Scroll ned og trykk <span class="highlight">"Legg til på Hjem-skjerm"</span></div></div>
        <div class="step"><div class="num">4</div><div>Gi den navnet <span class="highlight">VM 2026</span> og trykk <span class="highlight">Legg til</span></div></div>
        <div class="tip">✅ Et VM-ikon dukker opp på hjemskjermen — åpner fullskjerm som en app</div>
      </div>`;
  } else if (isAndroid) {
    el.innerHTML = `
      <div class="card">
        <h3>🤖 Android — Chrome</h3>
        <div class="step"><div class="num">1</div><div>Åpne appen i <span class="highlight">Chrome</span></div></div>
        <div class="step"><div class="num">2</div><div>Trykk på <span class="highlight">⋮</span> (tre prikker) øverst til høyre</div></div>
        <div class="step"><div class="num">3</div><div>Velg <span class="highlight">"Legg til på startskjermen"</span></div></div>
        <div class="step"><div class="num">4</div><div>Bekreft med <span class="highlight">Legg til</span></div></div>
        <div class="tip">✅ Appen vises på startskjermen din</div>
      </div>`;
  } else {
    el.innerHTML = `
      <div class="card">
        <h3>📱 iPhone / iPad — Safari</h3>
        <div class="step"><div class="num">1</div><div>Åpne appen i <span class="highlight">Safari</span></div></div>
        <div class="step"><div class="num">2</div><div>Trykk <span class="highlight">Del-ikonet ⬆</span> nederst</div></div>
        <div class="step"><div class="num">3</div><div>Velg <span class="highlight">"Legg til på Hjem-skjerm"</span></div></div>
        <div class="step"><div class="num">4</div><div>Trykk <span class="highlight">Legg til</span></div></div>
      </div>
      <div class="card">
        <h3>🤖 Android — Chrome</h3>
        <div class="step"><div class="num">1</div><div>Åpne appen i <span class="highlight">Chrome</span></div></div>
        <div class="step"><div class="num">2</div><div>Trykk <span class="highlight">⋮</span> øverst til høyre</div></div>
        <div class="step"><div class="num">3</div><div>Velg <span class="highlight">"Legg til på startskjermen"</span></div></div>
      </div>
      <div class="card">
        <h3>💻 Desktop (Chrome/Edge)</h3>
        <div class="step"><div class="num">1</div><div>Se etter <span class="highlight">⊕-ikonet</span> i adressefeltet til høyre</div></div>
        <div class="step"><div class="num">2</div><div>Klikk og velg <span class="highlight">"Installer"</span></div></div>
        <div class="tip">Appen åpnes da i sitt eget vindu — uten nettleser-rammer</div>
      </div>`;
  }
</script>
</body>
</html>
""", height=420)

st.markdown("---")
st.caption("VM 2026 Predictor · Poisson + Monte Carlo · Delt med venner via nettlink")
