import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎤 El Studio de Mamá")
st.write("Escribe el nombre de la canción y yo hago el puente por ti.")

busqueda = st.text_input("🔍 ¿Qué canción buscamos hoy?", placeholder="Ej: Amor Eterno Karaoke")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ PREPARAR MI PISTA"):
    if busqueda:
        with st.status("🚀 Conectando con el puente de audio...", expanded=True) as status:
            try:
                # EL TRUCO: Usamos un servidor "invitado" para saltar el bot-check
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'pista_temporal',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    # Este comando le dice a YouTube: "Soy un usuario de Android" (que casi nunca pide bot-check)
                    'extractor_args': {'youtube': {'player_client': ['android']}}, 
                    'nocheckcertificate': True,
                    'quiet': True,
                }

                # Si no es link, busca automáticamente
                query = busqueda if "youtube.com" in busqueda or "youtu.be" in busqueda else f"ytsearch1:{busqueda}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Descargando audio sin bloqueos...")
                    ydl.download([query])

                st.write("🎹 Ajustando el tono perfecto...")
                audio = AudioSegment.from_file("pista_temporal.mp3")
                new_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista = audio._spawn(audio.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(audio.frame_rate)
                pista.export("pista_final.mp3", format="mp3")
                
                status.update(label="✅ ¡Tu pista está lista!", state="complete")
                st.balloons()
                
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_karaoke.mp3")
                
                os.remove("pista_temporal.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error("YouTube está muy estricto hoy. Por favor, intenta escribir el nombre de la canción de forma diferente.")
                st.info("Tip: Intenta poner el nombre del artista + 'karaoke'.")
