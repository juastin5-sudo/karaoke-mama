import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎤")

# --- INTERFAZ ---
st.title("🎤 Studio de Pistas VIP")
url = st.text_input("🔗 Enlace de YouTube:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ GENERAR PISTA"):
    if url:
        with st.spinner("Cocinando tu música..."):
            try:
                # CONFIGURACIÓN CON COOKIES
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'audio_temp',
                    'cookiefile': 'youtube.com_cookies.txt', # <--- AQUÍ ESTÁ EL SECRETO
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Procesar audio
                sound = AudioSegment.from_file("audio_temp.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("pista_final.mp3", format="mp3")

                st.balloons()
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="mi_pista.mp3")
                
                os.remove("audio_temp.mp3")
            except Exception as e:
                st.error(f"Error crítico: {e}")




