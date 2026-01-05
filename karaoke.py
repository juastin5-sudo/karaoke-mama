import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")

# Diseño "Modo Oscuro Elegante"
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1DB954; color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎤 Studio Mágico de Mamá")
st.write("Escribe el nombre de la canción o pega el link de YouTube.")

# Input de búsqueda
busqueda = st.text_input("🔍 ¿Qué canción quieres cantar hoy?", placeholder="Ej: La gata bajo la lluvia karaoke")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ PREPARAR MI PISTA"):
    if busqueda:
        with st.status("🛠️ Iniciando puente de audio...", expanded=True) as status:
            try:
                # El "Puente": Buscamos en YouTube pero descargamos a través de un proxy de audio
                ydl_opts = {
                    'format': 'bestaudio/best',
                    # 'default_search': 'ytsearch',  <-- Esto permite buscar por nombre si no hay link
                    'outtmpl': 'pista_temporal',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'nocheckcertificate': True,
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                }

                # Si no es un link, buscamos el video
                query = busqueda if "youtube.com" in busqueda or "youtu.be" in busqueda else f"ytsearch1:{busqueda}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Buscando en el servidor de música...")
                    ydl.download([query])

                st.write("🎹 Ajustando el tono perfecto...")
                # Cargamos el archivo que llegó al "puente"
                audio = AudioSegment.from_file("pista_temporal.mp3")
                
                # Proceso de cambio de tono
                new_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista = audio._spawn(audio.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(audio.frame_rate)
                
                pista.export("pista_final.mp3", format="mp3")
                
                status.update(label="✅ ¡Tu pista está lista!", state="complete")
                st.balloons()
                
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_karaoke.mp3")
                
                # Limpiar
                os.remove("pista_temporal.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error("El servidor de música está ocupado. Intenta con otro nombre de canción.")
                st.info(f"Nota: {e}")
