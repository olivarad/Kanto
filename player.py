import discord
import directories
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