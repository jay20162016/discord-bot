import asyncio
import random
from datetime import datetime, timedelta, timezone

from discord.ext import tasks, commands


def get_seconds_until(hour, minute):
    now = datetime.now(tz=timezone.utc)
    return (timedelta(hours=24) - (now - now.replace(hour=hour, minute=minute))).total_seconds() % (24 * 3600)


class LotteryGame(commands.Cog):
    def __init__(self, bot, num_tickets=1000, ticket_cost=-10, winner_money=10000):
        self.bot = bot
        self.num_of_tickets = num_tickets
        self.ticket_list = {}
        self.ticket_cost = ticket_cost
        self.winner_money = winner_money

        self.lottery_winners.start()

        self.commands = {"buy ticket": self.buy_ticket, "lottery status": self.lottery_status}

    @commands.command()
    async def buy_ticket(self, ctx, number: int = -1):
        while number < 0 or number > self.num_of_tickets or number in self.ticket_list.keys():
            number = random.randint(0, self.num_of_tickets)

        money = self.bot.get_cog('Money')

        if money.do_get_money(ctx.message.author) < self.ticket_cost:
            return

        money.do_add_money(ctx.message.author, self.ticket_cost)

        self.ticket_list[number] = ctx.message.author

        await ctx.message.channel.send(f"Bought ticket #{number}. Good Luck!")

    @commands.command()
    async def lottery_status(self, ctx):
        s = "Here are the disposition of the tickets:\n"
        for k, v in self.ticket_list.items():
            s += f"#{k} belongs to {v.mention}\n"
        await ctx.message.channel.send(s)

    @tasks.loop(hours=3)
    async def lottery_winners(self):
        print("LOTTERY TIME")
        winning_number = random.randint(0, self.num_of_tickets)
        winner = self.ticket_list[winning_number] if winning_number in self.ticket_list.keys() else None

        if winner is not None:
            money = self.bot.get_cog('Money')
            money.do_add_money(winner, self.winner_money)

        for guild in self.bot.guilds:
            try:
                message_channel = guild.system_channel
                if message_channel is None:
                    message_channel = guild.text_channels[0]
                async with message_channel.typing():
                    await message_channel.send("**Lottery Drawing Time!!!**")
                    await asyncio.sleep(10)

                    await message_channel.send("*The winner of the lottery is...*")
                    await asyncio.sleep(5)

                    if winner is not None:
                        await message_channel.send(f"{winner.mention}!")
                    else:
                        await message_channel.send("Nobody won...")
            except:
                pass
        if winner is not None:
                self.ticket_list = {}

