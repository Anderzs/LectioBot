import os

import discord
from lectio_handler import LectioHandler
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()

KALENDER = [
    "Mandag",
    "Tirsdag",
    "Onsdag",
    "Torsdag",
    "Fredag",
    "Lørdag",
    "Søndag"
]

TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot("!", intents=discord.Intents.all())

lectio = LectioHandler(
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    skoleID=os.getenv("SKOLEID")
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Lectio"))

    for guild in bot.guilds:
        if not await skema_channel_exists(guild):
            await guild.create_text_channel(name="skema")
            print("")

    """
    await bot.get_channel(1148524567611048029).purge(limit=10)

    await send_status()
    await clear_channel(bot.get_channel(1148522781324083261).id)
    await bot.get_channel(1148522781324083261).send(
        f"**🔥🔥 Her kommer skemaet for uge 36 🔥🔥**"
    )
    for i in range(1, 6):
        await send_skema(i, 36, 2023)
        """

@bot.command(name="skema")
async def skema_command(ctx, dag, uge):    
    await send_skema(int(dag), int(uge), 2023, channel=ctx)
    
async def skema_channel_exists(guild: discord.Guild) -> bool:
    #print(guild.text_channels)
    return "skema" in [channel.name for channel in guild.text_channels]

async def send_status():
    status_channel = bot.get_channel(1148524567611048029)
    success_color = 0x59ff00
    await send_embed({
        "title": "Status - **Online**",
        "url": "",
        "channel": status_channel,
        "description": "Bot is up and running!",
        "fields": {
            "Skemalægger": {
                "value": "Skemalæggeren kommer snart!",
                "inline": False
            }
        },
        "color": success_color,
        "footer": f"Sidst opdateret: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
})
    
async def clear_channel(channel_id: int):
    await bot.get_channel(channel_id).purge(limit=100)

async def send_skema(dag: int, uge: int, år: int, channel = None):
    skema = lectio.få_skema_for_dag(dag, uge, år)
    skema_channel = bot.get_channel(1148522781324083261)
    await send_embed({
        "title": f"**{KALENDER[dag-1]} uge {uge}**",
        "url": f"https://www.lectio.dk/lectio/{lectio.client.skoleId}/SkemaNy.aspx?week={uge}{år}",
        "channel": skema_channel if not channel else channel,
        "description": f"Her kan du se skemaet for **{KALENDER[dag-1]}** uge **{uge}** år **{år}**",
        "fields": {
            f"{i}": {
                "value": f"{skema[i]}",
                "inline": True
            } for i in skema
        },
        "color": 0x59ff00,
        "footer": f"Sidst opdateret: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
    })


async def send_embed(embed_details: dict):
    embed=discord.Embed(title=embed_details["title"], url=embed_details['url'], description=embed_details['description'], color=embed_details['color'])
    #embed.set_thumbnail(url=bot.user.avatar)
    for field in embed_details["fields"]:
        value = embed_details["fields"][field]["value"]
        inline = embed_details["fields"][field]["inline"]

        embed.add_field(name=field, value=value, inline=inline)
    
    embed.set_footer(text=embed_details['footer'])
    await embed_details['channel'].send(embed=embed)


bot.run(TOKEN)
