import logging
import collections

class Document:

    #Initalization
    def __init__(self, connection, document_name):

        self.db = connection[document_name]
        self.logger = logging.getLogger(__name__)

    #Search By Functions
    #TESTED
    async def find_by_username(self, username):

        return await self.db.find_one({"_id": username})

    async def find_by_rank(self, rank):

        data = []

        async for document in self.db.find({"Rank" : rank}):
            data.append(document)

        return data

    async def find_by_status(self):

        data = []

        async for document in self.db.find({"In Use" : True}):
            data.append(document)

        return data

    #Remove Functions
    #TESTED
    async def delete_by_username(self, username):

        if not await self.find_by_username(username):
            return

        await self.db.delete_many({"_id": username})
        return 1

    async def delete_all(self):

        async for document in self.db.find({}):
            await self.db.delete_many(document)

    #Add/Insert Functoins
    #TESTED
    async def insert(self, dict):

        await self.db.insert_one(dict)

    #Setter Functoins
    #TESTED (Not Fully Status and Last user)
    async def set_all(self, username, dict):

        oldId = await self.db.find_one({'_id':username})
        oldId['_id'] = dict['_id']
        await self.db.insert_one(oldId)
        await self.db.delete_many({"_id":username})

        await self.db.update_one({"_id": oldId['_id']}, {"$set": dict})

    async def set_username(self, username, newusername):

        oldId = await self.db.find_one({'_id':username})
        oldId['_id'] = newusername
        await self.db.insert_one(oldId)
        await self.db.delete_many({"_id":username})

    async def set_password(self, username, password):

        await self.db.update_one({"_id": username}, {"$set": {"Password": password}})

    async def set_rank(self, username, rank):

        await self.db.update_one({"_id": username}, {"$set": {"Rank": rank}})

    async def set_rank_number(self, username, number):

        await self.db.update_one({"_id": username}, {"$set": {"Rank Number": number}})

    async def set_status(self, username, status):

        await self.db.update_one({"_id": username}, {"$set": {"In Use": status}})

    async def set_last_user(self, username, user):

        await self.db.update_one({"_id": username}, {"$set": {"Last User": user}})


    #Getter Functions
    async def get_all(self):

        data = []

        async for document in self.db.find({}):
            data.append(document)

        return data

    async def get_password(self, username):

        dict = await self.db.find_one({"_id": username})

        return dict['Password']

    async def get_rank(self, username):

        dict = await self.db.find_one({"_id": username})

        return dict['Rank']

    async def get_rank_number(self, username):

        dict = await self.db.find_one({"_id": username})

        return dict['Rank Number']

    async def get_status(self, username):

        dict = await self.db.find_one({"_id": username})

        return dict['In Use']

    async def get_last_user(self, username):

        dict = await self.db.find_one({"_id": username})

        return dict['Last User']
