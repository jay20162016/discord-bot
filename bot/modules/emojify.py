import emoji

from discord.ext import commands


def buildemojidict(nlp):
    emojis = {}
    for key, value in emoji.EMOJI_ALIAS_UNICODE.items():
        pkey = key.replace(":", "").replace("_", " ").replace("-", " ")
        emojis[nlp(pkey)] = value
    return emojis


def emojimatch(text, nlp, emojidict):
    doc = nlp(text)
    sim_li = []

    for key in emojidict.keys():
        # print(key)
        sim_li.append(doc.similarity(key))

    return list(emojidict.items())[sim_li.index(max(sim_li))]


class Emojify(commands.Cog):
    def __init__(self, bot, nlp):
        self.bot = bot
        self.nlp = nlp

        self.emojidict = buildemojidict(self.nlp)

        # emojimatch("It's sunny outside!", self.nlp, self.emojidict)

    def cog_check(self, ctx):
        return ctx.message.author != self.bot.user and ctx.message.content

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(':'):
            # await message.channel.send(emojimatch(message.content[1:], self.nlp, self.emojidict)[1])
            await message.add_reaction(emojimatch(message.content[1:], self.nlp, self.emojidict)[1])
