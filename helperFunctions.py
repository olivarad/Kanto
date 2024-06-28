def parseDict(dictionary: dict):
    parsedDict = ""
    for key, value in dictionary.items():
        parsedDict += f"{key.capitalize()}: {value}\n"
    return parsedDict