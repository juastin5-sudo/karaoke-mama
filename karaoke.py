import audioop_lts
import sys
sys.modules['audioop'] = audioop_lts
import yt_dlp
import os
from pydub import AudioSegment
from static_ffmpeg import add_paths

# Esto activa el motor de audio que instalamos
add_paths()

# --- CONFIGURACIÓN ---
# PEGA EL LINK DE YOUTUBE AQUÍ ABAJO ENTRE LAS COMILLAS
url = 'https://www.youtube.com/watch?v=kj9ptFo-DRc' 
# ELIGE EL TONO: -1 o -2 para bajar, +1 o +2 para subir (0 es original)
cambio_de_tono = -2 
# ---------------------

print("🚀 Empezando proceso...")

# 1. Descargar el audio
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,  
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'cancion_temporal',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print("📥 Descargando desde YouTube...")
    ydl.download([url])

# 2. Procesar el tono
print("🎵 Ajustando el tono de la pista...")
sound = AudioSegment.from_file("cancion_temporal.mp3")

def shift_pitch(audio, semitones):
    new_sample_rate = int(audio.frame_rate * (2.0 ** (semitones / 12.0)))
    return audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio.frame_rate)

pista_modificada = shift_pitch(sound, cambio_de_tono)

# 3. Guardar el resultado final
nombre_final = "pista_para_mama.mp3"
pista_modificada.export(nombre_final, format="mp3")

print(f"✅ ¡LISTO! El archivo se guardó como: {nombre_final}")

# Limpieza: borramos el temporal
if os.path.exists("cancion_temporal.mp3"):

    os.remove("cancion_temporal.mp3")
