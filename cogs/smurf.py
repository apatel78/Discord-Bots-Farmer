import discord
from discord.ext import commands
import platform
from pathlib import Path
import json
import os
import random

import utils.json

cwd = Path(__file__).parents[1]
cwd = str(cwd)
outer = {}
#outer = json.load(open(cwd+'\localstorage\\smurfs.json'))

#inuse command

#Smurf channel checker
def smurfchannelcheck(channel):
    if channel == 840414501660917790 or channel == 840705049444483102:
        return True
    return False

#Formats the rank
def rankFormater(rank):
    rank = rank.lower()
    rank = rank.capitalize()
    if rank == "Plat":
        rank = "Platinum"
    return rank

#Formats the rank number
def numberFormater(number):
    if number == '0':
        number = ''
    return number

#Error checking for rank input
def rankNumberChecker(rank, number):
    if (number == '0' or number == '1' or number == '2' or number == '3' or number == '') and (not any(i.isdigit() for i in rank)):
        return True
    return False

class Smurf(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Sends a help message to the user about the smurf account commands
    @commands.command()
    @commands.cooldown(1,30, commands.BucketType.guild)
    async def shelp(self, ctx):
        if smurfchannelcheck(ctx.channel.id):
            help1 = open(cwd+'/textfiles/help1.txt', "r")
            help2 = open(cwd+'/textfiles/help2.txt', "r")
            await ctx.send(help1.read())
            await ctx.send(help2.read())

    #Adds a smurf account to the Dicitionary
    @commands.command(name='sadd')
    async def _sadd(self, ctx, username, password, rank, number=''):
        if smurfchannelcheck(ctx.channel.id):

            if await self.bot.config.find_by_username(username) != None:
                await ctx.send(f"{username} already exists")
                return

            rank = rankFormater(rank)
            number = numberFormater(number)

            if (rankNumberChecker(rank, number)):
                    dict = {
                        '_id': username,
                        'Password': password,
                        'Rank': rank,
                        'Rank Number': number,
                        'In Use': False,
                        'Last User': ''
                    }
                    await self.bot.config.insert(dict)
                    await ctx.send(f"{username} added")
            else:
                await ctx.send(f"Invalid Rank Format")


    #Removes a smurf account from the Dictionary
    @commands.command(name='sremove')
    async def _sremove(self, ctx, username):
        if smurfchannelcheck(ctx.channel.id):
            if await self.bot.config.delete_by_username(username) != None:
                await ctx.send(f"{username} was deleted")
            else:
                await ctx.send(f"{username} does not exist")

    #Edit information group
    @commands.group(invoke_without_command=True)
    async def se(self, ctx, username, newusername, newpassword, newrank, newnumber=''):
        if smurfchannelcheck(ctx.channel.id):
            newrank = rankFormater(newrank)
            newnumber = numberFormater(newnumber)

            if (rankNumberChecker(newrank, newnumber)):

                if await self.bot.config.find_by_username(username) != None:
                    dict = {
                        '_id': newusername,
                        'Password': newpassword,
                        'Rank': newrank,
                        'Rank Number': newnumber,
                        'In Use': await self.bot.config.get_status(username),
                        'Last User': await self.bot.config.get_last_user(username)
                    }
                    await self.bot.config.set_all(username, dict)

                    printpassword = await self.bot.config.get_password(newusername)
                    printrank = await self.bot.config.get_rank(newusername) + " " + await self.bot.config.get_rank_number(newusername)
                    printstatus = await self.bot.config.get_status(newusername)
                    if await self.bot.config.get_last_user(newusername) == "":
                        printauthor = "None"
                    else:
                        printauthor = await self.bot.config.get_last_user(newusername)

                    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                    embed.add_field(name="Username", value=f"{newusername}", inline=True)
                    embed.add_field(name="Password", value=f"{printpassword}", inline=True)
                    embed.add_field(name="Rank", value=f"{printrank}", inline=False)
                    embed.add_field(name="In Use", value=f"{printstatus}", inline=True)
                    embed.add_field(name="Last User", value=f"{printauthor}", inline=True)
                    embed.set_author(name=f"Information for {newusername}", icon_url="https://cdn.discordapp.com/attachments/562425394402164736/844299299483680788/HafP3jMkeAAAAAElFTkSuQmCC.png")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"{username} does not exist")

            else:
                await ctx.send(f"Invalid Rank Format")

    #Changes the rank of a smurf account
    @se.command()
    async def erank(self, ctx, username, rank, number=''):
        if smurfchannelcheck(ctx.channel.id):

            rank = rankFormater(rank)
            number = numberFormater(number)

            if (rankNumberChecker(rank, number)):
                if await self.bot.config.find_by_username(username) != None:
                    await self.bot.config.set_rank(username, rank)
                    await self.bot.config.set_rank_number(username, number)
                    await ctx.send(f"{username} had its rank changed to {rank} {number}")
                else:
                    await ctx.send(f"{username} does not exist")
            else:
                await ctx.send(f"Invalid Rank Format")

    #Updates the account username
    @se.command()
    async def eusername(self, ctx, username, newusername):
        if smurfchannelcheck(ctx.channel.id):
            if await self.bot.config.find_by_username(username) != None:
                await self.bot.config.set_username(username, newusername)
                await ctx.send(f"{username} had its username changed to {newusername}")
            else:
                await ctx.send(f"{username} does not exist")

    #Updates the account password
    @se.command()
    async def epassword(self, ctx, username, newpassword):
        if smurfchannelcheck(ctx.channel.id):
            if await self.bot.config.find_by_username(username) != None:
                await self.bot.config.set_password(username, newpassword)
                await ctx.send(f"{username} had its password changed to {newpassword}")
            else:
                await ctx.send(f"{username} does not exist")

    #Update the status of an account
    @commands.command(name='suse')
    async def _suse(self, ctx, username):
        if smurfchannelcheck(ctx.channel.id):

            accounts = await self.bot.config.get_all()

            for dict in accounts:
                for key in dict:
                    if dict['Last User'] == ctx.author.name and dict['In Use'] and dict['_id'] != username:
                        await ctx.send(f"You can't use two accounts, please update the status of {dict['_id']}")
                        return

            if await self.bot.config.find_by_username(username):

                if await self.bot.config.get_status(username) and await self.bot.config.get_last_user(username) != ctx.author.name:
                    await ctx.send(f"{username} is currently being used by {await self.bot.config.get_last_user(username)}")
                    return

                if await self.bot.config.get_status(username):
                    await self.bot.config.set_status(username, False)
                    await ctx.send(f"{username} is no longer in use")

                else:
                    await self.bot.config.set_status(username, True)
                    await ctx.send(f"{username} is now in use")

                await self.bot.config.set_last_user(username, ctx.author.name)

            else:
                await ctx.send(f"{username} does not exist")

    #Prints every account in the database
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,10, commands.BucketType.guild)
    async def ss(self, ctx):
        if smurfchannelcheck(ctx.channel.id):

            accounts = await self.bot.config.get_all()

            for dict in accounts:

                printusername = dict['_id']
                printpassword = dict['Password']
                printrank = dict['Rank'] + " " + dict['Rank Number']
                printstatus = dict['In Use']
                if dict['Last User'] == "":
                    printauthor = "None"
                else:
                    printauthor = dict['Last User']

                embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                embed.add_field(name="Username", value=f"{printusername}", inline=True)
                embed.add_field(name="Password", value=f"{printpassword}", inline=True)
                embed.add_field(name="Rank", value=f"{printrank}", inline=False)
                embed.add_field(name="In Use", value=f"{printstatus}", inline=True)
                embed.add_field(name="Last User", value=f"{printauthor}", inline=True)
                embed.set_author(name=f"Information for {printusername}", icon_url="https://cdn.discordapp.com/attachments/562425394402164736/844299299483680788/HafP3jMkeAAAAAElFTkSuQmCC.png")
                await ctx.send(embed=embed)

    #Finds all accounts with the wanted rank
    @ss.command()
    async def rank(self, ctx, rank):
        if smurfchannelcheck(ctx.channel.id):

            rank = rankFormater(rank)

            if not any(i.isdigit() for i in rank):

                accounts = await self.bot.config.find_by_rank(rank)

                if not accounts:
                    await ctx.send(f"No accounts found in {rank}")
                    return

                for dict in accounts:

                    printusername = dict['_id']
                    printpassword = dict['Password']
                    printrank = dict['Rank'] + " " + dict['Rank Number']
                    printstatus = dict['In Use']
                    if dict['Last User'] == "":
                        printauthor = "None"
                    else:
                        printauthor = dict['Last User']

                    embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                    embed.add_field(name="Username", value=f"{printusername}", inline=True)
                    embed.add_field(name="Password", value=f"{printpassword}", inline=True)
                    embed.add_field(name="Rank", value=f"{printrank}", inline=False)
                    embed.add_field(name="In Use", value=f"{printstatus}", inline=True)
                    embed.add_field(name="Last User", value=f"{printauthor}", inline=True)
                    embed.set_author(name=f"Information for {printusername}", icon_url="https://cdn.discordapp.com/attachments/562425394402164736/844299299483680788/HafP3jMkeAAAAAElFTkSuQmCC.png")
                    await ctx.send(embed=embed)

            else:
                await ctx.send(f"Invalid Rank Format")

    #Finds the account with the wanted username
    @ss.command()
    async def username(self, ctx, username):
        if smurfchannelcheck(ctx.channel.id):

            if await self.bot.config.find_by_username(username) != None:

                dict = await self.bot.config.find_by_username(username)

                printusername = dict['_id']
                printpassword = dict['Password']
                printrank = dict['Rank'] + " " + dict['Rank Number']
                printstatus = dict['In Use']
                if dict['Last User'] == "":
                    printauthor = "None"
                else:
                    printauthor = dict['Last User']

                embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                embed.add_field(name="Username", value=f"{printusername}", inline=True)
                embed.add_field(name="Password", value=f"{printpassword}", inline=True)
                embed.add_field(name="Rank", value=f"{printrank}", inline=False)
                embed.add_field(name="In Use", value=f"{printstatus}", inline=True)
                embed.add_field(name="Last User", value=f"{printauthor}", inline=True)
                embed.set_author(name=f"Information for {printusername}", icon_url="https://cdn.discordapp.com/attachments/562425394402164736/844299299483680788/HafP3jMkeAAAAAElFTkSuQmCC.png")
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"{username} was not found")

    #Prints the accounts that are currently being used
    @ss.command()
    async def use(self, ctx):
        if smurfchannelcheck(ctx.channel.id):

            accounts = await self.bot.config.find_by_status()

            if not accounts:
                await ctx.send(f"No accounts are currently in use")
                return

            for dict in accounts:

                printusername = dict['_id']
                printpassword = dict['Password']
                printrank = dict['Rank'] + " " + dict['Rank Number']
                printstatus = dict['In Use']
                if dict['Last User'] == "":
                    printauthor = "None"
                else:
                    printauthor = dict['Last User']

                embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
                embed.add_field(name="Username", value=f"{printusername}", inline=True)
                embed.add_field(name="Password", value=f"{printpassword}", inline=True)
                embed.add_field(name="Rank", value=f"{printrank}", inline=False)
                embed.add_field(name="In Use", value=f"{printstatus}", inline=True)
                embed.add_field(name="Last User", value=f"{printauthor}", inline=True)
                embed.set_author(name=f"Information for {printusername}", icon_url="https://cdn.discordapp.com/attachments/562425394402164736/844299299483680788/HafP3jMkeAAAAAElFTkSuQmCC.png")
                await ctx.send(embed=embed)

    #Clears the entire list (ONLY FOR BOT OWNER)
    @commands.command(name='sclear')
    @commands.is_owner()
    async def _sclear(self, ctx):
        await self.bot.config.delete_all()
        await ctx.send(f"List Cleared")

    #Sign another user out of an account
    @commands.command(name='ssignout')
    @commands.is_owner()
    async def _ssignout(self, ctx, username):
        await self.bot.config.set_status(username, False)
        await ctx.send(f"{username} is no longer in use")


def setup(bot):
    bot.add_cog(Smurf(bot))
