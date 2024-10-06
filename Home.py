import streamlit as st
import leafmap.foliumap as leafmap
import time
import ollama
import sys


print(sys.executable)
print(sys.path)

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Project repository:
<https://github.com/massaindustries/EMISCANMK1>
"""
st.sidebar.title("Go Pro")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/CsBdfY1.png"
st.sidebar.image(logo)

# Customize page title
st.title("Interactive Map with Chatbot")

# Use columns to adjust layout
col1, col2 = st.columns([3, 1])  # La prima colonna è più grande (mappa), la seconda è più piccola (chatbot)

with col1:
    # Map section
    m = leafmap.Map(minimap_control=True)
    m.add_basemap("ESA WorldCover 2021")
    m.to_streamlit(height=500)

with col2:

    st.image("https://i.imgur.com/6hr2Wxy.png", use_column_width=True)

    # Chatbot section
    def stream_data(text):
        delay = 0.1  # Imposta un ritardo per il flusso dei dati
        for word in text.split():
            yield word + " "
            time.sleep(delay)

    # Input per il prompt (istruzione)
    instruction = st.chat_input("Ask Emiscan")

    if instruction:
        # Visualizza l'input dell'utente
        with st.chat_message("user"):
            st.write(instruction)

        # Elaborazione del prompt
        with st.spinner("Thinking ..."):
            result = ollama.chat(model="francescomassa/emiscanmk2", messages=[{
                "role": "user",
                "input": "",  # Nessun input aggiuntivo
                "content": instruction,
            }])

        # Estrae la risposta e la mostra
        response = result["message"]["content"]  # 'content' è il campo che contiene la risposta
        st.write_stream(stream_data(response))  # Mostra la risposta del chatbot
