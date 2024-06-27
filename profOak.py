from discord.ext import commands, tasks
import discord
import directories
import toml
import pokemon
import party
import player
from tokens import BOT_TOKEN
from channels import WELCOME_CHANNEL_ID

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
    await context.send(f"Commands: \
                        \n!commands: See commands \
                        \n!ready: Begin your pokemon journey (can not be used more than once) \
                        \n!starter: Indicate that you would like to choose your starter pokemon \
                        \n!viewParty: View your party")

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
    username = author.name

    if selection is None:
        await author.send("The options are as follows \
                        \nBulbasaur \
                        \nCharmander \
                        \nSquirtle \
                        \nPikachu \
                        \nWhen you are ready to select use the command again followed by your selection, ex. (!starter Pikachu)")
    else:
        data = player.loadSave(username)
        if data is not None:
            playerParty = player.getParty(data)
            if playerParty[0]["name"] == "":
                    selection = selection.upper()
                    if selection in party.acceptableStarters:
                        selection = selection.capitalize()
                        starter = pokemon.Pokemon(selection, 5)
                        party.addPartyMember(username, starter)
                        await author.send(f"You have chosen {selection.lower()}!")
                    else:
                        match selection:
                            case "MIKUCHU":
                                await author.send("FUCK PIKACHU, GIVE ME MIKUCHU!")
                            case _:
                                await author.send("Invalid selection, please try again!")
            else:
                await author.send("You cannot choose a second starter!")
        else:
            await author.send("You must use !ready to create a save file before you can play!")

"""
If the player has a party, a message will be sent to them containing each party member and their currentHP
If the pplayer does not have a party, a message will be sent to them about creating a save file and selecting a starter
"""
@bot.command()
async def viewParty(context):
    author = context.author
    username = author.name

    data = player.loadSave(username)

    if data is not None:
        message = ""
        playerParty = player.getParty(data)
        for i in range(6):
            pokemon = playerParty[i]
            if pokemon["name"] != "":
                # Formatting
                if i > 0:
                    message += "\n"
                    # Message contains the pokemon name and current HP
                message += f"{pokemon["name"]} \nHP: {pokemon["currentHP"]}"
        if message == "":
            await author.send("Your party is empty!")
        else:
            await author.send(message)

    else:
        await author.send("You must use !ready to create a save file then choose your starter with !starter before you can play!")

bot.run(BOT_TOKEN)