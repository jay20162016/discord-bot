from discord.ext import commands
import discord


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.commands = {"clear": self.clear}

    def cog_check(self, ctx):
        perms = ctx.message.author.permissions_in(ctx.message.channel)
        return perms.read_message_history and perms.manage_messages or ctx.message.author.id == 653364240912089088

    @commands.command()
    async def clear(self, ctx, number: int, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel

        # that id is mine hahaha
        await channel.purge(limit=number + 1)

        await channel.send(f"Deleted {number} messages")
