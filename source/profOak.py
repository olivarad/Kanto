from discord.ext import commands, tasks
import discord
import party
import player
from tokens import BOT_TOKEN
from channels import WELCOME_CHANNEL_ID
import definitions
import helperFunctions

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(definitions.botReadyMessage)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    await channel.send(definitions.joinMessage(member))


# Direct message processing
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages in which the bot is the author
    
    if isinstance(message.channel, discord.DMChannel):
        content = message.content
        if content.startswith("!"):
            # Process as a command
            context = await bot.get_context(message)
            author = context.author
            # Only process commands for those with permission
            if not helperFunctions.checkCommandPriveledges(author):
                return
            # revoke command permission before processing a command
            helperFunctions.revokeCommandPriveledges(author)
            await bot.invoke(context)
            # grant command priveledge after command has completed
            helperFunctions.grantCommandPrivledges(author)
    else:
        await bot.process_commands(message)  # Ensure commands still work in server channels

@bot.command()
async def commands(context):
    author = context.author
    await author.send(definitions.commands)

@bot.command()
async def ready(context):
    channel = context.channel.id
    if channel == WELCOME_CHANNEL_ID:
        author = context.author
        username = author.name
        await author.send(definitions.joinMessage(username))


@bot.command(name="party")
async def party_command(context):
    author = context.author
    await party.party(bot, author)

"""
If no selection is given, the bot will display starter choices
If a selection is given, the bot will add that to the players first party slot, provided they have not already recieved a starter and that it is a valid starter choice

Args:
    selection (optional): starter selected
"""
@bot.command()
async def starter(context, *, selection=None):
    author = context.author
    await author.send(party.chooseStarter(author, selection=selection))

"""
If the player has a party, a message will be sent to them containing each party member and their currentHP
If the pplayer does not have a party, a message will be sent to them about creating a save file and selecting a starter
"""
@bot.command()
async def showParty(context):
    author = context.author
    username = author.name
    await author.send(party.showParty(username))

@bot.command()
async def swapParty(context, slot1, slot2):
    author = context.author
    username = author.name
    slot1, slot2 = int(slot1) - 1, int(slot2) - 1
    await author.send(party.swapParty(username, slot1, slot2))

@bot.command()
async def box(context):
    author = context.author
    await party.box(bot, author)
    

@bot.command()
async def showBadges(context):
    author = context.author
    username = author.name
    await author.send(player.showBadges(username))

@bot.command()
async def showInventory(context):
    author = context.author
    username = author.name
    await author.send(player.showInventory(username))

bot.run(BOT_TOKEN)
