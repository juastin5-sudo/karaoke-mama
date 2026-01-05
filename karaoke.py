import audioop_lts
import sys
sys.modules['audioop'] = audioop_lts

import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment
from static_ffmpeg import add_paths

# Activar motor de audio
add_paths()

st.set_page_config(page_title="Karaoke de Mamá", page_icon="🎤")

st.title("🎤 Studio de Pistas para Mamá")
st.markdown("Pega el link de YouTube, elige el tono y descarga tu pista.")

# Interfaz de la página
url = st.text_input("Enlace de YouTube:", placeholder="https://www.youtube.com/watch?v=...")
tono = st.select_slider("Bajar o subir tono (semitonos):", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ Generar Pista"):
    if url:
        with st.spinner("Descargando y procesando... espera un momento."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'temp_web_audio',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Procesar el tono
                sound = AudioSegment.from_file("temp_web_audio.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                
                # Guardar temporalmente para descargar
                pista.export("pista_lista.mp3", format="mp3")

                # Mostrar reproductor y botón de descarga
                with open("pista_lista.mp3", "rb") as file:
                    st.audio(file.read(), format="audio/mp3")
                    st.download_button(label="⬇️ DESCARGAR CANCIÓN", data=file, file_name="mi_pista_karaoke.mp3")
                
                # Limpiar archivos
                os.remove("temp_web_audio.mp3")
                os.remove("pista_lista.mp3")
                st.success("¡Tu pista está lista!")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Por favor, pon un link de YouTube.")
