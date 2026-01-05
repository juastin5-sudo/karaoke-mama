import streamlit as st
import yt_dlp
import os
import subprocess

st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")
st.title("🎤 El Studio de Mamá")
st.write("Solo pega el link y yo preparo tu pista.")

url = st.text_input("🔗 Enlace de YouTube:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ ¡CREAR PISTA!"):
    if url:
        with st.spinner("Cocinando tu música..."):
            try:
                # 1. Descarga limpia
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'temp_audio.%(ext)s',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 2. Cambio de tono usando FFmpeg directo (sin pydub)
                # El valor de 'atempo' ajusta la velocidad, pero usaremos 'rubberband' si está o 'asetrate'
                semitono = 2.0 ** (tono / 12.0)
                rate = 44100
                new_rate = int(rate * semitono)
                
                cmd = f"ffmpeg -i temp_audio.mp3 -af \"asetrate={new_rate},aresample={rate}\" -y pista_final.mp3"
                subprocess.run(cmd, shell=True)

                # 3. Mostrar resultado
                st.balloons()
                st.audio("pista_final.mp3")
                with open("pista_final.mp3", "rb") as f:
                    st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_mama.mp3")
                
                # Limpiar
                if os.path.exists("temp_audio.mp3"): os.remove("temp_audio.mp3")
            except Exception as e:
                st.error(f"Error: {e}")
