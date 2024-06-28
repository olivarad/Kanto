import re

"""
Parse a file to find all discord bot commands

Args:
    filePath: the bot file containing commands

Returns: a list of commands
"""
def findCommands(botFile):
    # regex pattern for finding names of commands in python discord bots
    commandPattern = re.compile(r'@bot\.command\(\)\n\s*async\s+def\s+(\w+)\s*\(.*\):')

    commandNames = []

    # read the botFile into a string
    with open(botFile, 'r') as file:
        data = file.read()

        # preforming regex
        matches = commandPattern.finditer(data)
        
        for match in matches:
            commandNames.append(match.group(1))

    return commandNames

"""
Check if definitions for commands exist

Args:
    botFile: the bot file containing commands
    definitionsFile: the definitions file containing definitions of commands
"""
def checkCommandDefinitionExistence(botFile, definitionsFile):
    commands = findCommands(botFile)

    # read in the definitions file
    with open(definitionsFile, 'r') as file:
        definitions = file.read()

    for command in commands:
        if command not in definitions:
            return 1  # Return non-zero if any command is missing

    return 0  # Return 0 if all command are found

botFile = '../source/profOak.py'
definitionsFile = '../source/definitions.py'

exit_code = checkCommandDefinitionExistence(botFile, definitionsFile)
exit(exit_code)
