
#mainDictOfList is dictionary of named lists
#filterList is a list of filters
#filtes are lists of:
#   - list name
#   - first filter parameter - equality if only one, min if two
#   - second filter parameter - max if exists

from jsonReadWriteFile import *
from restructureScrapedCarsData import *



def filterListData(carDataMatrix, includeList, filterList):
    keepItem = [True]*len(carDataMatrix[1])
    for afilter in filterList:              #Apply Filters
        if afilter[0] not in carDataMatrix[0]:
            print("Skipping filter not matching item in list:", afilter)
            continue
        index = carDataMatrix[0].index(afilter[0]) + 1
        tempTempMatrix = []
        for i in range(len(carDataMatrix)-1):
            tempTempMatrix.append([])
        tempMatrix = [carDataMatrix[0]] + tempTempMatrix
        
        if len(afilter) == 2:
            for listItem in range(len(carDataMatrix[1])):
                if carDataMatrix[index][listItem] != afilter[1]:
                    keepItem[listItem] = False
        elif len(afilter) == 3:
            for listItem in range(len(carDataMatrix[1])):
                if (carDataMatrix[index][listItem] < afilter[1] or
                    carDataMatrix[index][listItem] > afilter[2]):
                    keepItem[listItem] = False
        else:
            print("Ignoring filter:", afilter)
            pass    #if not 2 or 3, ignore filter

    for charNo in range(1, (len(carDataMatrix[0])+1)):
        for listItem in range(len(carDataMatrix[1])):
            if keepItem[listItem]:
                tempMatrix[charNo].append(carDataMatrix[charNo][listItem])

    newTempMatrix = [[]]
    for charName in tempMatrix[0]:
        if charName in includeList:
            newTempMatrix[0].append(charName)
            index = carDataMatrix[0].index(charName) + 1
            newTempMatrix.append(tempMatrix[index])

    return newTempMatrix        


def separateListByChar(carDataMatrix, charToSep):
    if charToSep not in carDataMatrix[0]:
        print("Separator", charToSep, "not found in carDataMatrix keys:", carDataMatrix[0])
        return []
    listOfUniqueSepChar = []
    index = carDataMatrix[0].index(charToSep) + 1
    #print("index:", index)
    for listItem in range(len(carDataMatrix[index])):
        if carDataMatrix[index][listItem] not in listOfUniqueSepChar:
            listOfUniqueSepChar.append(carDataMatrix[index][listItem])
    #print("listOfUniqueSepChar:", listOfUniqueSepChar)
    #now have list of unique separators, create matrix for each one
    dictByUniqueSep = {}
    for uniqueSepChar in listOfUniqueSepChar:
        tempTempMatrix = []
        for i in range(len(carDataMatrix)-1):
            tempTempMatrix.append([])
        tempMatrix = [carDataMatrix[0]] + tempTempMatrix
        for listItem in range(len(carDataMatrix[1])):
            if carDataMatrix[index][listItem] == uniqueSepChar:
                for charNo in range(1,len(carDataMatrix[0])+1):
                    tempMatrix[charNo].append(carDataMatrix[charNo][listItem])
        #print("uniqueSepChar:", uniqueSepChar, "\n\ntempMatrix:", tempMatrix)
        dictByUniqueSep[uniqueSepChar] = tempMatrix
    #print("dictByUniqueSep:", dictByUniqueSep)
    return dictByUniqueSep



