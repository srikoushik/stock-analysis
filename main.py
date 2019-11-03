
import csv
import sys
import math
from dateutil.parser import parse
from datetime import datetime
from itertools import combinations
from fuzzywuzzy import process

from inputs import Inputs
from csvData import CSVData

inputs = Inputs()
csvData = CSVData()


def main():
    # Check CSV arguement is present
    if len(sys.argv) > 1 and sys.argv[1]:
        inputs.filePath = sys.argv[1]

        # process CSV and save as data class
        processCsvIntoDataClass()

        getTheStockName()
    else:
        print("Error: Load the CSV file.")


def continueInputAfterName():
    getTheStartDate()
    getTheEndDate()
    calculateResult()
    doYouWantToContinue()


def validateDate(enteredDate):
    result = None
    error = None
    try:
        result = datetime.strptime(enteredDate, "%d-%b-%Y")
    except ValueError:
        error = "Error: Enter a valid date. Eg: 19-Apr-2019"

    return error, result


def getTheStockName():
    inputs.stockName = input(
        "\nWelcome ! Enter the stock you need to analyse: ").lower()

    if inputs.stockName.isalpha():
        # Validate whether the startDate exists in CSV
        matched = isAValidStock()
        if matched:
            continueInputAfterName()
        else:
            nearestMatch = process.extract(
                inputs.stockName, csvData.getStockNamesArray())
            if nearestMatch and nearestMatch[0]:
                userInput = input("Oops! Do you mean %s? (y or n): " %
                                  (nearestMatch[0][0])).lower()
                if userInput == "y" or userInput == "yes":
                    inputs.stockName = nearestMatch[0][0]
                    continueInputAfterName()
                else:
                    doYouWantToContinue()
            else:
                print("Message: The entered stock do not have insights.")
                doYouWantToContinue()
    else:
        print("Error: Stock Name must be in characters.")
        doYouWantToContinue()


def doYouWantToContinue():
    userInput = input(
        "\nDo you want to analyse another stock? (y or n): ").lower()
    if userInput == "y" or userInput == "yes":
        inputs.resetInputData()
        getTheStockName()
    else:
        inputs.resetInputData()


def getTheStartDate():
    error, result = validateDate(input("\nEnter the Start Date: "))
    if not error:
        inputs.startDate = result
    else:
        print(error)
        getTheStartDate()


def getTheEndDate():
    error, result = validateDate(
        input("\nTill which date you want to analyse: "))
    if not error:
        if result > inputs.startDate:
            inputs.endDate = result
        else:
            print("Error: End date must be greater than start date.")
            getTheEndDate()
    else:
        print(error)
        getTheEndDate()


def calculateResult():
    mean, variance, combinationData = calculateMeanAndVariance()
    standardDeviation = calculateStandardDeviation(variance)
    bestBuyAndSellDate = getBestBuyAndSellDate(combinationData)

    print("\nYour Insights:")
    print("\nMean: ", mean)
    print("\nStandard Deviation: ", standardDeviation)

    sortedDifference = sorted(
        bestBuyAndSellDate, key=lambda x: x["difference"], reverse=True)
    if sortedDifference and sortedDifference[0]:
        topResult = sortedDifference[0]
        if topResult["difference"] > 0:
            print("\nBest Buy Date: ", topResult["buyDate"])
            print("\nBest Sell Date: ", topResult["sellDate"])
            print("\nProfit for 100 uints: ", topResult["difference"] * 100)
        else:
            print("\nMessage: No Profit for the stock in the selected date range.")


