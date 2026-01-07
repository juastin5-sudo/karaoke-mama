import streamlit as st
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from pydub import AudioSegment
import os
import time

# Configuración de página
st.set_page_config(page_title="El Studio de Mamá", page_icon="🎤")

# Cargar secretos
try:
    API_ID = st.secrets["TELEGRAM_API_ID"]
    API_HASH = st.secrets["TELEGRAM_API_HASH"]
    SESSION = st.secrets["TELEGRAM_SESSION"]
except:
    st.error("Faltan las llaves en los Secrets de Streamlit.")
    st.stop()

st.title("🎤 El Studio de Mamá")

async def descargar_de_telegram(nombre_cancion):
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    
    try:
        # Cambiamos al nuevo bot
        async with client.conversation('@vkmusic_bot', timeout=40) as conv:
            # 1. Enviamos la canción
            await conv.send_message(nombre_cancion)
            
            # 2. El bot responderá con una lista de canciones
            respuesta = await conv.get_response()
            
            # 3. Enviamos "1" para elegir el primer resultado de la lista
            await conv.send_message("1")
            
            # 4. Esperamos el audio (le damos 20 seg por si el bot está lento)
            audio_msg = await conv.get_response()
            
            if audio_msg.audio:
                path = await audio_msg.download_media(file="pista_original.mp3")
                return path
    except Exception as e:
        st.error(f"El bot no respondió: {e}")
    finally:
        await client.disconnect()
    return None

busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Juan Gabriel - Abrázame muy fuerte")
tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, -2)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.status("🎼 Procesando... esto puede tardar un minuto", expanded=True) as status:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            archivo = loop.run_until_complete(descargar_de_telegram(busqueda))
            
            if archivo:
                status.write("🎸 Ajustando el tono para tu voz...")
                audio = AudioSegment.from_file(archivo)
                nuevo_sample_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista_final = audio._spawn(audio.raw_data, overrides={'frame_rate': nuevo_sample_rate}).set_frame_rate(audio.frame_rate)
                pista_final.export("pista_lista.mp3", format="mp3")
                
                status.update(label="✅ ¡Lista para cantar!", state="complete")
                st.audio("pista_lista.mp3")
                with open("pista_lista.mp3", "rb") as f:
                    st.download_button("⬇️ Descargar MP3", f, file_name=f"karaoke_{busqueda}.mp3")
            else:
                status.update(label="❌ No se encontró la canción", state="error")
                st.error("El bot no respondió a tiempo o no encontró resultados.")

