import pokemon
import player
import helperFunctions
import party
import definitions

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
    None: no savefile exists or all parameter were empty
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
Obtain the box from the dict of a players toml save file
If you do not need to modify the box, you can simply obtain it by doing getBox(username)
If you need to modify a box you will need to first get the savefile then the box with getBox(None, data)

Args:
    username (string): the players username
    data (dict): toml data representing the save

Returns:
    a players box
    None: no savefile exists or all parameter were empty
    KeyError: a savefile exists but no box exists in the savefile
"""
def getBox(username: str = None, data: dict = None):
    if username is None:
        if data is None:
            return None
        else:
            try:
                playerBox = data["box"]
                return data["box"]
            except KeyError:
                raise KeyError
    else:
        data = player.loadSave(username)
        if data is None:
            return None
        else:
            try:
                playerBox = data["box"]
                return data["box"]
            except KeyError:
                raise KeyError

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
    showSlotNumbers (bool): Indication of if the message should include slot numbers

Returns:
    A message indicating that they either do not have a savefile, their party is empty, or showing the party
"""
def showParty(username: str = None, playerParty: dict = None, showSlotNumbers: bool = False):
    if username is not None:
        playerParty = getParty(username)
        if playerParty is not None:
            message = ""
            for i in range(6):
                    player_pokemon = playerParty[i]
                    if player_pokemon["name"] != "":
                        # Formatting
                        if i != 0:
                            message += "\n"
                        if showSlotNumbers is True:
                            message += f"{i + 1}:\n"
                        message += f"{pokemon.showPokemon(player_pokemon)}\n"
            if message == "":
                return "Your party is empty!"
            else:
                return message
        else:
            return "You must use !ready to create a save file then choose your starter with !starter before you can play!"
    else:
        # party provided
        if playerParty is not None:
            message = ""
            for i in range(6):
                    player_pokemon = playerParty[i]
                    if player_pokemon["name"] != "":
                        # Formatting
                        if i != 0:
                            message += "\n"
                        if showSlotNumbers is True:
                            message += f"{i + 1}:\n"
                        message += f"{pokemon.showPokemon(player_pokemon)}\n"
            if message == "":
                return "Your party is empty!"
            else:
                return message
    
"""
Helper function for the box command

Args:
    author: author of a discord command
"""
async def box(bot, author):
    await author.send(definitions.boxOptions)
    boxOption = await helperFunctions.getResponse(bot, author)
    if boxOption is not None:
        optionContent = boxOption.content.strip().lower()
        if optionContent in definitions.boxOptionResponses:
            username = author.name
            action = definitions.boxOptionResponses[optionContent]
            match action:
                case "show box inventory":
                    inventory = party.showBox(username)
                    await author.send(inventory)
                case "deposit a pokemon":
                    data = player.loadSave(username)
                    playerParty = getParty(None, data)
                    if playerParty is not None:
                        # party is large enough to deposit a pokemon
                        if playerParty[1]["name"] != "":
                            partyString = showParty(None, playerParty, True)
                            await author.send(f"Which pokemon would you like to deposit?\n{partyString}")
                            response = await helperFunctions.getResponse(bot, author)
                            if response is not None:
                                try:
                                    response = int(response.content.strip())
                                    if 1 <= response <= 6:
                                        response -= 1
                                        if playerParty[response]["name"] != "":
                                            try:
                                                box = getBox(None, data)
                                                box.append(playerParty[response])
                                            except KeyError:
                                                data["box"] = []
                                                data["box"].append(playerParty[response])
                                            for i in range(response, 5):
                                                playerParty[i] = playerParty[i + 1]
                                            playerParty[5] = definitions.emptyPokemonSlot
                                            player.saveData(username, data)
                                            await author.send(f"You have deposited {playerParty[response]["name"]}")
                                        else:
                                            await author.send("Please choose an occupied slot")
                                    else:
                                        await author.send("Please enter a valid number for your option")
                                except ValueError:
                                    await author.send("Please enter a valid number for your option")
                            else:
                                await author.send("Response timeout, cancelling transaction")
                        else:
                            await author.send("You must have more than one pokemon in your party to make a deposit")
                    else:
                        await author.send(definitions.noSavefileMessage)
                case "withdraw a pokemon":
                    data = player.loadSave(username)
                    playerParty = getParty(None, data)
                    if playerParty is not None:
                        if playerParty[5]["name"] == "":
                            try:
                                playerBox = getBox(None, data)
                                boxSize = len(playerBox)
                                await author.send(f"Which box pokemon would you like to withdraw?\n\n{showBox(None, playerBox, True)}")
                                response = await helperFunctions.getResponse(bot, author)
                                if response is not None:
                                    try:
                                        response = int(response.content.strip())
                                        response -= 1
                                        if 0 <= response < boxSize:
                                            for i in range(len(playerParty)):
                                                if playerParty[i]["name"] == "":
                                                    playerParty[i] = playerBox[response]
                                                    await author.send(f"You have withdrawn {playerBox[response]["name"]}")
                                                    if len(playerBox) == 1:
                                                        del data["box"]
                                                    else:
                                                        del playerBox[response]
                                                    player.saveData(username, data)
                                                    break
                                        else:
                                            await author.send("Please enter a valid number for your option")
                                    except ValueError:
                                        await author.send("Please enter a valid number for your option")
                                else:
                                    await author.send(definitions.timeoutMessage)
                            except KeyError:
                                await author.send(definitions.noSavefileMessage)
                        else:
                            await author.send("You cannot withdraw a pokemon with a full party")
                    else:
                        await author.send(definitions.noSavefileMessage)
                    
        else:
            await author.send("Invalid selection, cancelling transaction")
    else: 
        await author.send("Response timeout, cancelling transaction")

"""
Show a players box in a string

Args:
    username (string): The username of the player
    playerBox (dict): The player box if it is already accessed
    showSlotNumbers (bool): Indication of if the message should include slot numbers

Returns:
    A message indicating that they either do not have a savefile, their box is empty, or showing the box
"""
def showBox(username: str = None, playerBox: dict = None, showSlotNumbers: bool = False):
    message = ""
    if username is not None:
        try:
            playerBox = getBox(username, None)
            for i in range(len(playerBox)):
                boxPokemon = playerBox[i]
                if showSlotNumbers:
                    message += f"{i + 1}:\n"
                message += f"{pokemon.showPokemon(boxPokemon)}\n"
            if message == "":
                return definitions.emptyBoxMessage
            else:
                return message
        except KeyError:
            return definitions.emptyBoxMessage
    else:
        if playerBox is not None:
            for i in range(len(playerBox)):
                boxPokemon = playerBox[i]
                if showSlotNumbers:
                    message += f"{i + 1}:\n"
                message += f"{pokemon.showPokemon(boxPokemon)}\n"
            if message == "":
                return definitions.emptyBoxMessage
            else:
                return message
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