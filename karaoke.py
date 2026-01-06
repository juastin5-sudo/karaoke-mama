import streamlit as st
import requests
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke de Mamá", page_icon="🎤")

# Estilo para que se vea muy fácil
st.markdown("<style>.stButton>button {width:100%; background-color: #25D366; color: white; height: 3em; font-weight: bold;}</style>", unsafe_allow_html=True)

st.title("🎤 Studio de Mamá")
st.write("Solo escribe el nombre de tu canción favorita:")

nombre_cancion = st.text_input("", placeholder="Ej: Amor Eterno Rocio Durcal")
tono = st.select_slider("🎶 ¿Subir o bajar el tono?", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ ¡PREPARAR MI CANCIÓN!"):
    if nombre_cancion:
        with st.spinner("Buscando tu música..."):
            try:
                # PASO 1: Buscamos en una base de datos abierta (ITunes/Deezer)
                search_url = f"https://itunes.apple.com/search?term={nombre_cancion}&entity=song&limit=1"
                res = requests.get(search_url).json()
                
                if res['resultCount'] > 0:
                    track = res['results'][0]
                    preview_url = track['previewUrl'] # Este link es directo al archivo
                    
                    st.write(f"🎵 Encontré: {track['trackName']} de {track['artistName']}")
                    
                    # PASO 2: Descarga directa (Sin bloqueos de YouTube)
                    audio_data = requests.get(preview_url).content
                    with open("temp.m4a", "wb") as f:
                        f.write(audio_data)
                    
                    # PASO 3: Cambio de tono con Pydub
                    audio = AudioSegment.from_file("temp.m4a")
                    new_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                    pista = audio._spawn(audio.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(audio.frame_rate)
                    
                    pista.export("final.mp3", format="mp3")
                    
                    st.success("¡Aquí tienes tu pista lista, mamá!")
                    st.audio("final.mp3")
                    with open("final.mp3", "rb") as f:
                        st.download_button("⬇️ DESCARGAR CANCIÓN", f, file_name="pista_para_mama.mp3")
                else:
                    st.error("No encontré esa canción. Prueba escribiendo el nombre diferente.")
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Pega un link primero.")

