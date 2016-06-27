import urllib.request
import time
import json
import string


def get_page(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101'
    headers = {'User-Agent' : user_agent}
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)
    f = urllib.request.urlopen(req)
    pageFile = f.read().decode('utf-8')
    f.close()
    return pageFile


def extractCharsFromString(aString, characters):
    tempString = ""
    for char in aString:
        if char in characters:
            tempString += char
    return tempString


def write_json(databaseFile, listOfCarData): #Write locally saved vehicles
    try:
        f = open(databaseFile, "w")
        jsonCarData = json.dumps(listOfCarData, indent="\t", sort_keys=True)
        f.write(jsonCarData)
        f.close()
        return
    except OSError:
        return
    

def scrapeIndividualCarWebPage(carPageFile):
    tempIndiCarData = {}
    if 'Vehicle Not Found' in carPageFile:
        print("Vehicle Not found", carPageFile[0:500])
        tempIndiCarData["Active"] = "False"
        return tempIndiCarData
    else:
        print("Vehicle Found")
        tempIndiCarData["Active"] = "True"
    intFeatureToFind = [["Mileage", '<li><strong>Mileage</strong></li>', "</li>", 53],  #string to search for begin, end, begin offset
                        ["Price", '<span class="vehicle-price">', "</span>", 13]]
    featureToFind = [["Exterior Color", '<li><strong>Exterior Color</strong></li>', "</li>", 60],   #string to search for begin, end, begin offset
                     ["Interior Color", '<li><strong>Interior Color</strong></li>', "</li>", 60],
                     ["VIN", '<li><strong>VIN</strong></li>', "</li>", 49],
                     ["Fuel", '<li><strong>Fuel</strong></li>', "</li>"  , 50],
                     ["Body Style", '<li><strong>Body Style</strong></li>', "</li>", 56],
                     ["Fuel", "<li><strong>Fuel</strong></li>", "</li>", 50],
                     ["Drive Train", '<li><strong>Drivetrain</strong></li>', "</li>", 56],
                     ["Engine", '<li><strong>Engine</strong></li>', "</li>", 52]]

    for feature in intFeatureToFind:            #Get Data in List above as ints
        indexBegin = carPageFile.find(feature[1])+feature[3]    #Find feature begining string
        if indexBegin == feature[3] - 1:                            #If string isn't found, -1 is returned
            continue
        indexEnd   = carPageFile.find(feature[2], indexBegin+1) #Find feature end string
        tempValueAsString = extractCharsFromString(carPageFile[indexBegin:indexEnd],
                                                   string.digits)
        try:
            tempIndiCarData[feature[0]] = int(tempValueAsString)
        except ValueError:
            tempCarData[feature[0]] = 0

    for feature in featureToFind:            #Get Data in List above as ints
        indexBegin = carPageFile.find(feature[1])+feature[3]    #Find feature begining string
        if indexBegin == feature[3] - 1:                            #If string isn't found, -1 is returned
            continue
        indexEnd   = carPageFile.find(feature[2], indexBegin+1) #Find feature end string
        tempIndiCarData[feature[0]] = carPageFile[indexBegin:indexEnd]

    equipmentList = []
    equipListStartArea = carPageFile.find('<ul class="st-equipment list">') + 43
    fileIndex = equipListStartArea
    endOfEquipList = carPageFile.find("</span>", fileIndex)
    while True:
        itemStart = carPageFile.find("<li>", fileIndex)
        if itemStart == -1 or itemStart > endOfEquipList:
            break
        itemEnd = carPageFile.find("</li>", itemStart)
        equipmentList.append(carPageFile[itemStart:itemEnd])
        fileIndex = itemEnd + 5
    tempIndiCarData["Equipment List"] = equipmentList

    featuresList = []
    featureListStartArea = carPageFile.find('<ul class="features list">') + 39
    fileIndex = featureListStartArea
    endOfFeatureList = carPageFile.find("</span>", fileIndex)
    while True:
        itemStart = carPageFile.find("<li>", fileIndex)
        if itemStart == -1 or itemStart > endOfFeatureList:
            break
        itemEnd = carPageFile.find("</li>", itemStart)
        featuresList.append(carPageFile[itemStart:itemEnd])
        fileIndex = itemEnd + 5
    tempIndiCarData["Features List"] = featuresList
    return tempIndiCarData

listOfCarData = {}
carPageFile1 = get_page("file:///C:/Users/PaulJ/Data/Computers & Internet/Python/Cars Data Scraping/Car Detail Page for Practice.htm")
print(len(carPageFile1))
tempCarData1 = {}
tempCarData1["pageFile"] = carPageFile1           #ADD TO THIS WITH SCRAPING FUNCTION
tempIndividualCarData = scrapeIndividualCarWebPage(carPageFile1)
tempCarData1.update(tempIndividualCarData)
listOfCarData["car1"] = tempCarData1


carPageFile2 = get_page("file:///C:/Users/PaulJ/Data/Computers & Internet/Python/Cars Data Scraping/Car No Longer For Sale or Bad Number Detail Page for Practice.htm")
print(len(carPageFile2))
tempCarData2 = {}
tempCarData2["pageFile"] = carPageFile2           #ADD TO THIS WITH SCRAPING FUNCTION
tempIndividualCarData2 = scrapeIndividualCarWebPage(carPageFile2)
tempCarData2.update(tempIndividualCarData2)
listOfCarData["car2"] = tempCarData2

databaseFile = databaseFile = "Single_Car_For_Sale_Database.json"
try:
    write_json(databaseFile, listOfCarData)
except OSError:
    print("Unable to write local databasefile")
