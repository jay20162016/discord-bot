import inspect

import discord
from discord.ext import commands

# import inspect
from bot import modules
from difflib import SequenceMatcher
import itertools
import random

bot = commands.Bot(command_prefix='.')

class nlp_like:
    def __init__(self, x):
        self.x = x + '\t\t\tword'

    def similarity(self, x):
        x0 = self.x.split()
        x1 = x.x.split()

        total = []

        for a, b in itertools.product(x0, x1):
            total.append(
                    SequenceMatcher(None, a, b).ratio()
                )

        return sum(total + [0]) / (abs(len(x0)-len(x1)) + 1) * 7


# nlp = spacy.load("en_trf_distilbertbaseuncased_lg", disable=["tagger", "parser", "ner"])
nlp = nlp_like

print("Initializing cogs...")

cogs = [
    modules.AdminCommands(bot),
    modules.FunCommands(bot),

    modules.Emojify(bot, nlp=nlp),
    modules.Chatbot(bot),

    modules.Money(bot),

    modules.LotteryGame(bot)
]

print("Done Initializing cogs!")

for cog in cogs:
    bot.add_cog(cog)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    activity = discord.Game("Use .help for a command list. Waiting for Orders, Your Most Honorable Majesty...")
    status = discord.Status.idle
    await bot.change_presence(status=status, activity=activity)


@bot.event
async def on_disconnect():
    print("Disconnected! ...")


def similarity(a, b):
    return nlp(a).similarity(nlp(b))


async def null(*whatever):
    return whatever


async def scanfor(param: inspect.Parameter, message, ctx):
    cmd = commands.Command(null)

    if param.kind == inspect.Parameter.KEYWORD_ONLY:
        return " ".join(message)

    default = None
    if param.default != inspect.Parameter.empty:
        default = param.default

    if not param.annotation:
        return message[0]

    for word in message:
        try:
            converted = await cmd.do_conversion(ctx, param.annotation, word, param)
            return converted
        except Exception as e:
            pass

    return default


disable=False
@bot.event
async def on_message(message: discord.Message):
    global disable
    if '~~s' in message.content:
        await message.channel.send(str(disable))
    if '~~d' in message.content:
        disable = not disable
        print("DISABLLEE", disable)
        return
    if '~~e' in message.content and message.author.id == 766274162036572171:
        print("EXECUTING! ", message.content)
        awaitables = []
        exec(message.content.replace('~~e', '').strip())
        for a in awaitables:
            print(a)
            print(await a)
    if disable:
        print("DESABLED")
        return
    if 'COMMUNITY' in message.guild.features:
        print("STOPCRIME")
        await bot.process_commands(message)
        return
    print("MESSAGE!!!!!!!")
    compare = ''.join([i for i in message.content if not i.isdigit()])

    function_list = []
    similarity_list = []
    for cog in cogs:
        if hasattr(cog, "commands"):
            for command, function in cog.commands.items():
                function_list.append(function)
                similarity_list.append(similarity(command, compare))

    max_sim = max(similarity_list)
    most_similar_ind = similarity_list.index(max_sim)
    most_similar = function_list[most_similar_ind]

    to_scan = message.content.strip().split()

    ctx = await bot.get_context(message)

    kwargs = {}
    # commands.Command.do_conversion()
    parameters = inspect.signature(most_similar._callback).parameters

    for name, param in list(parameters.items())[2:]:
        kwargs[name] = await scanfor(param, to_scan, ctx)

    if max_sim > 0.7 and message.author != bot.user or random.random() < 0.2:
        try:
            await most_similar(ctx, **kwargs)
        except:
            pass

    await bot.process_commands(message)


with open(".token.txt") as f:
    token = f.read().strip()

bot.run(token)
