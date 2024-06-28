def parseDict(dictionary: dict):
    parsedDict = ""
    for key, value in dictionary.items():
        parsedDict += f"{key.capitalize()}: {value}\n"
    return parsedDict

def parseList(list):
    parsedList = ""
    for item in list:
        parsedList += f"{item.capitalize()}\n"
    return parsedList