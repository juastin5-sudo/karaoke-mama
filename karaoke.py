import streamlit as st
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from pydub import AudioSegment
import os

# Sacamos las llaves del "Cajón de Secretos"
API_ID = st.secrets["TELEGRAM_API_ID"]
API_HASH = st.secrets["TELEGRAM_API_HASH"]
SESSION = st.secrets["TELEGRAM_SESSION"]

st.set_page_config(page_title="El Studio de Mamá", page_icon="🎤")
st.title("🎤 El Studio de Mamá")
st.markdown("Busca tu canción, ajusta el tono y ¡a cantar!")

async def descargar_de_telegram(nombre_cancion):
    # Iniciamos el cliente usando la Llave Maestra
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    
    # Buscamos al bot de música
    async with client.conversation('@DeezerMusicBot') as conv:
        await conv.send_message(nombre_cancion)
        respuesta = await conv.get_response()
        if respuesta.audio:
            path = await respuesta.download_media(file="pista_original.mp3")
            return path
    return None

busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Juan Gabriel - Abrázame muy fuerte")
tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, -2)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.spinner("Buscando y preparando... esto tarda unos segundos."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            archivo = loop.run_until_complete(descargar_de_telegram(busqueda))
            
            if archivo:
                # Procesamos el audio
                audio = AudioSegment.from_file(archivo)
                nuevo_sample_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista_final = audio._spawn(audio.raw_data, overrides={'frame_rate': nuevo_sample_rate}).set_frame_rate(audio.frame_rate)
                pista_final.export("pista_lista.mp3", format="mp3")
                
                st.success("¡Aquí tienes tu pista!")
                st.audio("pista_lista.mp3")
                with open("pista_lista.mp3", "rb") as f:
                    st.download_button("⬇️ Descargar MP3", f, file_name=f"pista_{busqueda}.mp3")
            else:
                st.error("No pude encontrar esa canción. Intenta con otro nombre.")

