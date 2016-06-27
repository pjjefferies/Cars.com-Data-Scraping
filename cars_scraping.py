from readURLPage import *
from jsonReadWriteFile import *
from extractCharsFromString import *
import time
import string
import random

    

def findCarsInListPageFile(carListPageFile):     #Find Cars in Car List Page File
    carStartingPointsInList = []
    index = 0
    while True:
        newCarFound = carListPageFile.find('<div class="row vehicle"', index)
        if newCarFound == -1:
            break
        carStartingPointsInList.append(newCarFound)
        index = newCarFound + 25
    index = 0
    while True:
        newCarFound = carListPageFile.find('<div class="row vehicle cpo-listing"', index)
        if newCarFound == -1:
            break
        carStartingPointsInList.append(newCarFound)
        index = newCarFound + 25
    carStartingPointsInList.sort()
    return carStartingPointsInList


def makeListOfCarSectionData(carListPageFile, carStartingPointsInList): #Separate Vehicle sections of file
    carDataTextFromListFile = []
    for carNo in range(len(carStartingPointsInList)-1):
        carDataTextFromListFile.append(carListPageFile[carStartingPointsInList[carNo]:carStartingPointsInList[carNo+1]-1])
    carDataTextFromListFile.append(carListPageFile[carStartingPointsInList[-1]:])
    return carDataTextFromListFile


def tempCarDataFromCarListFile(carDataTextFromListFile):
    tempCarData = {}

    indexBegin = carInfoFromList.find('id="')+4    #Find ID begining string
    if indexBegin == 3:                            #If string isn't found, -1 is returned
        print("No ID found, ignoring CarDataSection in List File")
        raise ValueError
        return
    else:
        indexEnd = carInfoFromList.find('"', indexBegin+1) #Find feature end string
        tempCarData["ID"] = extractCharsFromString(carInfoFromList[indexBegin:indexEnd],
                                                   string.digits)

    intFeatureToFind = [["Mileage", '"milesSort"', "<", 12],     #string to search for begin, end, begin offset
                        ["Seller Distance", '"seller-distance muted locationSort"', "<", 37],
                        ["Price", '"price"', ",", 8]]

    for feature in intFeatureToFind:            #Get Data in List above as ints
        indexBegin = carInfoFromList.find(feature[1])+feature[3]    #Find feature begining string
        if indexBegin == feature[3] - 1:                            #If string isn't found, -1 is returned
            continue
        indexEnd   = carInfoFromList.find(feature[2], indexBegin+1) #Find feature end string
        tempValueAsString = extractCharsFromString(carInfoFromList[indexBegin:indexEnd],
                                                   string.digits)
        try:
            tempCarData[feature[0]] = int(tempValueAsString)
        except ValueError:
            tempCarData[feature[0]] = 0
#        print(feature[0],
#              type(extractCharsFromString(carInfoFromList[indexBegin:indexEnd],string.digits)),
#              extractCharsFromString(carInfoFromList[indexBegin:indexEnd],string.digits))

    featureToFind = [["Stock Type", '"stockType"', '"'  , 13],  #string to search for begin, end, begin offset
                     ["Seller ID", '"sellerID"', ",", 12],
                     ["Exterior Color", '"exteriorColorSort"', "<", 20],
                     ["Drive Train", '"driveTrainSort"', "<", 17],
                     ["Engine", '"engineDescriptionSort"', "<", 24],
                     ["Seller", '"sellerNameSort"', "<", 17],
                     ["Link", 'href="/vehicledetail/detail/', ">", 6]]

    for feature in featureToFind:               #Get Data in List above
        indexBegin = carInfoFromList.find(feature[1])+feature[3]    #Find feature begining string
        if indexBegin == feature[3] - 1:                            #If string isn't found, -1 is returned
            continue
        indexEnd   = carInfoFromList.find(feature[2], indexBegin+1) #Find feature end string
        tempCarData[feature[0]] = carInfoFromList[indexBegin:indexEnd]
    indexBegin = carInfoFromList.find('href="/vehicledetail/detail/') + 6
    indexEnd   = carInfoFromList.find('"', indexBegin+1)
    tempCarData["Link"] = "http://www.cars.com" + carInfoFromList[indexBegin:indexEnd]
    return tempCarData


def scrapeIndividualCarWebPage(carPageFile):
    tempIndiCarData = {}
    if 'Vehicle Not Found' in carPageFile:
        #print("Vehicle Not found", carPageFile[0:500])
        tempIndiCarData["Active"] = False
        return tempIndiCarData
    else:
        #print("Vehicle Found")
        tempIndiCarData["Active"] = True
    intFeatureToFind = [["Mileage", '<li><strong>Mileage</strong></li>', "</li>", 53],  #string to search for begin, end, begin offset
                        ["Price", '<span class="vehicle-price">', "</span>", 13],
                        ["Model Year", 'data-year="', '" ', 11]]
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


    

"""
def mergeCarData(carDataMain, carDataNew):
    for feature in iter(carDataNew):
        if type(carDataNew[feature]) == str:
            if carDataNew[feature] != "":
                carDataMain[feature] = carDataNew[feature]
        elif type (carDataNew[feature]) == int:
            if carDataNew[feature] != 0:
                carDataMain[feature] = carDataNew[feature]
    return carDataMain
"""

