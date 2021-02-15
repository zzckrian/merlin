from datetime import datetime
from glob import glob
from discord import Intents
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.triggers.cron import CronTrigger
from ..db import db

PREFIX = "2"
OWNER_IDS = [503052622438334485]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded yh")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup..")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        print("Running bot")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        self.stdout.channel.send("Rules: bebas anjing")

    async def on_connect(self):
        print("Ngontol")

    async def on_disconnect(self):
        print('awakoawk crash')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        else:
            self.stdout.send("Akwokwaokaw error mampus.")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Ngomong nn tuh")

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(776108158891982889)
            self.stdout = self.get_channel(808223116126846986)
            self.scheduler.start()
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            print("bot ready")

            await self.stdout.send("bot jalan")

        #            embed = Embed(title="DEATH NOTE", description="11/02/21", color=0xff0963, timestamp=datetime.utcnow())
        #            field = [("TOGI DI BAN", "REASON : MUKA LO PG", False),
        #                     ("CLIENT.ON EVERY TEXT", "KEBIASAAN TOGI", False),
        #                     ("YOI GAK BRO", "YOI", False)]
        #            for name, value, inline in field:
        #                embed.add_field(name=name, value=value, inline=inline)
        #            embed.set_footer(text="^^^ TOGI KAWOKAWOKAW")
        #            embed.set_author(name="<-- Togi", icon_url="https://imgur.com/kINAlvJ.png")
        #            embed.set_thumbnail(url=self.guild.icon_url)
        #            embed.set_image(url="https://imgur.com/kINAlvJ.png")

        #            await channel.send(embed=embed)
        #            await channel.send(file=File("./data/togi.png"))
        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        pass


bot = Bot()
