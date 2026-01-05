import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment
import random

st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")

# Estilo para que se vea profesional
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    .stButton>button { background-color: #e63946; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎤 El Studio de Mamá")
st.write("Pega el link y yo hago todo el trabajo por ti.")

url = st.text_input("🔗 Link de la canción (YouTube):")
tono = st.select_slider("🎶 ¿Qué tan bajo quieres el tono?", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ ¡HACER MAGIA!"):
    if url:
        with st.spinner("Descargando y preparando tu pista..."):
            try:
                # LISTA DE DISFRACES PARA ENGAÑAR A YOUTUBE
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                ]

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'cancion_mama',
                    'user_agent': random.choice(user_agents),
                    'nocheckcertificate': True,
                    'quiet': True,
                    'add_header': ['Accept-Language: es-ES,es;q=0.9']
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Procesar audio
                sound = AudioSegment.from_file("cancion_mama.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("pista_final.mp3", format="mp3")

                st.balloons()
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR CANCIÓN", f, file_name="tu_pista.mp3")
                
                os.remove("cancion_mama.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error("¡Ay! YouTube se puso difícil. Intenta con un video de 'Karaoke' (esos fallan menos) o espera 2 minutitos.")
    else:
        st.warning("⚠️ Primero pon un link, mamá.")
