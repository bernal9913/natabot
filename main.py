import discord
import asyncio

TOKEN = 'MTEwNDMzNzY1NDcxNzM2NjQxMg.GmcLB2.9ivlC3BQYsZ82IXlegPHxyD-Ri8q4cWiAQBU4k'
CHANNEL_ID = 1053910584707514368
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Bot conectado')
    await send_message()  # Llamamos a la función send_message() cuando el bot esté listo

async def send_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        await channel.send(';p')
        await asyncio.sleep(10)  # Espera 10 segundos

client.run(TOKEN)