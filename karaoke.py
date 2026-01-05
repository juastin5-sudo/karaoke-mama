import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

st.set_page_config(page_title="Karaoke Studio VIP", page_icon="🎤")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎤 Studio Mágico de Mamá")
st.write("Escribe el nombre de la canción. Ahora usamos un motor de búsqueda más libre.")

busqueda = st.text_input("🔍 ¿Qué canción quieres hoy?", placeholder="Ej: Amor Eterno Rocio Durcal")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ PREPARAR MI PISTA"):
    if busqueda:
        with st.status("🚀 Buscando en la red de música libre...", expanded=True) as status:
            try:
                # CAMBIAMOS EL MOTOR A SOUNDCLOUD (scsearch)
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'pista_temporal',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'default_search': 'scsearch', # <--- AQUÍ ESTÁ EL CAMBIO
                    'nocheckcertificate': True,
                    'quiet': True,
                }

                # Buscamos solo el primer resultado para que sea rápido
                query = f"scsearch1:{busqueda}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Descargando archivo desde SoundCloud...")
                    ydl.download([query])

                st.write("🎹 Ajustando el tono perfecto...")
                audio = AudioSegment.from_file("pista_temporal.mp3")
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
                st.error("El servidor de música está saturado. Prueba escribiendo el nombre de forma diferente.")
                st.info(f"Nota técnica: {e}")
