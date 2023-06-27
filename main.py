import discord
import asyncio
import lyricsgenius
import random
import spotipy
from discord_interactions import InteractionsClient
from discord_slash import SlashCommand


# making the token isolation from the main file
from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    GENIUS_ACCESS_TOKEN,
    DISCORD_TOKEN,
    CHANNEL_ID_LP,
    CHANNEL_ID_PS,
    CHANNEL_ID_VC
)
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

bot = discord.Client(intents=discord.Intents.default())
client = InteractionsClient(bot, token=DISCORD_TOKEN)


running = """
⠄⠄⣿⣿⣿⣿⠘⡿⢛⣿⣿⣿⣿⣿⣧⢻⣿⣿⠃⠸⣿⣿⣿⠄⠄⠄⠄⠄
⠄⠄⣿⣿⣿⣿⢀⠼⣛⣛⣭⢭⣟⣛⣛⣛⠿⠿⢆⡠⢿⣿⣿⠄⠄⠄⠄⠄
⠄⠄⠸⣿⣿⢣⢶⣟⣿⣖⣿⣷⣻⣮⡿⣽⣿⣻⣖⣶⣤⣭⡉⠄⠄⠄⠄⠄
⠄⠄⠄⢹⠣⣛⣣⣭⣭⣭⣁⡛⠻⢽⣿⣿⣿⣿⢻⣿⣿⣿⣽⡧⡄⠄⠄⠄
⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⡛⢿⣽⢘⣿⣷⣿⡻⠏⣛⣀⠄⠄
⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⡅⣿⠚⣡⣴⣿⣿⣿⡆⠄
⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣱⣾⣿⣿⣿⣿⣿⣿⠄
⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠄
⠄ ⣿⣿⣿ terrible, sushon?⣿⣿⣿⣿⣿⣿⠄
⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⠿⣿⣿⣿⣿⠄
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠄
"""
# deprecated songs
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

@client.command(
    name="pon",
    description="Reproducir canción y mostrar letra",
    options=[
        {
            "name": "cancion",
            "description": "Nombre de la canción",
            "type": 3,  # String type
            "required": True
        }
    ]
)

@bot.event
async def on_ready():
    print('Bot conectado')
    print(running)


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
async def play_song(ctx, cancion):
    track_uri = get_spotify_track_uri(cancion)

    if track_uri is not None:
        channel = ctx.author.voice.channel
        if channel:
            voice_channel = await channel.connect()
            await ctx.send("Reproduciendo la canción en el canal de voz...")
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=spotify.track_audio_analysis(track_uri)))

            while voice_channel.is_playing():
                await asyncio.sleep(1)

            await voice_channel.disconnect()
            await ctx.send("Canción finalizada")
            await ctx.send("Obteniendo la letra de la canción...")
            lyrics = get_song_lyrics(cancion)
            await ctx.send("Letra de la canción:\n" + lyrics)
        else:
            await ctx.send("Debes estar en un canal de voz para utilizar este comando.")
    else:
        await ctx.send("No se encontró la canción en Spotify")

def get_spotify_track_uri(song_name):
    search_results = spotify.search(q=song_name, type='track', limit=1)

    if search_results['tracks']['items']:
        track_uri = search_results['tracks']['items'][0]['uri']
        return track_uri
    else:
        return None

def get_song_lyrics(song_name):
    song = genius.search_song(song_name)
    if song is not None:
        return song.lyrics
    else:
        return "No se encontraron letras para esta canción"

bot.run(DISCORD_TOKEN)