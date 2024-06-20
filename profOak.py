from discord.ext import commands, tasks
import discord
import json

BOT_TOKEN = "XXXXX"
WELCOME_CHANNEL_ID = XXXXX
PALLET_TOWN_CHANNEL_ID = XXXXX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to Kanto, Join the pallet-town channel and type !ready when you would like your pokemon journey to begin!")

@bot.command()
async def commands(context):
    channel = context.channel.id
    if channel == WELCOME_CHANNEL_ID:
        await context.send("Commands: \
                           \n!commands: See commands")
    elif channel == PALLET_TOWN_CHANNEL_ID:
        await context.send("Commands: \
                           \n!commands: See commands \
                           \n!ready: Begin your pokemon journey")

bot.run(BOT_TOKEN)