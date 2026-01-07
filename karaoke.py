import streamlit as st
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

st.set_page_config(page_title="El Studio de Mamá", page_icon="🎤")

# Cargar llaves
try:
    API_ID = st.secrets["TELEGRAM_API_ID"]
    API_HASH = st.secrets["TELEGRAM_API_HASH"]
    SESSION = st.secrets["TELEGRAM_SESSION"]
except:
    st.error("⚠️ Error: Faltan las llaves en Secrets.")
    st.stop()

st.title("🎤 El Studio de Mamá")

async def descargar_de_telegram(nombre_cancion):
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    try:
        async with client.conversation('@vkmusic_bot', timeout=60) as conv:
            await conv.send_message(nombre_cancion)
            respuesta = await conv.get_response()
            if hasattr(respuesta, 'buttons') and respuesta.buttons:
                await respuesta.click(0, 0)
                audio_msg = await conv.get_response()
                if audio_msg.audio:
                    return await audio_msg.download_media(file="temp_audio.mp3")
            elif hasattr(respuesta, 'audio') and respuesta.audio:
                return await respuesta.download_media(file="temp_audio.mp3")
    except Exception as e:
        st.error(f"Error con el bot: {e}")
    finally:
        await client.disconnect()
    return None

busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Rocio Durcal - Costumbres")
tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, 0)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.status("🎼 Procesando...", expanded=True) as status:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            archivo_original = loop.run_until_complete(descargar_de_telegram(busqueda))
            
            if archivo_original:
                nombre_final = "pista_pro.mp3"
                centisimos = tono * 100
                
               if archivo_original:
                nombre_limpio = "audio_estandar.wav"
                nombre_final = "pista_pro.mp3"
                centisimos = tono * 100
                
                if tono == 0:
                    status.write("🎸 Preparando audio original...")
                    os.rename(archivo_original, nombre_final)
                    resultado = 0
                else:
                    status.write("🎸 Limpiando formato y ajustando tono...")
                    
                    # PASO 1: FFmpeg convierte CUALQUIER cosa a un WAV estándar que SoX entienda perfecto
                    os.system(f'ffmpeg -i "{archivo_original}" -ar 441

                if resultado == 0 and os.path.exists(nombre_final):
                    status.update(label="💖 ¡Lista para cantar!", state="complete")
                    st.audio(nombre_final)
                    with open(nombre_final, "rb") as f:
                        st.download_button("⬇️ Descargar MP3", f, file_name=f"karaoke_{busqueda}.mp3")
                else:
                    st.error("Error al procesar el audio.")
                
                if os.path.exists(archivo_original): os.remove(archivo_original)

