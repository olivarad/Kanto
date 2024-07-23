import player

acceptableStarterMessage = "Please choose from these accepted starters: \
    \n1: Bulbasaur \
    \n2: Charmander \
    \n3: Squirtle \
    \n4: Pikachu"

botReadyMessage = "Pokebot ready!"

saveFileExistsMessage = "A save file for pokemon Kanto already exists!"

saveFileCreatedMessage = "A save file for pokemon Kanto has been created for you!"

noSavefileMessage = "You do not have a savefile, to create one and begin playing send !ready in the welcome channel!"

chooseValidNumberMessage = "Please enter a valid number for your option!"

invalidSelectionMessage = "Invalid selection, cancelling transaction!"

filledSlotsRequiredMessage = "Slots chosen must be filled!"

swapPartyInvalidSlotsMessage = "Please choose valid slots 1 through 6 that are not equal to each other!"

emptyPartyMessage = f"Your party is empty, please select a starter from the below options:\n"

emptyBoxMessage = "Your box is empty!"

partyOptionsWithStarter = "Please select an option: \
                      \n1: Choose a starter \
                      \n2: Show party \
                      \n3: Swap party order"

partyOptionsWithoutStarter = "Please select an option: \
                      \n1: Show party \
                      \n2: Swap party order"

boxOptions = "Please select an option: \
                      \n1: Show box inventory \
                      \n2: Deposit a pokemon \
                      \n3: Withdraw a pokemon"

boxDepositPromptMessage = "Which pokemon would you like to deposit?\n"

boxDepositConfirmationMessage = "You have deposited "

boxDepositInsufficientPartySizeMessage = "You must have more than one pokemon in your party to make a deposit!"

boxWithdrawPromptMessage = "Which box pokemon would you like to withdraw?\n\n"

boxWithdrawConfirmationMessage = "You have withdrawn "

boxWithdrawInvalidPartySizeMessage = "You cannot withdraw a pokemon with a full party!"

nonFilledSlotBoxMessage = "Please choose an occupied slot!"

timeoutMessage = "Response timeout, cancelling transaction!"

noBadgeMessage = "You do not have any badges!"

starterOptionsMessage = "Please select a starter \
                        \n1: Bulbasaur \
                        \n2: Charmander \
                        \n3: Squirtle \
                        \n4: Pikachu \
                        \nWhen you are ready to select use the command again followed by your selection, ex. (!starter Pikachu)"

"""
Generates a message for new players that have joined the Kanto guild

Args:
    member: the discord member data variable

Returns:
    a message specific to that player welcoming them or indicating that they have already joined
"""
def joinMessage(member):
    return f"Welcome {member.name} to Kanto, type !ready when you would like your pokemon journey to begin!"

"""
Generates a message for when players indicate they are ready in the Welcome channel

Args:
    username (str): the username of the player

Returns:
    A personalized message for players who indicated that they are ready
"""
def playerReadyMessage(username: str):
    message = player.checkForSave(username)
    return f"{message} \
                          \nPokemon Kanto is played by sending me DMs, for help with commands, please type !commands!"

# Dictionary to store who cannot run commands
userCommandPriveledges = {}

commands = f"Commands: \
                        \n!commands: See commands \
                        \n!ready: Begin your pokemon journey (can not be used more than once) \
                        \n!starter: Indicate that you would like to choose your starter pokemon \
                        \n!showParty: View your party \
                        \n!swapParty: Swap 2 party slots (!swapParty slot1 slot2)\
                        \n!box: Start a box transaction \
                        \n!showBadges: Display your badges \
                        \n!showInventory: Display your inventory"

# Acceptable Starters
acceptableStarters = {
    "1": "BULBASAUR", 
    "2": "CHARMANDER", 
    "3": "SQUIRTLE", 
    "4": "PIKACHU"
}


# Used for emptying a pokemon slot
emptyPokemonSlot = {
    "name": "",
    "nickname": "",
    "primary": "",
    "secondary": "",
    "level": 0,
    "moves": [],
    "HealthIV": 0,
    "AttackIV": 0,
    "DefenseIV": 0,
    "SpecialIV": 0,
    "SpeedIV": 0,
    "HealthEV": 0,
    "AttackEV": 0,
    "DefenseEV": 0,
    "SpecialEV": 0,
    "SpeedEV": 0,
    "maxHP": 0,
    "currentHP": 0,
    "Attack": 0,
    "Defense": 0,
    "Sp. Attack": 0,
    "Sp. Defense": 0,
    "Speed": 0
}

boxOptionResponses = {
    "1": "show box inventory",
    "2": "deposit a pokemon",
    "3": "withdraw a pokemon"
}