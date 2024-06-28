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