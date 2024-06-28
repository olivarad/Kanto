import discord
import directories
import helperFunctions
import toml

"""
Check for a player save file and make one if it does not exist

Args:
    author: the author of a message
"""
async def checkForSave(author):
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

"""
Load a players save file

Args:
    username (string): The username of the player

Returns:
    toml data (file exists)
    None (file does not exist)
"""
def loadSave(username: str):
    filename = f"{directories.players_directory}{username}.toml"
    try: 
        with open(filename, 'r') as file:
            data = toml.load(file)
            return data
    except FileNotFoundError:
        print("loadSave: FILE NOT FOUND")
        return None

"""
Load a players inventory to a dict
If you do not need to modify the inventory, you can simply obtain it by doing loadInventory(username)
If you need to modify an inventory you will need to first get the savefile then the inventory with loadInventory(None, data)

Args:
    username (string): the players username
    data (dict): a players savefile

Returns:
    the inventory of a player in toml dictionary format
"""
def loadInventory(username: str = None, data: dict = None):
    if username is None:
        if data is None:
            return None
        else:
            return data["inventory"]
    else:
        data = loadSave(username)
        if data is None:
            return None
        else:
            return data["inventory"]

"""
Save data to a players save file

Args:
    username (string): The username of the player
    data (dict): toml data representing the save
"""
def saveData(username: str, data: dict):
    filename = f"{directories.players_directory}{username}.toml"
    try:
        with open(filename, 'w') as file:
            toml.dump(data, file)
    except FileNotFoundError:
        print("saveData: FILE NOT FOUND")

"""
Helper function to give the bot a players inventory

Args:
    username (string): The username of the player

Returns:
    a message indicating that no save file exists or contatining the users inventory
"""
def showInventory(username: str):
    inventory = loadInventory(username)
    if inventory is None:
        return "No Savefile Exists"
    else:
        return helperFunctions.parseDict(inventory)
