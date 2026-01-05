import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

# Intentar importar audioop (para versiones viejas) o ignorarlo (para nuevas)
try:
    import audioop
except ImportError:
    st.warning("Nota: Usando motor de audio alternativo.")

st.set_page_config(page_title="Karaoke de Mamá", page_icon="🎤")
st.title("🎤 Studio de Pistas para Mamá")

url = st.text_input("Enlace de YouTube:", placeholder="https://www.youtube.com/watch?v=...")
tono = st.select_slider("Ajustar tono (semitonos):", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ Generar Pista"):
    if url:
        with st.spinner("Procesando..."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    'outtmpl': 'temp_audio',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                sound = AudioSegment.from_file("temp_audio.mp3")
                # Método compatible para cambiar tono
                new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                pista.export("pista_lista.mp3", format="mp3")

                with open("pista_lista.mp3", "rb") as file:
                    st.audio(file.read(), format="audio/mp3")
                    st.download_button(label="⬇️ DESCARGAR", data=file, file_name="pista.mp3")
                
                os.remove("temp_audio.mp3")
                os.remove("pista_lista.mp3")
            except Exception as e:
                st.error(f"Error: {e}")

