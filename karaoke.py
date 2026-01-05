import audioop_lts
import sys
sys.modules['audioop'] = audioop_lts

import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎤")
st.title("🎤 El Studio de Mamá")

url = st.text_input("🔗 Enlace de YouTube:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ GENERAR PISTA"):
    if url:
        with st.spinner("Procesando..."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'pista_mama',
                    'nocheckcertificate': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                sound = AudioSegment.from_file("pista_mama.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("final.mp3", format="mp3")

                st.audio("final.mp3")
                with open("final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR", f, file_name="pista.mp3")
                
                os.remove("pista_mama.mp3")
            except Exception as e:
                st.error(f"Error: {e}")
