async def descargar_de_telegram(nombre_cancion):
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    
    async with client.conversation('@DeezerMusicBot') as conv:
        # 1. Enviamos el nombre de la canción
        await conv.send_message(nombre_cancion)
        
        # 2. Esperamos la lista de opciones
        respuesta_lista = await conv.get_response()
        
        # 3. Si el bot nos da opciones (botones), elegimos la primera (el '1')
        # Si el bot no tiene botones y solo manda el audio de una, esto se saltará
        if hasattr(respuesta_lista, 'reply_markup') and respuesta_lista.reply_markup:
            # Enviamos un "1" para elegir la primera opción de la lista
            await conv.send_message("1")
            # Esperamos la respuesta que ya debería ser el audio
            respuesta_audio = await conv.get_response()
        else:
            respuesta_audio = respuesta_lista

        # 4. Descargamos si es un audio
        if respuesta_audio.audio:
            path = await respuesta_audio.download_media(file="pista_original.mp3")
            return path
            
    return None
