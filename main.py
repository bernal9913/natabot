import discord
import asyncio
import lyricsgenius
import random

TOKEN = 'MTEwNDMzNzY1NDcxNzM2NjQxMg.GmcLB2.9ivlC3BQYsZ82IXlegPHxyD-Ri8q4cWiAQBU4k'
#CHANNEL_ID = 1121662573666914326 # server test
CHANNEL_ID = 1055403822266187847
GENIUS_API_TOKEN = 'cOF1DgUx67gTgw5AyzRiQeq_lq6Mlw2iRuLlSEJ0zd7HiBVSSCP3okB4LRv67-G8'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)
genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
songs = [
    {'title': 'Diamantes', 'artist': 'Natanael Cano'},
    {'title': 'PRC', 'artist': 'Peso Pluma & Natanael Cano'},
    {'title': 'Carlitos', 'artist': 'Natanael Cano'},
    {'title': 'Porte exuberante', 'artist': 'Natanael Cano'},
    {'title': 'TQM', 'artist': 'Fuerza Regida'},
    {'title': 'Igualito a mi apa', 'artist': 'Fuerza Regida'},
    {'title': 'Ojos de maniaco ', 'artist': 'Legado 7'},
    {'title': 'Mbappe', 'artist': 'Eladio Carrion'},
    {'title': 'Rosa pastel', 'artist': 'Peso pluma'},
    {'title': 'Soy el unico', 'artist': 'Yahritza y su escencia'}
]

@client.event
async def on_ready():
    print('Bot conectado')
    await send_lyrics()  # Llama a la función send_lyrics() cuando el bot esté listo

async def send_lyrics():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        # Seleccionar una canción aleatoria del arreglo
        song = random.choice(songs)
        title = song['title']
        artist = song['artist']

        # Obtener las letras de la canción deseada usando lyricsgenius
        song_lyrics = genius.search_song(title, artist)
        if song_lyrics is not None:
            lyrics = song_lyrics.lyrics
            print("Ahora suena: " + title)
            await channel.send(lyrics)
        else:
            await channel.send("No se encontraron letras para la canción")

        await asyncio.sleep(60)  # Espera 1 hora (3600 segundos)

client.run(TOKEN)