if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab

    databaseFile = "Cars_For_Sale_Database.json"
    listDatabaseFile = "Data_Lists_For_Car_Sales.json"

    try:
        structuredListOfCarData = restructureScrapedCarsData(databaseFile)
    except (FileNotFoundError, ValueError, OSError):
        print("Exception returned")

    structuredMatrixOfCarData = dictToMatrix(structuredListOfCarData)
    #print(structuredMatrixOfCarData[:5])
    
    reducedStructMatrixOfCarData = filterListData(structuredMatrixOfCarData,
                                                 ['Price',
                                                  'Mileage', 'Model Year',
                                                  'Fuel', 'ID', 'VIN'],
                                                 [['Price', 30000, 32000],
                                                  #['Model Year', 2000, 2016],
                                                  ['Model Year', 2012, 2012],
                                                  ['Mileage', 29000, 33000]])
                                                  
    #print("reducedStuctMatrixOfCarData:", reducedStructMatrixOfCarData)

    #newDictByModelYear = separateListByChar(reducedStructMatrixOfCarData, "Model Year")
    newDictByModelYear = separateListByChar(reducedStructMatrixOfCarData, "Fuel")

    #print("\n\n\nnewDictByModelYear:", newDictByModelYear)

    plt.figure(1) # make figure 1 the current figure
    plt.axis([0, 100000, 0, 60000])
    plt.grid(b='on', which='major', axis='both', alpha=0.5, animated=True,
             color='blue', linestyle='-.', linewidth=0.75)
    x0 = np.array(range(0,100000,5000))
    fitArray = {}
    fitString = {}
    initFitTextLoc = 0.33
    fitTextInc = -0.095
    initFormat = ['bx', 'b--']
    #for year in iter(newDictByModelYear):
    for year in iter(newDictByModelYear):   #acutally year = fuel in this case, need to re-do to make more general
        mileageIndex = newDictByModelYear[year][0].index('Mileage') + 1
        priceIndex = newDictByModelYear[year][0].index('Price') + 1
        plt.plot(newDictByModelYear[year][mileageIndex], newDictByModelYear[year][priceIndex], initFormat[0], label=str(year)) # draw on figure 1
        #plt.plot(newDictByModelYear[2012][1], newDictByModelYear[2012][3], 'bx', label='2012') # draw on figure 1
        #plt.plot(newDictByModelYear[2013][1], newDictByModelYear[2013][3], 'r+', label='2013') # draw on figure 1

        #fitArray = np.polyfit(newDictByModelYear[year][mileageIndex], newDictByModelYear[year][priceIndex], 2, full=False)
        fitArray = np.polyfit(newDictByModelYear[year][mileageIndex], newDictByModelYear[year][priceIndex], 1, full=False)

        #fitString = "P = {:+.2e} x M^2 {:+.3f} x M {:+.0f}".format(fitArray[0],fitArray[1],fitArray[2])
        fitString = "P = {:+.3f} x M {:+.0f}".format(fitArray[0],fitArray[1])

        plt.figtext(0.34, initFitTextLoc, fitString, size="small")
        initFitTextLoc += fitTextInc
        #plt.figtext(0.34, 0.186, fitString1, size="small")
        #plt.figtext(0.34, 0.138, fitString2, size="small")
        #print(fitArray1, "\n\n", fitArray2)

        #y0 = fitArray[0] * x0**2.0 + fitArray[1] * x0**1.0 + fitArray[2]
        y0 = fitArray[0] * x0**1.0 + fitArray[1]
        
        plt.plot(x0, y0, initFormat[1], label=str(year)+' Fit')
        #print("x0:",x0)
        #y02 = fitArray2[0] * x0**2.0 + fitArray2[1] * x0**1.0 + fitArray2[2]
        #print("y02:", y02)
        if initFormat[0] == 'bx':
            initFormat = ['r+', 'r--']
        elif initFormat[0] == 'r+':
            initFormat = ['go', 'g--']
        else:
            initFormat = ['oo', 'o--']
        #plt.plot(x0, y02, 'r--', label='2013 Fit')
    plt.legend(loc=3, frameon=True, fancybox=True, shadow=True, numpoints=1)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', direction='inout')
    plt.tick_params(axis='both', which='minor', direction='in')
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    plt.title(r'Car Prices by Miles')
    plt.show() # show figure on screen
"""
    plt.figure(2)
    plt.axis([0, 100000, 0, 15])
    n1, bins1, patches1 = plt.hist(newDictByModelYear[2012][1])
    mu1 = np.mean(newDictByModelYear[2012][1])
    sigma1 = np.std(newDictByModelYear[2012][1])
    y1 = mlab.normpdf(bins1, mu1, sigma1) * (1.1 / 2.0688267e-6)
    #print(bins1, "\n\n", y1)
    plt.plot(bins1, y1, 'r--')
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', direction='inout')
    plt.tick_params(axis='both', which='minor', direction='in')
    plt.xlabel('Mileage')
    plt.ylabel('Probability')
    plt.title(r'Histogram Car Mileage: $\mu=$'+str(int(mu1))+', $\sigma=$'+str(int(sigma1)))
    #plt.show()

    plt.figure(3)
    plt.axis([0, 50000, 0, 15])
    plt.hist(newDictByModelYear[2012][3])
    n2, bins2, patches2 = plt.hist(newDictByModelYear[2012][3])
    mu2 = np.mean(newDictByModelYear[2012][3])
    sigma2 = np.std(newDictByModelYear[2012][3])
    y2 = mlab.normpdf(bins2, mu2, sigma2) * (0.3 * 1.3 / 3e-6)
    plt.plot(bins2, y2, 'r--')
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', direction='inout')
    plt.tick_params(axis='both', which='minor', direction='in')
    plt.xlabel('Price')
    plt.ylabel('Probability')
    plt.title(r'Histogram Car Prices: $\mu=$'+str(int(mu2))+', $\sigma=$'+str(int(sigma2)))
    #plt.show()
"""
