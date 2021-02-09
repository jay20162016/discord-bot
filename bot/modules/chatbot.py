from discord.ext import commands

import bot.utils.eliza as eliza
import random

eliza = eliza.Eliza()
eliza.load('doctor.txt')

standalone = []

jargon_beginners = ['You are equivalent to', 'You are isomorphic to', 'Go blast yourself with', 
        'You are created with', 'You are similar to', 'You occasionally represent', 'You occasionally resemble',
        'You are like', 'Go rewrite yourself in', 'You are identical to', 'You are', 'Go create a', 'You utter',
        'You can be modeled as', 'You can be mathematically modeled as', ]

jargon_adjectives = ['orbital', 'array of', 'O(n!!) complexity', 'magnetic', '42', '4096', '137578245924',
        'icosahedral', '7th-order', 'dodecahedral prism tesselating']

jargon_nouns = ['laser', 'strikes', 'transistor', 'storage', 
        'rust', 'time', 'space', 'life', 'bot', '\t', '\n']


def jargon():
    if random.random() < 0.2:
        return random.choice(standalone)
    if random.random() < 0.1:
        if random.random() < 0.3:
            return random.random()
        elif random.random() < 0.5:
            return hex(int(random.random()*100000000000))
        else:
            return bin(int(random.random()*1000000000000000000000000000000000000000))

    text = (random.choice(jargon_beginners) + ' a ' + 
            ' '.join([random.choice(jargon_adjectives) for _ in range(random.randint(2, 4))]) + ' ' + 
            random.choice(jargon_nouns))
    return text


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.commands = {"insult": self.insult, "joke": self.insult, "speak": self.insult, "die": self.insult}

    @commands.command()
    async def insult(self, ctx):
        await ctx.channel.send(jargon())

    def cog_check(self, ctx):
        return ctx.message.author != self.bot.user and ctx.message.content

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.random() < 0.1:
            await message.channel.send(jargon())
        response = eliza.respond(message.content)
        if (random.random() < 0.3 or "eliza" in message.content.lower()
                and ('COMMUNITY' in message.guild.features and random.random() < 0.1)) and message.author != self.bot.user:
            await message.channel.send(response)

