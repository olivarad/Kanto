from discord.ext import commands, tasks
import discord
import directories
import toml
import pokemon
import party
import player
from tokens import BOT_TOKEN
from channels import WELCOME_CHANNEL_ID
import definitions

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Pokebot ready")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to Kanto, type !ready when you would like your pokemon journey to begin!")

# Direct message processing
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages in which the bot is the author
    
    if isinstance(message.channel, discord.DMChannel):
        content = message.content
        if content.startswith("!"):
            # Process as a command
            command = content[1:].split()[0]  # Extract the command (without the prefix '!')
            args = content[len(command)+1:].strip()  # Extract arguments if any
            context = await bot.get_context(message)
            await bot.invoke(context)
    else:
        await bot.process_commands(message)  # Ensure commands still work in server channels

@bot.command()
async def commands(context):
    await context.send(definitions.commands)

@bot.command()
async def ready(context):
    channel = context.channel.id
    if channel == WELCOME_CHANNEL_ID:
        author = context.author
        await player.checkForSave(author)
        await author.send("Pokemon Kanto is played by sending me DMs, for help with commands, please type !commands!")


"""
If no selection is given, the bot will display starter choices
If a selection is given, the bot will add that to the players first party slot, provided they have not already recieved a starter and that it is a valid starter choice

Args:
    selection (optional): starter selected
"""
@bot.command()
async def starter(context, *, selection=None):
    author = context.author
    message = party.chooseStarter(author, selection=selection)
    await author.send(message)

"""
If the player has a party, a message will be sent to them containing each party member and their currentHP
If the pplayer does not have a party, a message will be sent to them about creating a save file and selecting a starter
"""
@bot.command()
async def showParty(context):
    author = context.author
    username = author.name
    message = party.showParty(username)
    await author.send(message)

@bot.command()
async def swapParty(context, slot1, slot2):
    author = context.author
    username = author.name
    slot1, slot2 = int(slot1) - 1, int(slot2) - 1
    message = party.swapParty(username, slot1, slot2)
    await author.send(message)

@bot.command()
async def showBadges(context):
    author = context.author
    username = author.name
    badges = player.showBadges(username)
    await author.send(badges)

@bot.command()
async def showInventory(context):
    author = context.author
    username = author.name
    inventory = player.showInventory(username)
    await author.send(inventory)

bot.run(BOT_TOKEN)
