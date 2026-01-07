import streamlit as st
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="El Studio de Mamá", page_icon="🎤")

# 2. CARGAR LLAVES DESDE LOS SECRETS
try:
    API_ID = st.secrets["TELEGRAM_API_ID"]
    API_HASH = st.secrets["TELEGRAM_API_HASH"]
    SESSION = st.secrets["TELEGRAM_SESSION"]
except Exception as e:
    st.error("⚠️ Error: No se encontraron las llaves en los Secrets de Streamlit.")
    st.stop()

st.title("🎤 El Studio de Mamá")
st.markdown("Busca tu canción, ajusta el tono y ¡prepárate para cantar!")

# 3. FUNCIÓN DE TELEGRAM (CON CLIC EN BOTONES)
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
                    # Guardamos con un nombre base
                    path = await audio_msg.download_media(file="temp_audio.mp3")
                    return path
            elif hasattr(respuesta, 'audio') and respuesta.audio:
                return await respuesta.download_media(file="temp_audio.mp3")
                    
    except Exception as e:
        st.error(f"Hubo un problema con el bot: {e}")
    finally:
        await client.disconnect()
    return None

# 4. INTERFAZ DE USUARIO
busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Rocio Durcal - Costumbres")
tono = st.slider("✨ Ajustar tono (Semitonos):", -5, 5, -2)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.status("🎼 Procesando pista profesional...", expanded=True) as status:
            # Ejecutamos la descarga
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            archivo_original = loop.run_until_complete(descargar_de_telegram(busqueda))
            
            if archivo_original:
                status.write("🎸 Ajustando tono sin cambiar la velocidad...")
                
                # Definimos rutas absolutas para evitar errores en el servidor
                cwd = os.getcwd()
                ruta_entrada = os.path.join(cwd, archivo_original)
                nombre_final = "pista_pro.mp3"
                ruta_salida = os.path.join(cwd, nombre_final)
                
                # SoX usa "cents" (100 cents = 1 semitono)
                centisimos = tono * 100
                
                # COMANDO DE SOX: cambia el pitch sin cambiar el tiempo
                comando = f'sox "{ruta_entrada}" "{ruta_salida}" pitch {centisimos}'
                resultado = os.system(comando)
                
                if resultado == 0 and os.path.exists(ruta_salida):
                    status.update(label="💖 ¡Tu pista está lista, Reina! A brillar.", state="complete")
                    
                    # REPRODUCTOR Y BOTÓN
                    st.audio(nombre_final)
                    with open(nombre_final, "rb") as f:
                        st.download_button(
                            label="⬇️ Descargar MP3",
                            data=f,
                            file_name=f"karaoke_{busqueda}.mp3",
                            mime="audio/mp3"
                        )
                    
                    # Limpieza de archivos temporales
                    if os.path.exists(ruta_entrada): os.remove(ruta_entrada)
                else:
                    status.update(label="❌ Error en el motor de audio", state="error")
                    st
