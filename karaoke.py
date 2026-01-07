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

# --- Interfaz ---
busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Dalila - Otra ocupa mi lugar")
col1, col2 = st.columns(2)
with col1:
    tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, 0)
with col2:
    quitar_voz = st.checkbox("✂️ ELIMINAR VOZ DEL ARTISTA", value=False)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.status("🎼 Trabajando en la música...", expanded=True) as status:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            archivo_original = loop.run_until_complete(descargar_de_telegram(busqueda))
            
            if archivo_original:
                nombre_limpio = "audio_estandar.wav"
                nombre_final = "pista_pro.mp3"
                
                status.write("🎸 Estabilizando audio...")
                # Convertimos a WAV estéreo
                os.system(f'ffmpeg -i "{archivo_original}" -ar 44100 -ac 2 "{nombre_limpio}" -y')
                
                if quitar_voz:
                    status.write("🧠 Eliminando voz del artista...")
                    # Filtro simplificado: 
                    # 1. 'pan' para restar canales (quita voz central)
                    # 2. 'equalizer' simple para recuperar bajos (sin usar c0/c1)
                    # 3. 'rubberband' para el tono
                    factor_pitch = 2**(tono/12)
                    filtro_audio = (
                        f"pan=stereo|c0=c0-c1|c1=c1-c0,"
                        f"equalizer=f=100:width_type=h:width=200:g=10,"
                        f"rubberband=pitch={factor_pitch}"
                    )
                    comando = f'ffmpeg -i "{nombre_limpio}" -af "{filtro_audio}" "{nombre_final}" -y'
                else:
                    status.write("✨ Ajustando tono...")
                    centisimos = tono * 100
                    comando = f'sox "{nombre_limpio}" -t mp3 "{nombre_final}" pitch {centisimos}'
                
                resultado = os.system(comando)
                
                if resultado == 0 and os.path.exists(nombre_final):
                    status.update(label="💖 ¡Lista para cantar!", state="complete")
                    st.audio(nombre_final)
                    with open(nombre_final, "rb") as f:
                        st.download_button("⬇️ Descargar MP3", f, file_name=f"karaoke_{busqueda}.mp3")
                else:
                    st.error("Hubo un problema técnico al procesar el audio.")
                
                # Limpieza
                if os.path.exists(nombre_limpio): os.remove(nombre_limpio)
                if os.path.exists(archivo_original): os.remove(archivo_original)
            else:
                st.error("No se pudo obtener la canción.")
