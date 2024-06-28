import discord
import definitions
import asyncio

"""
Parse a dict to be sent as a message to a player

Args:
    dictionary (dict): the dictionary to be parsed
Returns:
    A parsed dictionary in the form of a string
"""
def parseDict(dictionary: dict):
    parsedDict = ""
    for key, value in dictionary.items():
        parsedDict += f"{key.capitalize()}: {value}\n"
    return parsedDict

"""
Parse a list to be sent as a message to a player

Args:
    list: the list to be parsed

Returns:
    A parsed list in the form of a string
"""
def parseList(list):
    parsedList = ""
    for item in list:
        parsedList += f"{item.capitalize()}\n"
    return parsedList

"""
Helper function to get a response to a bot prompt

Args:
    author: the author the response is expected to originate from

Returns:
    the response
    None: timeout after 60 seconds
"""
async def getResponse(bot, author):
    try:
        return await bot.wait_for("message", check=lambda message: checkMessage(author, message), timeout=60)
    except asyncio.TimeoutError:
        return None

"""
Helper function for commands that require a prompt and response

Args:
    author: author of a message
    message (string): message recieved by the bot

Returns
    True: message is from the author and a private DM
    False: Otherwise
"""
def checkMessage(author, message):
    return message.author == author and isinstance(message.channel, discord.DMChannel)

"""
Check if a user has command priveledges

Args:
    author: the author of a message

Returns:
    True: if the author has command priveledges, or if the author is not registered (this will register them with command priveledges)
    False: otherwise
"""
def checkCommandPriveledges(author):
    if author.id in definitions.userCommandPriveledges:
        return definitions.userCommandPriveledges[author.id]
    else:
        grantCommandPrivledges(author)
        return True

"""
grant a user command priveledges

Args:
    author: the author of a command to be granted priveledges
"""
def grantCommandPrivledges(author):
    definitions.userCommandPriveledges[author.id] = True

"""
revoke a user of command priveledges

Args:
    author: the author of a command to be revoked of priveledges
"""
def revokeCommandPriveledges(author):
    definitions.userCommandPriveledges[author.id] = False