import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎤", layout="centered")

# --- DISEÑO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        background-color: #FF4B4B;
        color: white;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff6666;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---
st.markdown("<h1>🎤 STUDIO DE PISTAS VIP</h1>", unsafe_allow_html=True)
st.write("---")

# Organización en columnas
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("🔗 Enlace de YouTube:", placeholder="Pega el link aquí...")

with col2:
    tono = st.select_slider("🎶 Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

st.write("") 

if st.button("✨ ¡CREAR MI PISTA MÁGICA!"):
    if url:
        with st.status("🎼 Trabajando en tu música...", expanded=True) as status:
            try:
                # 1. Descarga
                st.write("📥 Obteniendo canción de YouTube...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'nocheckcertificate': True,
'quiet': True,
'no_warnings': True,
'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'cancion_mama',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 2. Cambio de tono
                st.write("🎹 Ajustando el tono perfecto...")
                sound = AudioSegment.from_file("cancion_mama.mp3")
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                
                # 3. Exportar
                pista.export("pista_final.mp3", format="mp3")
                status.update(label="✅ ¡Tu pista está lista!", state="complete", expanded=False)
                
                # Celebración
                st.balloons()
                
                # Resultado
                st.success("¡Disfruta tu canción!")
                st.audio("pista_final.mp3")
                
                with open("pista_final.mp3", "rb") as file:
                    st.download_button(
                        label="⬇️ DESCARGAR MP3",
                        data=file,
                        file_name="pista_karaoke_mama.mp3",
                        mime="audio/mp3"
                    )
                
                # Limpiar archivos temporales
                os.remove("cancion_mama.mp3")
                os.remove("pista_final.mp3")

            except Exception as e:
                st.error(f"Hubo un pequeño problema: {e}")
    else:
        st.warning("⚠️ Olvidaste poner el link de la canción.")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: gray;'>Hecho con amor por su hijo favorito</p>", unsafe_allow_html=True)


