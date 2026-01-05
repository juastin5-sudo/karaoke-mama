import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; width: 100%; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎤 El Studio de Mamá")
st.write("Pega el link y yo hago el resto.")

url = st.text_input("🔗 Link de la canción:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ ¡GENERAR PISTA!"):
    if url:
        with st.spinner("Saltando bloqueos y preparando audio..."):
            try:
                # REGLAS PARA ENGAÑAR A YOUTUBE
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'cancion_mama',
                    'cookiefile': 'youtube.com_cookies.txt', # <--- USA TUS LLAVES
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Procesar audio
                sound = AudioSegment.from_file("cancion_mama.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("pista_final.mp3", format="mp3")

                st.balloons()
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="tu_pista.mp3")
                
                os.remove("cancion_mama.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error(f"Hubo un error: {e}")
                st.info("Tip: Asegúrate de que el archivo cookies.txt esté en GitHub.")
