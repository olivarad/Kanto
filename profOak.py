from discord.ext import commands, tasks
import discord
import directories
import party
import toml
import pokemon

BOT_TOKEN = "XXXXX"
WELCOME_CHANNEL_ID = XXXXX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Pokebot ready")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to Kanto, type !ready when you would like your pokemon journey to begin!")


"""
Direct message processing
"""
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
            fake_context = await bot.get_context(message)
            await bot.invoke(fake_context)
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
        username = author.name
        try:
            with open(f"{directories.players_directory}{username}.toml", 'r') as file:
                await author.send("A save file for pokemon Kanto already exists!")
        except FileNotFoundError:
            with open(f"{directories.players_directory}template.toml", "r") as template:
                templateData = template.read()
                with open(f"{directories.players_directory}{username}.toml", "a") as savefile:
                    savefile.write(templateData) 
                    await author.send("A save file for pokemon Kanto has been created for you!")
        await author.send("Pokemon Kanto is played by sending me DMs, for help with commands, please type !commands!")


"""
If no selection is given, the bot will display starter choices
If a selection is given, the bot will add that to the players first party slot, provided they have not already recieved a starter and that it is a valid starter choice

Args:
    selection (optional)
"""
@bot.command()
async def starter(context, *, selection=None):
    author = context.author
    username = author.name
    filename = f"{directories.players_directory}{username}.toml"

    try:

        # Load the existing player save file
        with open(filename, 'r') as file:
            data = toml.load(file)
        
        # Check if a starter has already been selectedZ
        if "pokemon" in data and len(data["pokemon"]) > 0:
            if data["pokemon"][0]["name"] == "":
                if selection is None:
                    await author.send("The options are as follows \
                                    \nBulbasaur \
                                    \nCharmander \
                                    \nSquirtle \
                                    \nPikachu \
                                    \nWhen you are ready to select use the command again followed by your selection, ex. (!starter Pikachu)")
                else:
                    match selection.upper():
                        case "BULBASAUR":
                            starter = pokemon.Pokemon("Bulbasaur", 5)
                            party.addPartyMember(username, starter)
                            await author.send("You have chosen bulbasaur!")
                        case "CHARMANDER":
                            starter = pokemon.Pokemon("Charmander", 5)
                            party.addPartyMember(username, starter)
                            await author.send("You have chosen charmander!")
                        case "SQUIRTLE":
                            starter = pokemon.Pokemon("Squirtle", 5)
                            party.addPartyMember(username, starter)
                            await author.send("You have chosen Squirtle!")
                        case "PIKACHU":
                            starter = pokemon.Pokemon("Pikachu", 5)
                            party.addPartyMember(username, starter)
                            await author.send("You have chosen Pikachu!")
                        case "MIKUCHU":
                            await author.send("FUCK PIKACHU, GIVE ME MIKUCHU!")
                        case _:
                            await author.send("Invalid selection, please try again!")
            else:
                await author.send("You cannot choose a second starter!")
    
    except FileNotFoundError:
        await author.send("You must use !ready to create a save file before you can play!")

"""
If the player has a party, a message will be sent to them containing each party member and their currentHP
If the pplayer does not have a party, a message will be sent to them about creating a save file and selecting a starter
"""
@bot.command()
async def viewParty(context):
    author = context.author
    username = author.name
    filename = f"{directories.players_directory}{username}.toml"

    try:

        # Load the existing player save file
        with open(filename, 'r') as file:
            data = toml.load(file)

        message = ""
        for i in range(6):
            if data["pokemon"][i]["name"] == "":
                # Formatting
                if i > 0:
                    message += "\n"
                    # Message contains the pokemon name and current HP
                message += f"{data["pokemon"][i]["name"]} \nHP: {data["pokemon"][i]["currentHP"]}"
        if message == "":
            await author.send("Your party is empty!")
        else:
            await author.send(message)

    except FileNotFoundError:
        await author.send("You must use !ready to create a save file then choose your starter with !starter before you can play!")

bot.run(BOT_TOKEN)