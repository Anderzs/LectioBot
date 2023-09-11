import os

import discord
from lectio_handler import LectioHandler
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.commands import Bot
from logger import LogHandler, LogLevel

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

class LectioBot(Bot):
    def __init__(self, command_prefix = "!") -> None:
        Bot.__init__(self, command_prefix=command_prefix,intents=discord.Intents.all())
        # Bot
        self.logger = LogHandler()
        self.skema_id = {}
        # Lectio
        self.lectio = LectioHandler(
            username=os.getenv("LECTIO_USERNAME"),
            password=os.getenv("LECTIO_PASSWORD"),
            skoleID=os.getenv("LECTIO_SKOLEID")
        )

        self.add_commands()
    
    async def on_ready(self):
        self.logger.log(LogLevel.SUCCES, f'{self.user} er forbundet til Discord!')
        self.today = datetime.today().isocalendar()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Lectio"))

        for guild in self.guilds:
            if not await self.skema_channel_exists(guild):
                self.logger.log(LogLevel.INFO, f"Opretter skema kanal i guild: {guild}")
                channel = await guild.create_text_channel(name="skema")
                self.skema_id[guild.name] = channel.id
            else:
                self.skema_id[guild.name] = discord.utils.get(guild.channels, name="skema").id
            
            self.logger.log(LogLevel.SUCCES, f"Fandt skemaID for guild: {guild}")
            await self.send_weekly_schedule(guild, self.today[1], self.today[0])
        
        #await bot.get_channel(1148524567611048029).purge(limit=10)
        #await clear_channel(bot.get_channel(1148522781324083261).id)

    async def send_weekly_schedule(self, guild, week: int, year: int) -> None:
        await self.clear_channel(self.skema_id[guild.name])
        await self.get_channel(self.skema_id[guild.name]).send(
            f"**🔥🔥 Her kommer skemaet for uge 37 🔥🔥**"
        )

        for i in range(1, 6):
            await self.send_skema(guild, i, week, year)

    def launch(self) -> None:
        self.logger.log(LogLevel.INFO, "Starter LectioBot...")
        self.run(TOKEN)

    def add_commands(self):
        @self.command(name="skema")
        async def skema_command(ctx, dag, uge):    
            await self.send_skema(ctx.guild, int(dag), int(uge), 2023, channel=ctx)

    
    async def skema_channel_exists(self, guild: discord.Guild) -> bool:
        return "skema" in [channel.name for channel in guild.text_channels]

    async def send_status(self):
            status_channel = self.get_channel(self.skema_id)
            success_color = 0x59ff00
            await self.send_embed({
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
    
    
    async def clear_channel(self, channel_id: int):
        await self.get_channel(channel_id).purge(limit=100)

    async def send_skema(self, guild, dag: int, uge: int, år: int, channel = None):
        skema = self.lectio.få_skema_for_dag(dag, uge, år)
        skema_channel = self.get_channel(self.skema_id[guild.name])
        await self.send_embed({
            "title": f"**{KALENDER[dag-1]} uge {uge}**",
            "url": f"https://www.lectio.dk/lectio/{self.lectio.client.skoleId}/SkemaNy.aspx?week={uge}{år}",
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


    async def send_embed(self, embed_details: dict):
        embed=discord.Embed(title=embed_details["title"], url=embed_details['url'], description=embed_details['description'], color=embed_details['color'])
        #embed.set_thumbnail(url=bot.user.avatar)
        for field in embed_details["fields"]:
            value = embed_details["fields"][field]["value"]
            inline = embed_details["fields"][field]["inline"]

            embed.add_field(name=field, value=value, inline=inline)
        
        embed.set_footer(text=embed_details['footer'])
        await embed_details['channel'].send(embed=embed)


if __name__ == "__main__":
    lectio_bot = LectioBot()
    lectio_bot.launch()
