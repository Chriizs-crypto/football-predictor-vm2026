import streamlit as st
import os

st.set_page_config(page_title="VM Legends Quiz", page_icon="🏆", layout="centered")
st.title("🏆 VM Legends Quiz")
st.caption("Gjett VM-legender fra samlekort · Henter Wikipedia-bilder automatisk")

# Prøv å laste quiz-filene fra søskermappe
quiz_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "Football Legends Quiz"
)
html_path = os.path.join(quiz_dir, "index.html")
data_path  = os.path.join(quiz_dir, "data.js")

if os.path.exists(html_path) and os.path.exists(data_path):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    with open(data_path, encoding="utf-8") as f:
        data_js = f.read()

    # Inline data.js slik at alt er self-contained i iframe
    combined = html.replace('<script src="data.js"></script>', f'<script>{data_js}</script>')

    st.components.v1.html(combined, height=900, scrolling=True)

else:
    st.info(
        "Quizen lastes fra `Football Legends Quiz/index.html`.\n\n"
        "Mappen forventes å ligge ved siden av `Football Predictor/`:\n"
        "```\n"
        "Projects/\n"
        "  Football Predictor/   ← denne appen\n"
        "  Football Legends Quiz/ ← quiz-filer her\n"
        "```\n"
        "Du kan også [åpne quizen direkte](../Football%20Legends%20Quiz/index.html) som en egen fil."
    )
    st.markdown("---")
    st.subheader("Spill direkte")
    st.markdown(
        "Åpne `Football Legends Quiz/index.html` i nettleseren for full opplevelse — "
        "kan installeres som app på iPhone/Android."
    )
