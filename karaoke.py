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

st.title("🎤 Studio de Mamá (Versión Completa)")
st.write("Buscando en servidores de música libre (No usa YouTube).")

busqueda = st.text_input("🔍 Escribe el nombre de la canción:", placeholder="Ej: Rocio Durcal Amor Eterno")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ PREPARAR CANCIÓN COMPLETA"):
    if busqueda:
        with st.status("🚀 Buscando en el puente de música libre...", expanded=True) as status:
            try:
                # CONFIGURACIÓN SIN YOUTUBE
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'pista_temporal',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    # Bloqueamos YouTube y forzamos buscadores de música abierta como Audiomack o Jamendo
                    'default_search': 'amsearch', # 'amsearch' busca en Audiomack (canciones completas)
                    'nocheckcertificate': True,
                    'quiet': True,
                }

                # Buscamos la canción completa
                query = f"amsearch1:{busqueda}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Descargando archivo desde el puente Audiomack...")
                    ydl.download([query])

                st.write("🎹 Cambiando el tono a la pista entera...")
                audio = AudioSegment.from_file("pista_temporal.mp3")
                
                # Proceso de cambio de tono
                new_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista = audio._spawn(audio.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(audio.frame_rate)
                pista.export("pista_final.mp3", format="mp3")
                
                status.update(label="✅ ¡Pista terminada!", state="complete")
                st.balloons()
                
                # Mostramos el tiempo real de la canción
                duracion_segundos = len(audio) / 1000
                st.success(f"Duración obtenida: {int(duracion_segundos // 60)} min {int(duracion_segundos % 60)} seg")
                
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3 COMPLETO", f, file_name="pista_completa.mp3")
                
                os.remove("pista_temporal.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error("No encontramos esa canción en el servidor libre. Prueba escribiendo el nombre del artista de nuevo.")
                st.info(f"Nota: {e}")
