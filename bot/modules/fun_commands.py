import random
import zlib

import discord
from discord.ext import commands


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.commands = {"slap": self.slap, "russian roulette": self.russianroulette, "dice": self.dice,
                         "pig latin": self.piglatin, "backward": self.backward, "complexity": self.complexity,
                         "heavserver": self.heavserver, "info": self.info,}

    @commands.command()
    async def info(self, ctx):
        await ctx.message.channel.send(f"I am the 42 bot. Invite me at https://discord.com/api/oauth2/authorize?client_id=779109168468066315&permissions=8&scope=bot . My support server is https://discord.gg/vhDYZcrNfk !")

    @commands.command()
    async def heavserver(self, ctx):
        await ctx.message.channel.send(f"Heavserver is inevitable! Join! https://discord.gg/AFvDGYz")

    @commands.command()
    async def slap(self, ctx, victim: discord.User, *, reason: str):
        await ctx.message.channel.send(f"{ctx.message.author.mention} slapped {victim.mention} for *{reason}*")

    @commands.command()
    async def russianroulette(self, ctx, chance1: int = 1, chance2: int = 6):
        try:
            chance = chance1 / chance2
        except:
            chance = 1 / 6

        if random.random() < chance:
            await ctx.message.channel.send(f"BOOM! {ctx.message.author.mention} died")
        else:
            await ctx.message.channel.send("click.")

    @commands.command()
    async def dice(self, ctx, sides: int = 6):
        await ctx.message.channel.send(f"You rolled a {random.randint(0, sides)}!")

    @commands.command()
    async def piglatin(self, ctx, *, text):
        piglatin = ""

        for word in text.split():
            if word[0] in "aeiou":
                return word + "yay"
            cc = ""
            for i in word:
                if i in "bcdfghjklmnpqrstvwxyz":
                    cc += i
                else:
                    break
            piglatin += word[len(cc):] + cc + "ay "

        await ctx.message.channel.send(piglatin)

    @commands.command()
    async def backward(self, ctx, *, txt):
        await ctx.message.channel.send("".join(list(reversed(txt))))

    @commands.command()
    async def complexity(self, ctx):
        message = ctx.message
        bytemsg = message.content.encode("utf-8")
        compressmsg = zlib.compress(bytemsg)
        cplx = len(compressmsg)
        await message.channel.send(
            f"The complexity of ```{message.content}```, down from {len(bytemsg)} is `{cplx}`")
