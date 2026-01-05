import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

# Configuración visual
st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎤 El Studio de Mamá</h1>", unsafe_allow_html=True)
st.write("---")

url = st.text_input("🔗 Enlace de YouTube:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ ¡CREAR PISTA!"):
    if url:
        with st.spinner("Procesando tu música..."):
            try:
                # Opciones de descarga (con disfraz para evitar el 403)
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'pista_mama',
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Cambio de tono con Pydub
                sound = AudioSegment.from_file("pista_mama.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("resultado.mp3", format="mp3")

                st.balloons()
                st.audio("resultado.mp3")
                with open("resultado.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_karaoke.mp3")
                
                # Limpiar archivos para no llenar el servidor
                os.remove("pista_mama.mp3")
                if os.path.exists("resultado.mp3"):
                    os.remove("resultado.mp3")

            except Exception as e:
                st.error(f"Ocurrió un detalle: {e}")
