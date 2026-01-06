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
st.write("Buscando versiones completas en el puente Bandcamp (Sin YouTube).")

busqueda = st.text_input("🔍 ¿Qué canción quieres hoy?", placeholder="Ej: Amor Eterno Rocio Durcal")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ PREPARAR MI PISTA"):
    if busqueda:
        with st.status("🚀 Conectando con el puente de música completa...", expanded=True) as status:
            try:
                # MOTOR BANDCAMP: Canciones completas y sin bloqueos de robot
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'pista_temporal',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'default_search': 'bcsearch', # <--- BUSCADOR BANDCAMP
                    'nocheckcertificate': True,
                    'quiet': True,
                }

                query = f"bcsearch1:{busqueda} karaoke"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Descargando archivo desde Bandcamp...")
                    ydl.download([query])

                st.write("🎹 Ajustando el tono perfecto...")
                audio = AudioSegment.from_file("pista_temporal.mp3")
                
                # Verificamos que sea más larga que los 37 segundos de antes
                duracion_seg = len(audio) / 1000
                if duracion_seg < 60:
                    st.warning("⚠️ El resultado es corto. Prueba siendo más específico con el nombre.")

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
                st.error("No encontramos esa canción en este puente. Prueba con otro nombre.")
                st.info(f"Nota técnica: {e}")
