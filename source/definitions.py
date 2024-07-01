commands = f"Commands: \
                        \n!commands: See commands \
                        \n!ready: Begin your pokemon journey (can not be used more than once) \
                        \n!starter: Indicate that you would like to choose your starter pokemon \
                        \n!showParty: View your party \
                        \n!swapParty: Swap 2 party slots (!swapParty slot1 slot2)\
                        \n!box: Start a box transaction \
                        \n!showBadges: Display your badges \
                        \n!showInventory: Display your inventory"

boxOptions = f"Please select an option: \
                      \n1: Show box inventory \
                      \n2: Deposit a pokemon \
                      \n3: Withdraw a pokemon"

boxOptionResponses = {
    "1": "show box inventory",
    "2": "deposit a pokemon",
    "3": "withdraw a pokemon"

}

# Dictionary to store who cannot run commands
userCommandPriveledges = {}

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

noSavefileMessage = "You do not have a savefile, to create one and begin playing send !ready in the welcome channel"

emptyBoxMessage = "Your box is empty"

timeoutMessage = "Response timeout, cancelling transaction"