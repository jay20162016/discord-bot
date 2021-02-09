import discord
import pymongo

from bot.utils.lru_cache import LRUCache

client = pymongo.MongoClient(
    "mongodb+srv://admin:4PG5JNxRoU1CirZG@moneygamecluster-jtgj1.gcp.mongodb.net/discord?retryWrites=true&w=majority")
db = client.discord
collection: pymongo.collection.Collection = db.users


class UserDatabase:
    def __init__(self, cache_size=32):
        self.cache = LRUCache(cache_size)
        self.cache_size = cache_size

    def get(self, user: discord.User):
        cached = self.cache.get(user)

        if cached is None:
            query = {"_id": user.id}
            result = collection.find_one(query)

            if result is not None:
                self.cache.put(user, result)

            return result

        return cached

    def update(self, user: discord.User, data):
        query = {"_id": user.id}
        result = collection.find_one(query)

        if result is None:
            data.update(query)
            collection.insert_one(data)
            result = {}
        else:
            collection.update_one(query, {"$set": data})

        result.update(data)

        self.cache.put(user, result)


database = UserDatabase()
