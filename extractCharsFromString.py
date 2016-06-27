def extractCharsFromString(aString, characters):
    tempString = ""
    for char in aString:
        if char in characters:
            tempString += char
    return tempString
