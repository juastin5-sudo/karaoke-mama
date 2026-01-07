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
        st.error(f"Error de conexión: {e}")
    finally:
        await client.disconnect()
    return None

# --- Interfaz de Usuario ---
busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Dalila - Otra ocupa mi lugar")
col1, col2 = st.columns(2)
with col1:
    tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, 0)
with col2:
    quitar_voz = st.checkbox("✂️ ELIMINAR VOZ DEL ARTISTA", value=False)

if st.button("🚀
