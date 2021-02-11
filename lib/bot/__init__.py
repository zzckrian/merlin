from discord import Intents
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "2"
OWNER_IDS = [503052622438334485]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )
    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        print("Running bot")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Ngontol")

    async def on_disconnect(self):
        print('awakoawk crash')

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(776108158891982889)
            print("bot ready")

            channel = self.get_channel(808223116126846986)
            await channel.send("Togi Menggokilzzz")

            embed = Embed(title="List death note 11/02/21", description="Lo kontol")
            fields = [("Togi", "Ngontol", True),
                        ("Togi", "Ngontol", True),
                        ("Togi gokil", "Oke", True),
                        ("client.on", "kawoawkoawok", True),
                        ("a", "a", True)
                      ]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await channel.send(embed=embed)

            embed = Embed(title="DEATH NOTE", description="11/02/21", color=0xff0963)
            field = [("TOGI", "F", False),
                     ("CLIENT.ON EVERY TEXT", "KEBIASAAN TOGI", False),
                     ("YOI GAK BRO", "YOI", False)]
            embed.set_footer(text="HH KAWOKAWOKAW")
            for name, value, inline in field:
                embed.add_field(name=name, value=value, inline=inline)
            await channel.send(embed=embed)
        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        pass

bot = Bot()
