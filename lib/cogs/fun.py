from discord.ext.commands import Cog
from random import choice, randint
from discord.ext.commands import command


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="test", aliases=["tst"])
    async def test_command(self, ctx):
        await ctx.send(f"{choice(('togi', 'agus', 'warman'))} {ctx.author.mention}")

    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        rolls = [randint(i, value) for i in range(dice)]

        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

        await self.bot.stdout.send("fun cogs jalan yh")
        print("fun cogs yh")


def setup(bot):
    bot.add_cog(Fun(bot))