if __name__ == '__main__':
    #loadFileLocation = "Local"      #choose 1
    loadFileLocation = "Online"
    #loadFileLocation = "None"
    
    databaseFile = "Cars_For_Sale_Database.json"

    maxCarPagesToLoad = 60               #Limit page loads during testing
    avgCarPageLoadDelay = 10            #delay an average of 10 seconds between page load. Also add variability

    try:                                            #Load local car database
        listOfCarData = load_json(databaseFile)
    except (OSError, ValueError):
        print("No good json file found, creating empty car databse")
        listOfCarData = {}          #Main list of car data as dictionary (by ID) of dictionaries (by data type)
        startNoCars = 0
    else:
        startNoCars = len(listOfCarData)
        print("Found json file and loaded into 'listOfCarData' with", startNoCars, "car entries.")

    if loadFileLocation == "Local":                 #Load www.cars.com list of cars for sale webpage
        carListURL = "file:///C:/Users/PaulJ/Data/Computers & Internet/Python/Cars Data Scraping/Car List Page for Practice.htm"
    elif loadFileLocation == "Online":
        carListURL = "http://www.cars.com/for-sale/searchresults.action?AmbMkNm=Volkswagen&AmbMdNm=Touareg&AmbMkId=20089&AmbMdId=22189&searchSource=ADVANCED_SEARCH&rd=100000&zc=48105&uncpo=2&stkTyp=U&mdId=22189&alMkId=20089&yrMn=2012&yrMx=2013&fuelTypeId=31766&rpp=250"
        carListURL = "http://www.cars.com/for-sale/searchresults.action?feedSegId=28705&isDealerGrouping=false&rpp=250&sf1Dir=ASC&sf1Nm=price&sf2Dir=DESC&sf2Nm=miles&zc=48105&rd=500&stkTypId=28881&mkId=20089&mdId=22189&mdId=22281&mdId=22189&clrId=27123&clrId=27124&clrId=27127&clrId=27128&clrId=27132&clrId=27133&clrId=27123&drvTrnId=27105&drvTrnId=27102&drvTrnId=27105&kw=navigation%20camera&yrId=39723&yrId=47272&yrId=39723&searchSource=GN_REFINEMENT"
    elif loadFileLocation == "None":
        carListURL = ""

    if carListURL != "":
        carListPageFile = get_page(carListURL)      #Load URL from above
        carStartingPointsInList = findCarsInListPageFile(carListPageFile)   #Find starting points of individual car data
        carDataTextFromListFile = makeListOfCarSectionData(carListPageFile, carStartingPointsInList)
                                                    #Make list of text section for each car
        for carInfoFromList in carDataTextFromListFile:         #For each car summary section in car list, get data
            try:
                tempCarData = tempCarDataFromCarListFile(carDataTextFromListFile)
            except ValueError:
                pass
            if tempCarData["ID"] not in listOfCarData:
                #print("Adding new car with ID", tempCarData["ID"], listOfCarData.keys())
                listOfCarData[tempCarData["ID"]] = tempCarData  #If ID is not in list add to list
            else:
                tempCarDataFromDatabase = listOfCarData[tempCarData["ID"]] #If ID is in list, add/replace any fields that were read-in with values
                #print("Merging data for car with ID", tempCarData["ID"])
                #listOfCarData[tempCarData["ID"]] = mergeCarData(listOfCarData[tempCarData["ID"]], tempCarData)
                
                listOfCarData[tempCarData["ID"]].update(tempCarData)

    endNoCars = len(listOfCarData)
    print("Start No. Cars:", startNoCars,
          "\n  End No. Cars:", endNoCars,
          "\n    Cars added:", endNoCars - startNoCars)

    
    counter = 0                     #Get Individual Car Pages
    print("Reading",maxCarPagesToLoad,"individual car page(s) at an average rate of 1 page every", avgCarPageLoadDelay,
          "seconds.")
    for car in iter(listOfCarData):
        tempCarData = listOfCarData[car]
        if listOfCarData[car].get("Active", True) == False:
            print(car, "car not active, skipping")
            continue
        #if "pageFile" in listOfCarData[car]:        #Don't get pages that I already have
        #    continue
        if listOfCarData[car].get("scraped", False):       #Only scape pagefile if haven't already
            print(car, "car already scraped, skipping")
            continue
        if listOfCarData[car].get("pageFile", "") == "":
            print("Getting individual page for Car ID", car)
            tempCarData["pageFile"] = get_page(tempCarData["Link"])
            counter += 1
            delay = avgCarPageLoadDelay + avgCarPageLoadDelay*(random.random()-0.5)
            print("{:.2f} seconds delay".format(delay))
            time.sleep(delay)
        print("Scaping page for car ID", car)
        tempIndividualCarData = scrapeIndividualCarWebPage(tempCarData["pageFile"])
        tempCarData.update(tempIndividualCarData)       #Add data scraped from individual car page to main temp dict
        listOfCarData[car] = tempCarData                #Save temporary separate car dict back to main database dictionary
        print("Read", str(counter), "of (" + str(len(listOfCarData)) + "/" + str(maxCarPagesToLoad) +
              "/" + str(endNoCars - startNoCars) + ") to load")
        if counter >= maxCarPagesToLoad:    #limit number of pages to check
            print("reached maximum pages to load, stopping")
            break
    try:
        write_json(databaseFile, listOfCarData)
    except OSError:
        print("Unable to write local databasefile")
