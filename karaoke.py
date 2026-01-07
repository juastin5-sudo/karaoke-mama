import streamlit as st
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from pydub import AudioSegment
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
st.markdown("Busca tu canción, ajusta el tono y ¡prepárate para brillar!")

# 3. FUNCIÓN MÁGICA DE TELEGRAM (CON CLIC EN BOTONES)
async def descargar_de_telegram(nombre_cancion):
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    
    try:
        async with client.conversation('@vkmusic_bot', timeout=60) as conv:
            # Enviamos el nombre de la canción
            await conv.send_message(nombre_cancion)
            
            # Esperamos la respuesta (la lista con botones)
            respuesta = await conv.get_response()
            
            # Si el bot envía botones (como el de "1. Canción"), hacemos clic en el primero
            if respuesta.buttons:
                # [0][0] es el primer botón de la primera fila
                await respuesta.click(0, 0)
                
                # Esperamos el archivo de audio que el bot envía tras el clic
                audio_msg = await conv.get_response()
                
                if audio_msg.audio:
                    path = await audio_msg.download_media(file="pista_original.mp3")
                    return path
            else:
                # Si el bot no tiene botones y manda el audio directo
                if respuesta.audio:
                    return await respuesta.download_media(file="pista_original.mp3")
                    
    except Exception as e:
        st.error(f"Hubo un problema con el bot: {e}")
    finally:
        await client.disconnect()
    return None

# 4. INTERFAZ DE USUARIO
busqueda = st.text_input("🎵 ¿Qué canción quieres cantar hoy?", placeholder="Ej: Rocio Durcal - Costumbres")
tono = st.slider("✨ Ajustar tono (Bajar o Subir):", -5, 5, -2)

if st.button("🚀 PREPARAR PISTA"):
    if busqueda:
        with st.status("🎼 Buscando y ajustando tono... ten paciencia", expanded=True) as status:
            # Ejecutamos la parte de Telegram
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            archivo = loop.run_until_complete(descargar_de_telegram(busqueda))
            
            if archivo:
                status.write("🎸 Pista encontrada. Ajustando el tono...")
                
                # PROCESAMIENTO DE AUDIO (CAMBIO DE TONO)
                audio = AudioSegment.from_file(archivo)
                nuevo_sample_rate = int(audio.frame_rate * (2.0 ** (tono / 12.0)))
                pista_final = audio._spawn(audio.raw_data, overrides={'frame_rate': nuevo_sample_rate}).set_frame_rate(audio.frame_rate)
                
                nombre_final = "pista_lista.mp3"
                pista_final.export(nombre_final, format="mp3")
                
                status.update(label="✅ ¡Tu pista está lista!", state="complete")
                
                # REPRODUCTOR Y BOTÓN DE DESCARGA
                st.audio(nombre_final)
                with open(nombre_final, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar MP3",
                        data=f,
                        file_name=f"karaoke_{busqueda}.mp3",
                        mime="audio/mp3"
                    )
                # Limpiar archivos temporales
                if os.path.exists(archivo): os.remove(archivo)
            else:
                status.update(label="❌ No se pudo obtener la pista", state="error")
                st.error("No se encontró la canción o el bot tardó mucho. ¡Intenta de nuevo!")
    else:
        st.warning("Escribe el nombre de una canción primero.")
