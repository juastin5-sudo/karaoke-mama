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

st.title("🎤 Studio Mágico de Mamá")
st.write("Escribe el nombre de la canción. Este sistema no usa YouTube para evitar bloqueos.")

busqueda = st.text_input("🔍 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Amor Eterno Rocio Durcal")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ PREPARAR MI PISTA"):
    if busqueda:
        with st.status("🚀 Buscando música en el puente libre...", expanded=True) as status:
            try:
                # Opciones optimizadas para SoundCloud en servidores
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'pista_temporal',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'default_search': 'scsearch', 
                    'nocheckcertificate': True,
                    'quiet': True,
                }

                query = f"scsearch1:{busqueda}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Descargando audio desde el puente...")
                    ydl.download([query])

                st.write("🎹 Cambiando el tono de la canción...")
                audio = AudioSegment.from_file("pista_temporal.mp3")
                new_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista = audio._spawn(audio.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(audio.frame_rate)
                pista.export("pista_final.mp3", format="mp3")
                
                status.update(label="✅ ¡Listo! Descárgala abajo", state="complete")
                st.balloons()
                
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_karaoke.mp3")
                
                os.remove("pista_temporal.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error("Hubo un detalle técnico. Prueba escribiendo el nombre de forma diferente.")
                st.info(f"Nota: {e}")
