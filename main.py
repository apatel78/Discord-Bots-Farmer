#Import
import discord
from discord.ext import commands
import logging
from pathlib import Path
import json

#Needed stuff
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

secret_file = json.load(open(cwd+'\secrets.json'))
bot = commands.Bot(command_prefix='!', case_insensitive=True, owner_id=302865175294509057)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

#Holds smurf accounts
bot.outer = {}
outerKey = 1


#When bot is turned on, load the data
@bot.event
async def on_ready():
    bot.outer = read_json("smurfs")
    await bot.change_presence(activity=discord.Game(name=f"I am The Farmer"))


#Error Handling
@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send("Please don't use that command")
    raise error


#Read Files
def read_json(filename):
    with open(f"{filename}.json", "r") as file:
        data = json.load(file)
    return data


#Write Files
def write_json(data, filename):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file)


#Smurf Accounts Commands


#Smurf channel checker
def smurfchannelcheck(channel):
    if channel == 840414501660917790 or channel == 840705049444483102:
        return True
    return False


#Sends a help message to the user about the smurf account commands
@bot.command()
async def shelp(ctx):
    if smurfchannelcheck(ctx.channel.id):
        help1 = open("help.txt", "r")
        help2 = open("help2.txt", "r")
        await ctx.send(help1.read())
        await ctx.send(help2.read())


#Adds a smurf account to the Dicitionary
@bot.command(name='sadd')
async def _sadd(ctx, username, password, rank, number):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            for x, y in v.items():
                if y == username:
                    await ctx.send(f"{username} already exists")
                    return
        if (number == '0' or number == '1' or number == '2' or number == '3') and (not any(i.isdigit() for i in rank)):
                global outerKey
                rank = rank.upper()
                inner = {
                    'Username': username,
                    'Password': password,
                    'Rank': rank,
                    'Rank Number': number,
                    'Status': False,
                    'Last User': ''
                }
                bot.outer.update({outerKey: inner})
                write_json(bot.outer, "smurfs")
                outerKey = outerKey + 1
                await ctx.send(f"{username} added")
        else:
            await ctx.send(f"Invalid Rank Format")


#Removes a smurf account from the Dictionary
@bot.command(name='sremove')
async def _sremove(ctx, username):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            for x, y in v.items():
                if y == username:
                    bot.outer.pop(k)
                    write_json(bot.outer, "smurfs")
                    await ctx.send(f"{username} was deleted")
                    return
        await ctx.send(f"{username} does not exist")


#Changes the rank of a smurf account
@bot.command(name='serank')
async def _serank(ctx, username, rank, number):
    if smurfchannelcheck(ctx.channel.id):
        if (number == '0' or number == '1' or number == '2' or number == '3') and (not any(i.isdigit() for i in rank)):
            rank = rank.upper()
            for k, v in bot.outer.items():
                for x, y in v.items():
                    if y == username:
                        v['Rank'] = rank
                        v['Rank Number'] = number
                        write_json(bot.outer, "smurfs")
                        await ctx.send(f"{username} had its rank changed to {rank} {number}")
                        return
            await ctx.send(f"{username} does not exist")
        else:
            await ctx.send(f"Invalid Rank Format")


#Updates the account username
@bot.command(name='seusername')
async def _seusername(ctx, username, newusername):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            for x, y in v.items():
                if y == username:
                    v['Username'] = newusername
                    write_json(bot.outer, "smurfs")
                    await ctx.send(f"{username} had its username changed to {newusername}")
                    return
        await ctx.send(f"{username} does not exist")


#Updates the account password
@bot.command(name='sepassword')
async def _sepassword(ctx, username, newpassword):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            for x, y in v.items():
                if y == username:
                    v['Password'] = newpassword
                    write_json(bot.outer, "smurfs")
                    await ctx.send(f"{username} had its username changed to {newpassword}")
                    return
        await ctx.send(f"{username} does not exist")


#Updates all information about the account
@bot.command(name='seall')
async def _seall(ctx, username, newusername, newpassword, newrank, newnumber):
    if smurfchannelcheck(ctx.channel.id):
        newrank = newrank.upper()
        if (newnumber == '0' or newnumber == '1' or newnumber == '2' or newnumber == '3') and (not any(i.isdigit() for i in newrank)):
            for k, v in bot.outer.items():
                for x, y in v.items():
                    if y == username:
                        v['Username'] = newusername
                        v['Password'] = newpassword
                        v['Rank'] = newrank
                        v['Rank Number'] = newnumber
                        write_json(bot.outer, "smurfs")
                        await ctx.send(f"{username} became: ```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}```")
                        return
        else:
            await ctx.send(f"Invalid Rank Format")
        await ctx.send(f"{username} does not exist")


#Update the status of an account
@bot.command(name='susing')
async def _susing(ctx, username):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            for x, y in v.items():
                if y == username:
                    if  v['Status'] == True:
                        v['Status'] = False
                    else:
                        v['Status'] = True
                    v['Last User'] = ctx.author.name
                    write_json(bot.outer, "smurfs")
                    if v['Status'] == False:
                        await ctx.send(f"{username} is no longer in use")
                    else:
                        await ctx.send(f"{username} is now in use")
                    return
        await ctx.send(f"{username} does not exist")


#Finds all accounts with the wanted rank
@bot.command(name='sranksearch')
async def _sranksearch(ctx, rank):
    if smurfchannelcheck(ctx.channel.id):
        if not any(i.isdigit() for i in rank):
            rank = rank.upper()
            for k, v in bot.outer.items():
                for x, y in v.items():
                    if y == rank:
                        await ctx.send(f"```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}\nStatus: {v['Status']}\nLast User: {v['Last User']}```")
                        return
            await ctx.send(f"No accounts found in {rank}")
        else:
            await ctx.send(f"Invalid Rank Format")


#Finds the account with the wanted username
@bot.command(name='susersearch')
async def _susersearch(ctx, username):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            for x, y in v.items():
                if y == username:
                    if v['Status']:
                        status = "In Use"
                    else:
                        status = "Not In Use"
                    await ctx.send(f"```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}\nStatus: {v['Status']}\nLast User: {v['Last User']}```")
                    return
        await ctx.send(f"{username} was not found")


#Prints every account in the database
@bot.command(name='sprint')
async def _sprint(ctx):
    if smurfchannelcheck(ctx.channel.id):
        for k, v in bot.outer.items():
            if v['Status']:
                status = "In Use"
            else:
                status = "Not In Use"
            await ctx.send(f"```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}\nStatus: {status}\nLast User: {v['Last User']}```")


#Clears the entire list (ONLY FOR BOT OWNER)
@bot.command(name='sclear')
@commands.is_owner()
async def _sclear(ctx):
    bot.outer.clear()
    write_json(bot.outer, "smurfs")
    await ctx.send(f"List Cleared")


#Turn off the bot (ONLY FOR BOT OWNER)
@bot.command()
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f"Logging off")
    await bot.logout()

#Turn on the bot
bot.run(bot.config_token)
