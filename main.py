#Standard Libraries
import os
import json
import datetime
import logging

#Third Party
import discord
from pathlib import Path
import motor.motor_asyncio
from discord.ext import commands

#Local
import utils.json
from utils.mongo import Document

#Needed stuff
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

secret_file = utils.json.read_json('token')
bot = commands.Bot(command_prefix='!', case_insensitive=True, owner_id=secret_file['ownerid'])
bot.config_token = secret_file['token']
bot.connection_url = secret_file["mongo"]
logging.basicConfig(level=logging.INFO)

#When bot is turned on, load the data
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"I am The Farmer"))
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["Smurfs"]
    bot.config = Document(bot.db, "testing")

#Error Handling
@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')

    if isinstance(error, commands.CheckFailure):
        await ctx.send("Please don't use that command")

    raise error

#Turn off the bot (ONLY FOR BOT OWNER)
@bot.command()
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f"Logging off")
    await bot.logout()

#Deal with Cogs
if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py" ) and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
