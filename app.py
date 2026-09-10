import streamlit as st
import pandas as pd
import random

# Pagina-instellingen
st.set_page_config(page_title="Franse Woordjes Oefenen", page_icon="🇫🇷")
st.title("🇫🇷 Franse Woordjes Oefenen")

# 1. Woordenlijst laden
@st.cache_data
def laad_woorden():
    try:
        return pd.read_csv("woorden.csv", sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv("woorden.csv", sep=None, engine="python", encoding="cp1252")

try:
    df = laad_woorden()
except FileNotFoundError:
    st.error("Bestand 'woorden.csv' niet gevonden! Plaats dit bestand in dezelfde map.")
    st.stop()
except Exception as e:
    st.error(f"Er is een fout opgetreden bij het lezen van 'woorden.csv': {e}")
    st.stop()

# 2. Sessiestatus bijhouden
if "index" not in st.session_state:
    st.session_state.index = random.randint(0, len(df) - 1)
    st.session_state.score = 0
    st.session_state.pogingen = 0
    st.session_state.laatste_feedback = None

# 3. Kies de oefenrichting
optie = st.radio(
    "Wat wil je oefenen?",
    ("Frans ➡️ Nederlands", "Nederlands ➡️ Frans"),
    horizontal=True
)
richting = "FR_NL" if optie == "Frans ➡️ Nederlands" else "NL_FR"

# Woord ophalen uit het CSV-bestand
rij = df.iloc[st.session_state.index]
if richting == "FR_NL":
    te_vertalen = rij["Frans"]
    juiste_antwoord_ruw = rij["Nederlands"]
else:
    te_vertalen = rij["Nederlands"]
    juiste_antwoord_ruw = rij["Frans"]

# 4. Feedback van de vorige beurt tonen
if st.session_state.laatste_feedback:
    status, bericht = st.session_state.laatste_feedback
    if status == "success":
        st.success(bericht)
    else:
        st.error(bericht)

# 5. Interface tonen
st.subheader(f"Vertaal: **{te_vertalen}**")

met_formulier = st.form(key="quiz_form", clear_on_submit=True)
invoer = met_formulier.text_input("Jouw antwoord:")
knop = met_formulier.form_submit_button("Controleren")

if knop:
    st.session_state.pogingen += 1
    
    # Maak een lijst van alle toegestane antwoorden (gescheiden door '/')
    mogelijkheden = [optie.strip().lower() for optie in str(juiste_antwoord_ruw).split("/")]
    ingevoerd_antwoord = str(invoer).strip().lower()
    
    # Controleer of het ingevoerde antwoord in de lijst van opties staat
    if ingevoerd_antwoord in mogelijkheden:
        st.session_state.score += 1
        st.session_state.laatste_feedback = ("success", f"🎉 Goed zo! Goedgekeurd (mogelijkheden waren: **{juiste_antwoord_ruw}**)")
    else:
        st.session_state.laatste_feedback = ("error", f"❌ Helaas! Het juiste antwoord was: **{juiste_antwoord_ruw}**")
    
    # Kies een nieuw willekeurig woord en ververs de pagina
    st.session_state.index = random.randint(0, len(df) - 1)
    st.rerun()

# Score tonen
st.write("---")
st.write(f"**Score:** {st.session_state.score} / {st.session_state.pogingen}")