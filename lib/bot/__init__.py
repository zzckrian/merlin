from asyncio import sleep
from datetime import datetime
from glob import glob
from discord import Embed, File, Intents, Activity, ActivityType
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, Context
from apscheduler.triggers.cron import CronTrigger
from ..db import db

PREFIX = "-"
OWNER_IDS = [503052622438334485]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog jalan (init)")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
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

        print("Starting..")
        print("Loading COGS")

    def run(self, version):
        self.VERSION = version

        print("  /$$      /$$ /$$$$$$$$ /$$$$$$$  /$$       /$$$$$$ /$$   /$$"
              "\n| $$$    /$$$| $$_____/| $$__  $$| $$      |_  $$_/| $$$ | $$"
              "\n| $$$$  /$$$$| $$      | $$  \ $$| $$        | $$  | $$$$| $$"
              "\n| $$ $$/$$ $$| $$$$$   | $$$$$$$/| $$        | $$  | $$ $$ $$"
              "\n| $$  $$$| $$| $$__/   | $$__  $$| $$        | $$  | $$  $$$$"
              "\n| $$\  $ | $$| $$      | $$  \ $$| $$        | $$  | $$\  $$$"
              "\n| $$ \/  | $$| $$$$$$$$| $$  | $$| $$$$$$$$ /$$$$$$| $$ \  $$"
              "\n|__/     |__/|________/|__/  |__/|________/|______/|__/  \__/"

              "\n         MERLIN DISCORD BOT, WRITTEN IN PYTHON 3.9"
              "\n                github.com/zzckrian/merlin"
              "\n      © 2021 zzckrian. See LICENSE.md for more info.")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        print("Running bot")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("Saya belum siap menerima perintah, tunggu beberapa saat.")

    async def rules_reminder(self):
        self.stdout.send("Rules: bebas anjing")

    async def pengingat_sholat(self):
        await self.get_channel(801483230598922261).send("Sholat isya dlu bg")

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print('Bot Disconected')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        else:
            self.stdout.send("Akwokwaokaw error.")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Ngomong nn tuh")

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(776108158891982889)
            self.stdout = self.get_channel(808223116126846986)
            self.scheduler.start()
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.add_job(self.pengingat_sholat, CronTrigger(hour=19, minute=37, second=0))

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

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Bot jalan")
            self.ready = True
            print("Bot Ready")

        else:
            print("Bot Reconnected")

        # STATUS
        await bot.change_presence(activity=Activity(type=ActivityType.listening, name="Ar-Rahman"))
        await sleep(10)
        await bot.change_presence(activity=Activity(type=ActivityType.watching, name="you"))
        await sleep(10)
        await bot.change_presence(activity=Activity(type=ActivityType.playing, name="do you know how to make bot?"))
        await sleep(10)
        await bot.change_presence(activity=Activity(type=ActivityType.watching, name="how to make bot in discord"))

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
