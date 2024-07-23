import pokemon
import player
import helperFunctions
import party
import definitions

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
    bot: discord bot
    author: the author of a message
"""
async def starter(bot, author):
    await author.send(definitions.starterOptionsMessage)
    starterOption = await helperFunctions.getResponse(bot, author)
    if starterOption is not None:
        optionContent = starterOption.content.strip().upper()
        if optionContent in definitions.boxOptionResponses:
            username = author.name
            "TODO: FINISH DUE TO EEPY, FOLLOW BOX FUNCTION"
            pass

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
        return definitions.acceptableStarterMessage
    else:
        username = author.name
        data = player.loadSave(username)
        if data is not None:
            playerParty = getParty(None, data)
            if playerParty[0]["name"] == "":
                    selection = selection.upper()
                    if selection in definitions.acceptableStarters.values():
                        selection = selection.capitalize()
                        starter = pokemon.Pokemon(selection, 5)
                        addPartyMember(username, starter)
                        return f"You have chosen {selection.lower()}!"
                    else:
                        match selection:
                            case "MIKUCHU":
                                return "FUCK PIKACHU, GIVE ME MIKUCHU!"
                            case _:
                                return "Invalid selection, please try again!"
            else:
                return "You cannot choose a second starter!"
        else:
            return definitions.noSavefileMessage

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
                return definitions.emptyPartyMessage
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
                return definitions.emptyPartyMessage
            else:
                return message
    
"""
Helper function for the party command

Args
    bot: discord bot
    author: author of a discord command
"""
async def party(bot, author):
    username = author.name
    data = player.loadSave(username)
    if data is not None:
        playerParty = getParty(None, data)
        if playerParty[0]["name"] != "":
            # Party options other than choosing a starter
            while True:
                await author.send(definitions.partyOptions)
                response = await helperFunctions.getResponse(bot, author)
                if response is not None:
                    response = response.content.strip().upper()
                    if response in definitions.partyOptions.upper():
                        match response:
                            case "1" | "SHOW PARTY":
                                await author.send(showParty(None, playerParty))
                                return
                            case "2" | "SWAP PARTY ORDER":
                                await swapParty(bot, author)
                                return
                else:
                    await author.send(definitions.timeoutMessage)
                    break
        else:
            # Offer the player to choose a starter
            while True:
                await author.send(definitions.acceptableStarterMessage)
                response = await helperFunctions.getResponse(bot, author)
                if response is not None:
                    response = response.content.strip().upper()
                    if response in definitions.acceptableStarters:
                        choice = definitions.acceptableStarters[str(response)]
                        await author.send(chooseStarter(author, selection=choice))
                        break
                else:
                    await author.send(definitions.timeoutMessage)
                    break
    else:
        return definitions.noSavefileMessage

"""
Helper function for the box command

Args
    bot: discord bot
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
                    inventory = showBox(username)
                    await author.send(inventory)
                case "deposit a pokemon":
                    data = player.loadSave(username)
                    playerParty = getParty(None, data)
                    if playerParty is not None:
                        # party is large enough to deposit a pokemon
                        if playerParty[1]["name"] != "":
                            partyString = showParty(None, playerParty, True)
                            await author.send(f"{definitions.boxDepositPromptMessage}{partyString}")
                            response = await helperFunctions.getResponse(bot, author)
                            if response is not None:
                                try:
                                    response = int(response.content.strip())
                                    if 1 <= response <= 6:
                                        response -= 1
                                        if playerParty[response]["name"] != "":
                                            name = playerParty[response]["name"]
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
                                            await author.send(f"{definitions.boxDepositConfirmationMessage}{name}")
                                        else:
                                            await author.send(definitions.nonFilledSlotBoxMessage)
                                    else:
                                        await author.send(definitions.chooseValidNumberMessage)
                                except ValueError:
                                    await author.send(definitions.chooseValidNumberMessage)
                            else:
                                await author.send(definitions.timeoutMessage)
                        else:
                            await author.send(definitions.boxDepositInsufficientPartySizeMessage)
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
                                await author.send(f"{definitions.boxWithdrawPromptMessage}{showBox(None, playerBox, True)}")
                                response = await helperFunctions.getResponse(bot, author)
                                if response is not None:
                                    try:
                                        response = int(response.content.strip())
                                        response -= 1
                                        if 0 <= response < boxSize:
                                            for i in range(len(playerParty)):
                                                if playerParty[i]["name"] == "":
                                                    playerParty[i] = playerBox[response]
                                                    await author.send(f"{definitions.boxWithdrawConfirmationMessage}{playerBox[response]["name"]}")
                                                    if len(playerBox) == 1:
                                                        del data["box"]
                                                    else:
                                                        del playerBox[response]
                                                    player.saveData(username, data)
                                                    break
                                        else:
                                            await author.send(definitions.chooseValidNumberMessage)
                                    except ValueError:
                                        await author.send(definitions.chooseValidNumberMessage)
                                else:
                                    await author.send(definitions.timeoutMessage)
                            except KeyError:
                                await author.send(definitions.noSavefileMessage)
                        else:
                            await author.send(definitions.boxWithdrawInvalidPartySizeMessage)
                    else:
                        await author.send(definitions.noSavefileMessage)
                    
        else:
            await author.send(definitions.invalidSelectionMessage)
    else: 
        await author.send(definitions.timeoutMessage)

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
    bot: discord bot
    author: author of a discord command

Returns:
    A message indicating success, or debug data
"""
async def swapParty(bot, author):
    username = author.name
    data = player.loadSave(username)
    playerParty = getParty(None, data)
    validSlots = []
    for slot in playerParty:
        if slot["name"] != "":
            validSlots.append(slot)
        else:
            break
    if len(validSlots) >= 2:
        validSlotsNames = []
        for slot in validSlots:
            validSlotsNames.append(slot["name"])
        while True:
            message = definitions.swapPartyFirstSelectionMessage
            for i in range(0, len(validSlotsNames)):
                message += f"\n{i + 1}: {validSlotsNames[i]}"
            await author.send(message)
            response = await helperFunctions.getResponse(bot, author)
            if response is not None:
                response = response.content.strip()
                try:
                    if 0 < int(response) < len(validSlots) + 1:
                        slot1value = int(response) - 1
                        slot1 = validSlots[slot1value]
                        break
                except ValueError:
                    pass
            else:
                await author.send(definitions.timeoutMessage)
                return
        while True:
            message = definitions.swapPartySecondSelectionMessage
            for i in range(0, len(validSlotsNames)):
                message += f"\n{i + 1}: {validSlotsNames[i]}"
            await author.send(message)
            response = await helperFunctions.getResponse(bot, author)
            if response is not None:
                response = response.content.strip()
                try:
                    if 0 < int(response) < len(validSlots) + 1:
                        slot2value = int(response) - 1
                        slot2 = validSlots[slot2value]
                        break
                except ValueError:
                    pass
            else:
                await author.send(definitions.timeoutMessage)
                return
        message = f"Before:\n\n{showParty(username)}\n\n"
        tempSlot = slot1
        playerParty[slot1value] = slot2
        playerParty[slot2value] = tempSlot
        player.saveData(username, data)
        message += f"After:\n\n{showParty(username)}"
        await author.send(message)