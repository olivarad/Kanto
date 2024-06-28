import pokemon
import player

# Acceptable Starters
acceptableStarters = {
    "BULBASAUR", "CHARMANDER", "SQUIRTLE", "PIKACHU"
}

"""
Obtain the party from the dict of a players toml save file
If you do not need to modify the party, you can simply obtain it by doing getParty(username)
If you need to modify a party you will need to first get the savefile then the party with getParty(None, data)

Args:
    username (string): the players username
    data (dict): toml data representing the save

Returns:
    a players party
"""
def getParty(username: str = None, data: dict = None):
    if username is None:
        if data is None:
            return None
        else:
            return data["pokemon"]
    else:
        data = player.loadSave(username)
        if data is None:
            return None
        else:
            return data["pokemon"]

"""
Add a pokemon to a players party
If the party is full, the pokemon should instead be added to their pc

Args:
    username (string): The username of the player
    pokemon (A Pokemon class instance defined in pokemon.py)
"""
def addPartyMember(username: str, pokemon: pokemon.Pokemon):
    data = player.loadSave(username)
    if data is not None:
        # Check for an open slot and fill it
        # TODO If no open slot is found add it to the pc
        playerParty = getParty(None, data)
        for partySlot in playerParty:
            if partySlot.get("name", "") == "":
                pokemon.loadPokemonTOML(partySlot)
                break
        player.saveData(username, data)

"""
Helper function for the bot command !starter

Args:
    author: the author of a message
    selection (optional): starter selected

Returns:
    message for display in the !starter command
"""
def chooseStarter(author, *, selection=None):
    if selection is None:
        message = "The options are as follows \
                        \nBulbasaur \
                        \nCharmander \
                        \nSquirtle \
                        \nPikachu \
                        \nWhen you are ready to select use the command again followed by your selection, ex. (!starter Pikachu)"
    else:
        username = author.name
        data = player.loadSave(username)
        if data is not None:
            playerParty = getParty(None, data)
            if playerParty[0]["name"] == "":
                    selection = selection.upper()
                    if selection in acceptableStarters:
                        selection = selection.capitalize()
                        starter = pokemon.Pokemon(selection, 5)
                        addPartyMember(username, starter)
                        message = f"You have chosen {selection.lower()}!"
                    else:
                        match selection:
                            case "MIKUCHU":
                                message = "FUCK PIKACHU, GIVE ME MIKUCHU!"
                            case _:
                                message = "Invalid selection, please try again!"
            else:
                message = "You cannot choose a second starter!"
        else:
            message = "You must use !ready to create a save file before you can play!"
    return message

"""
Show a players party in a string

Args:
    username (string): The username of the player

Returns:
    A message indicating that they either do not have a savefile, their party is empty, or showing the party
"""
def showParty(username: str):
    playerParty = getParty(username)
    if playerParty is not None:
        message = ""
        for i in range(6):
                pokemon = playerParty[i]
                if pokemon["name"] != "":
                    # Formatting
                    if i > 0:
                        message += "\n"
                        # Message contains the pokemon name and current HP
                    message += f"{pokemon["name"]} \nHP: {pokemon["currentHP"]}"
        if message == "":
            return "Your party is empty!"
        else:
            return message
    else:
        return "You must use !ready to create a save file then choose your starter with !starter before you can play!"
    
"""
Swap two members in a players party

Args:
    username (string): the username of the player
    slot1 (int): first pokemon slot
    slot2 (int): second pokemon slot

Returns:
    A message indicating success, or debug data
"""
def swapParty(username: str, slot1: int, slot2: int):
    data = player.loadSave(username)
    playerParty = getParty(None, data)
    if 0 <= slot1 <= 5 and 0 <= slot2 <= 5 and slot1 != slot2:
        if playerParty[slot1]["name"] != "" and playerParty[slot2]["name"] != "":
            message = f"Before:\n\n{showParty(username)}\n\n"
            tempSlot = playerParty[slot1]
            playerParty[slot1] = playerParty[slot2]
            playerParty[slot2] = tempSlot
            player.saveData(username, data)
            message += f"After:\n\n{showParty(username)}"
        else:
            message = "Slots chosen must be filled"
    else:
        message = "Please choose valid slots 1 through 6 that are not equal to each other"
    return message