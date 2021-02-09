import discord
from discord.ext import commands

from bot.utils import database

db = database.database


class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.commands = {"balance": self.balance, "give money": self.give_money}

    def do_get_money(self, user):
        data = db.get(user)

        if data is None or "money" not in data.keys():
            db.update(user, {"money": 1000})
            return 1000

        return data["money"]

    def do_set_money(self, user, money):
        assert money > 0

        db.update(user, {"money": money})

    def do_add_money(self, user, money):
        usermoney = self.do_get_money(user)
        self.do_set_money(user, usermoney + money)

    @commands.command()
    async def balance(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.message.author
        money = self.do_get_money(user)

        await ctx.message.channel.send(f"{user.mention} has ${money}")

    @commands.command(checks=[lambda ctx: ctx.message.author.id == 766274162036572171])
    async def set_money(self, ctx, user: discord.User, money: int):
        self.do_set_money(user, money)

        await ctx.message.channel.send(f"Set {user.mention}'s balance to ${money}")

    @commands.command(checks=[lambda ctx: ctx.message.author.id == 766274162036572171])
    async def add_money(self, ctx, user: discord.User, money: int):
        self.do_add_money(user, money)

        await ctx.message.channel.send(f"Added ${money} to {user.mention}, for a total of ${self.do_get_money(user)}")

    @commands.command()
    async def give_money(self, ctx, user: discord.User, money: int):
        assert money > 0

        self.do_add_money(ctx.message.author, -money)
        self.do_add_money(user, money)

        await ctx.message.channel.send(
            f"{ctx.message.author.mention} gave ${money} to {user.mention}. Now you have ${self.do_get_money(ctx.message.author)}.")
