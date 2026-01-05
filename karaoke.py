import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎤")

st.title("🎤 Studio de Pistas VIP")
st.markdown("Si un link da error, intenta con otro de un canal diferente.")

url = st.text_input("🔗 Enlace de YouTube:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ GENERAR PISTA"):
    if url:
        with st.spinner("Descargando... (Si tarda más de 1 minuto, intenta con otro link)"):
            try:
                # CONFIGURACIÓN DE EMERGENCIA
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'audio_temp',
                    # Engañamos a YouTube simulando una TV o un celular
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/',
                    'nocheckcertificate': True,
                    'quiet': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                sound = AudioSegment.from_file("audio_temp.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("pista_final.mp3", format="mp3")

                st.balloons()
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_mama.mp3")
                
                os.remove("audio_temp.mp3")
                os.remove("pista_final.mp3")
            except Exception as e:
                st.error("YouTube bloqueó este servidor temporalmente. Prueba con un link de un canal de 'Karaoke' o 'Lyrics' (suelen tener menos protección).")
                st.info("Tip: A veces los videos oficiales (VEVO) son los más protegidos.")
