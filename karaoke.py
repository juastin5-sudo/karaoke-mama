import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎤", layout="centered")

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1 { color: #FF4B4B; text-align: center; }
    .stButton>button { width: 100%; border-radius: 50px; background-color: #FF4B4B; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🎤 STUDIO DE PISTAS VIP</h1>", unsafe_allow_html=True)
st.write("---")

url = st.text_input("🔗 Enlace de YouTube:", placeholder="Pega el link aquí...")
tono = st.select_slider("🎶 Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ ¡CREAR MI PISTA MÁGICA!"):
    if url:
        with st.status("🎼 Procesando...", expanded=True) as status:
            try:
                # --- NUEVA CONFIGURACIÓN ANTIBLOQUEO ---
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'quiet': True,
                    # Este es el truco: forzar a usar IPv4 y un agente de usuario real
                    'source_address': '0.0.0.0', 
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'pista_mama',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📥 Intentando saltar bloqueo de YouTube...")
                    ydl.download([url])

                st.write("🎹 Ajustando el tono...")
                sound = AudioSegment.from_file("pista_mama.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("resultado.mp3", format="mp3")

                status.update(label="✅ ¡Listo!", state="complete")
                st.balloons()
                st.audio("resultado.mp3")
                
                with open("resultado.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista.mp3")
                
                os.remove("pista_mama.mp3")
            except Exception as e:
                st.error(f"YouTube bloqueó el acceso. Intenta con otro link o espera 5 minutos. Error: {e}")



