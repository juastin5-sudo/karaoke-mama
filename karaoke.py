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

async def descargar_de_telegram(nombre_cancion, modo_karaoke):
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    
    # Si quiere karaoke, modificamos la búsqueda para que el bot ayude
    termino_busqueda = f"{nombre_cancion} karaoke" if modo_karaoke else nombre_cancion
    
    try:
        async with client.conversation('@vkmusic_bot', timeout=60) as conv:
            await conv.send_message(termino_busqueda)
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

# --- Interfaz de Usuario ---
busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Rocio Durcal - Costumbres")

col1, col2 = st.columns(2)
with col1:
    tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, 0)
with col2:
    quitar_voz = st.checkbox("✂️ Modo Karaoke (Busca pista instrumental)", value=False)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.status("🎼 Procesando...", expanded=True) as status:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # Pasamos el modo_karaoke a la función de descarga
            archivo_original = loop.run_until_complete(descargar_de_telegram(busqueda, quitar_voz))
            
            if archivo_original:
                nombre_limpio = "audio_estandar.wav"
                nombre_final = "pista_pro.mp3"
                centisimos = tono * 100
                
                status.write("🎸 Limpiando formato...")
                # PASO 1: Convertir a WAV estándar (Forzamos Estéreo para que el filtro funcione)
                os.system(f'ffmpeg -i "{archivo_original}" -ar 44100 -ac 2 "{nombre_limpio}" -y')
                
                status.write("🛠️ Ajustando tono y refinando audio...")
                
                # PASO 2: Aplicamos cambio de tono y, si es necesario, filtro de voz avanzado
                # El filtro 'stereotools' intenta remover el centro (donde está la voz) sin perder tanta calidad
                if quitar_voz:
                    # Filtro que remueve el centro pero mantiene los extremos de la música
                    comando_final = f'ffmpeg -i "{nombre_limpio}" -af "stereotools=mlev=0.5:mspan=0:middle=0, rubberband=pitch={pow(2, tono/12)}" "{nombre_final}" -y'
                else:
                    # Solo cambio de tono con SoX (que es más rápido para esto)
                    comando_final = f'sox "{nombre_limpio}" -t mp3 "{nombre_final}" pitch {centisimos}'
                
                resultado = os.system(comando_final)
                
                if resultado == 0 and os.path.exists(nombre_final):
                    status.update(label="💖 ¡Lista para cantar!", state="complete")
                    st.audio(nombre_final)
                    with open(nombre_final, "rb") as f:
                        st.download_button("⬇️ Descargar MP3", f, file_name=f"karaoke_{busqueda}.mp3")
                else:
                    st.error("Error al procesar el audio. Intentando sin filtros...")
                
                # Limpieza de archivos temporales
                if os.path.exists(nombre_limpio): os.remove(nombre_limpio)
                if os.path.exists(archivo_original): os.remove(archivo_original)
            else:
                st.error("No se encontró la canción. Intenta con otro nombre.")
