from discord.ext import commands, tasks
import discord

BOT_TOKEN = "XXXXX"
WELCOME_CHANNEL_ID = XXXXX
private_pallet_towns = []
players_directory = "players/"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    guild = bot.guilds[0]
    for channel in guild.channels:
        if "-pallet-town" in channel.name:
            private_pallet_towns.append(channel.id)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to Kanto, type !ready when you would like your pokemon journey to begin!")

@bot.command()
async def commands(context):
    channel = context.channel.id
    if channel == WELCOME_CHANNEL_ID:
        await context.send(f"Commands: \
                           \n!commands: See commands \
                           \n!ready: Begin your pokemon journey")

@bot.command()
async def ready(context):
    channel = context.channel.id
    if channel == WELCOME_CHANNEL_ID:
        guild = context.guild
        author = context.author
        username = author.name
        channel_name = f"{username}-pallet-town"
        if not discord.utils.get(guild.channels, name = channel_name):
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                author: discord.PermissionOverwrite(send_messages=True),
                author: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            private_pallet_towns.append(channel.id)
            with open(f"{players_directory}template.toml", "r") as template:
                templateData = template.read()
                with open(f"{players_directory}{username}.toml", "a") as savefile:
                    savefile.write(templateData)
            await context.send(f"The channel \"{channel_name}\" has been created for you, join it and use !starter to gain your first pokemon!")
        else:
             await context.send(f"The channel \"{channel_name}\" already exists!")     

bot.run(BOT_TOKEN)