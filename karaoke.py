import streamlit as st
import requests
import os
from pydub import AudioSegment
import time

st.set_page_config(page_title="Karaoke VIP para Mamá", page_icon="🎤")
st.title("🎤 El Studio de Mamá")

url_video = st.text_input("🔗 Pega el link de YouTube aquí:")
tono = st.select_slider("🎶 Ajustar Tono:", options=[-4, -3, -2, -1, 0, 1, 2], value=-2)

if st.button("✨ GENERAR PISTA COMPLETA"):
    if url_video:
        with st.status("🚀 Usando puente de alta velocidad...", expanded=True) as status:
            try:
                # 1. Llamamos al puente de Cobalt (servidor externo)
                st.write("🛰️ Pidiendo permiso al puente...")
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                data = {
                    "url": url_video,
                    "downloadMode": "audio",
                    "audioFormat": "mp3",
                    "audioBitrate": "128"
                }
                
                # Usamos una instancia pública de Cobalt
                response = requests.post("https://api.cobalt.tools/api/json", json=data, headers=headers)
                res_data = response.json()
                
                if res_data.get("status") == "picker" or res_data.get("status") == "redirect" or res_data.get("status") == "stream":
                    audio_url = res_data.get("url")
                    
                    # 2. Descargamos el archivo que el puente nos da
                    st.write("📥 Descargando canción completa...")
                    audio_res = requests.get(audio_url)
                    with open("temp.mp3", "wb") as f:
                        f.write(audio_res.content)
                    
                    # 3. Procesamos con Pydub (cambio de tono)
                    st.write("🎹 Ajustando el tono profesionalmente...")
                    sound = AudioSegment.from_file("temp.mp3")
                    new_rate = int(sound.frame_rate * (2.0 ** (tono / 12.0)))
                    pista = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(sound.frame_rate)
                    pista.export("final.mp3", format="mp3")
                    
                    status.update(label="✅ ¡Listo!", state="complete")
                    st.balloons()
                    st.audio("final.mp3")
                    with open("final.mp3", "rb") as f:
                        st.download_button("⬇️ DESCARGAR MP3", f, file_name="pista_karaoke.mp3")
                else:
                    st.error("El puente está saturado. Intenta de nuevo en un momento.")
            except Exception as e:
                st.error(f"Error en el puente: {e}")
    else:
        st.warning("Pega un link primero.")
