from random import choice, randint
from typing import Optional

from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from aiohttp import request


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    # TEST COMMAND
    @command(name="test", aliases=["tst"])
    async def test_command(self, ctx):
        await ctx.send(f"{choice(('bot is running', 'kefo'))} {ctx.author.mention}")

    # ABOUT COMMAND
    @command(name="about", aliases=["abt"])
    async def test_command(self, ctx):
        await ctx.send("https://eskrimlezat.rf.gd/home/about-me/")

    # DICE COMMAND
    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        rolls = [randint(i, value) for i in range(dice)]

        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

    # SLAP COMMAND
    @command(name="slap", aliases=["tenggeul"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.mention} nyabok {member.mention} pedah {reason}!")

    # SAY COMMAND
    @command(name="say", aliases=["ngomong"])
    async def say_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    # ANIMAL PIC COMMAND
    @command(name="pic", aliases=["foto"])
    async def pic(self, ctx, pic: str):
        if pic.lower() in ("dog", "cat", "panda", "fox", "koala"):
            URL = f"https://some-random-api.ml/img/{pic.lower()}"

            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.send(data["link"])
                else:
                    await ctx.send(f"API merespon balik {response.status}")

        else:
            await ctx.send(f"Tidak ada foto yang ditemukan untuk hewan '{pic.lower()}'")

    # ANIMAL FACT COMMAND
    @command(name="fact", aliases=["aseli"])
    async def fact(self, ctx, animal: str):
        if animal.lower() in ("dog", "cat", "panda", "fox", "koala"):
            URL = f"https://some-random-api.ml/facts/{animal.lower()}"

            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.send(data["fact"])
                else:
                    await ctx.send(f"API merespon balik {response.status}")

        else:
            await ctx.send(f"Tidak ada fakta yang ditemukan untuk hewan '{animal.lower()}'")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

        await self.bot.stdout.send("Fun cogs jalan")


def setup(bot):
    bot.add_cog(Fun(bot))
