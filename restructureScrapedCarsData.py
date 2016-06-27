from jsonReadWriteFile import *

def restructureScrapedCarsData(jsonCarsDatabase):
    try:
        listOfCarData = load_json(jsonCarsDatabase)
    except FileNotFoundError:
        print("No good json file found, please drive through")
        raise FileNotFoundError
        return        
    except ValueError:
        print("JSON file found with no good values, please drive through")
        raise ValueError
        return
    except OSError:
        print("No good json file found, please drive through - OS Error")
        raise OSError
        return
    else:
        noCars = len(listOfCarData)
        print("Found json file and loaded into 'listOfCarData' with", noCars, "car entries.")

    structuredCarData = {}

    tempCarIDList = []
    tempPriceList = []
    tempMilesList = []
    tempMYearList = []
    tempActivList = []
    tempNavigList = []
    tempCamerList = []
    tempSellDList = []
    tempVINNoList = []
    tempFuelTList = []
    
    for car in listOfCarData:
        tempCarIDList.append(listOfCarData[car].get("ID", ""))
        tempPriceList.append(listOfCarData[car].get("Price", 0))
        tempMilesList.append(listOfCarData[car].get("Mileage", 0))
        tempMYearList.append(listOfCarData[car].get("Model Year", 0))
        tempActivList.append(listOfCarData[car].get("Active", ""))
        tempSellDList.append(listOfCarData[car].get("Seller Distance", 999))
        tempVINNoList.append(listOfCarData[car].get("VIN", ""))
        tempFuelTList.append(listOfCarData[car].get("Fuel", ""))
        equipList = listOfCarData[car].get("Equipment List", [])
        equipList += listOfCarData[car].get("Features List", [])
        tempNavigEntry = False
        tempCamerEntry = False
        for equip in equipList:
            if "navigation" in equip.lower():
                tempNavigEntry = True
            if "camera" in equip.lower():
                tempCamerEntry = True
        tempNavigList.append(tempNavigEntry)
        tempCamerList.append(tempCamerEntry)
    structuredCarData["ID"] = tempCarIDList
    structuredCarData["Price"] = tempPriceList
    structuredCarData["Mileage"] = tempMilesList
    structuredCarData["Model Year"] = tempMYearList
    structuredCarData["Active"] = tempActivList
    structuredCarData["Seller Distance"] = tempSellDList
    structuredCarData["VIN"] = tempVINNoList
    structuredCarData["Navigation"] = tempNavigList
    structuredCarData["Camera"] = tempCamerList
    structuredCarData["Fuel"] = tempFuelTList
    return structuredCarData


def dictToMatrix(aDict):
    tempKeyList = sorted(list(aDict.keys()))
    tempMatrix = []
    for item in tempKeyList:
        tempMatrix.append(aDict[item])
    matrix = [tempKeyList] + tempMatrix
    return matrix



if __name__ == '__main__':
    from jsonReadWriteFile import *
    databaseFile = "Cars_For_Sale_Database.json"
    listDatabaseFile = "Data_Lists_For_Car_Sales.json"

    try:
        structuredListOfCarData = restructureScrapedCarsData(databaseFile)
    except (FileNotFoundError, ValueError, OSError):
        print("Exception returned")

    write_json(listDatabaseFile, structuredListOfCarData)    

    structuredMatrixOfCarData = dictToMatrix(structuredListOfCarData)

    
