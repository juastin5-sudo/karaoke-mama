import audioop_lts
import sys
sys.modules['audioop'] = audioop_lts

import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎵", layout="centered")

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff7575;
        border: none;
    }
    .titulo {
        text-align: center;
        color: #FF4B4B;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<h1 class='titulo'>🎤 Karaoke Studio VIP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Crea tus pistas personalizadas en segundos</p>", unsafe_allow_html=True)
st.divider()

# --- CUERPO ---
col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input("🔗 Enlace de YouTube:", placeholder="Pega el link aquí...")

with col2:
    tono = st.select_slider("🎶 Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

st.write("") # Espacio en blanco

if st.button("✨ GENERAR MI PISTA"):
    if url:
        with st.status("🎼 Procesando audio...", expanded=True) as status:
            try:
                st.write("📥 Descargando de YouTube...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'temp_audio',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                st.write("🎹 Ajustando tono...")
                sound = AudioSegment.from_file("temp_audio.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("pista_lista.mp3", format="mp3")

                status.update(label="✅ ¡Pista lista!", state="complete", expanded=False)
                
                st.balloons() # ¡Globos de celebración!
                
                # REPRODUCTOR Y DESCARGA
                st.audio("pista_lista.mp3")
                with open("pista_lista.mp3", "rb") as file:
                    st.download_button(
                        label="⬇️ DESCARGAR MP3",
                        data=file,
                        file_name="mi_pista_karaoke.mp3",
                        mime="audio/mp3"
                    )
                
                os.remove("temp_audio.mp3")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("⚠️ Por favor, introduce un link válido.")

st.divider()
st.markdown("<p style='text-align: center; font-size: 0.8em; color: gray;'>Hecho con ❤️ para mamá</p>", unsafe_allow_html=True)