def calculateMeanAndVariance():
    dataForEnteredStockName = csvData.getNameKeyAsData().get(inputs.stockName)
    previousPriceForStartDate = 0
    previousPriceForEndDate = 0
    variance = 0
    fullDataObjectForEnteredDate = []
    mean = 0
    combinationOfData = []

    # If exact date matched get that or get the nearest least and get that price
    startDate = inputs.startDate
    stockDataForStockName = dataForEnteredStockName.get("data")

    if not stockDataForStockName.get(inputs.startDate):
        # Check for the nearest previous start date or through the error
        # filter and sort the dates
        filteredDateBelowStartRange = list(filter(
            lambda x: x < inputs.startDate, dataForEnteredStockName.get("dates")))

        sortedFilteredDates = sorted(
            filteredDateBelowStartRange, key=lambda x: x, reverse=True)

        if sortedFilteredDates:
            # Get the price of this and save for inputs.startDate
            previousPriceForStartDate = dataForEnteredStockName.get(
                "data").get(sortedFilteredDates[0])
        else:
            print("\nMessage: Data for requested start date is not available.")
            exit(0)

    endDate = inputs.endDate

    if not stockDataForStockName.get(inputs.endDate):
        # Check for the the nearest previous end date which is greater than start date or through the error
        filteredDateAfterStartRange = list(filter(
            lambda x: x > inputs.startDate and x <= inputs.endDate, dataForEnteredStockName.get("dates")))

        sortedFilteredDatesAfterStartRange = sorted(
            filteredDateAfterStartRange, key=lambda x: x, reverse=True
        )

        if sortedFilteredDatesAfterStartRange:
            previousPriceForEndDate = dataForEnteredStockName.get(
                "data").get(sortedFilteredDatesAfterStartRange[0])
        else:
            print("\nMessage: Data for requested end date is not available.")
            exit(0)

    dataForEnteredDateRange = list(filter(
        lambda x: ((x >= startDate) and (x <= endDate)), dataForEnteredStockName.get("dates")))

    if dataForEnteredDateRange:
        sumOfPrices = 0
        data = dataForEnteredStockName.get("data")

        for dateObject in dataForEnteredDateRange:
            price = data.get(dateObject)

            if dateObject == inputs.startDate and not data.get(dateObject):
                price = previousPriceForStartDate
            elif dateObject == inputs.endDate and not data.get(dateObject):
                price = previousPriceForEndDate

            sumOfPrices += float(price)

            record = dict({
                "date": dateObject,
                "price": float(price)
            })
            fullDataObjectForEnteredDate.append(record)

        # TODO: Handle 0 division error when all prices are 0
        mean = sumOfPrices/len(dataForEnteredDateRange)

        combinationOfData = list(combinations(fullDataObjectForEnteredDate, 2))

        # find the variance
        squareOfMeanMinusPrice = 0

        for dateObject in dataForEnteredDateRange:
            meanMinusPrice = mean - float(data.get(dateObject))
            squareOfMeanMinusPrice += (meanMinusPrice * meanMinusPrice)

        # TODO: Handle 0 division error when all prices are 0
        variance = squareOfMeanMinusPrice/len(dataForEnteredDateRange)

    return mean, variance, combinationOfData


def calculateStandardDeviation(variance):
    # Square root of variance
    standardDeviation = math.sqrt(variance)

    return standardDeviation


def getBestBuyAndSellDate(combinationOfData):
    combinationOfDataAfterPriceDifference = []

    for item in combinationOfData:
        differenceValue = 0

        if item[0]["price"] < item[1]["price"]:
            differenceValue = abs(
                float(item[0]["price"]) - float(item[1]["price"]))
        else:
            differenceValue = - \
                abs(float(item[0]["price"]) - float(item[1]["price"]))

        record = dict({
            "difference": differenceValue,
            "buyDate": item[0]["date"],
            "sellDate": item[1]["date"]
        })
        combinationOfDataAfterPriceDifference.append(record)

    return combinationOfDataAfterPriceDifference


def processCsvIntoDataClass():
    NameKeyAsData = {}
    stockNames = []

    with open(inputs.filePath) as csv_file:
        csv_reader = csv.reader(csv_file)
        """
            "ITC": {
                dates: [],
                data: {
                    "date": "price"
                }
            }
        """
        for row in csv_reader:
            if row[0].lower() in NameKeyAsData.keys():
                NameKeyAsData[row[0].lower()]["dates"].append(parse(row[1]))
                NameKeyAsData[row[0].lower()]["data"][parse(row[1])] = row[2]
            else:
                NameKeyAsData[row[0].lower()] = {
                    "dates": [parse(row[1])],
                    "data": {
                        parse(row[1]): row[2]
                    }
                }

            # This is used for showing the suggestion of stockName
            if row[0].lower() not in stockNames:
                stockNames.append(row[0].lower())

    csvData.setNameKeyAsData(NameKeyAsData)
    csvData.setStockNamesArray(stockNames)


def isAValidStock():
    matched = False
    for stockName in csvData.getNameKeyAsData():
        if stockName == inputs.stockName:
            matched = True

    return matched


main()
