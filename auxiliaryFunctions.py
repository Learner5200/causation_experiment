import random

def listmaker(csvFile):
    # Creates from a csv file a list of lists (i.e. a list of rows) for easier reading and manipulation
    data = open(csvFile, 'a+')  # Opening in 'a+' move allows both reading and creation of new csvFile
    data.seek(0)  # Reads from beginning of file
    allLines = data.readlines()
    for index in range(0,len(allLines)):
        allLines[index] = allLines[index].split(',')
    data.close()
    return allLines

def chooseRandom(list):
    index = random.randint(0, len(list) - 1)
    return list[index]

def initialise(csvFile, fieldList):
    # Creates csv file if needed, and assigns participant ID
    dataList = listmaker(csvFile)
    if dataList == [] or dataList[-1][0] == fieldList[0]:
        # Adds the header to new (i.e. empty) file
        data = open(csvFile, 'w')
        data.write(','.join(fieldList) + '\n')
        data.close()
        return '1'
    else:
        lastNumber = dataList[-1][0]
        return str(int(lastNumber) + 1)

def setCondition(csvFile, conditionIndex, conditionDictionary):
    # Uses a dictionary to store the count in each condition, fetches these counts from the csv file and uses a list
    # comprehension to efficiently create a list of the conditions with fewest subjects in to select the condition
    # randomly from.
    dataList = listmaker(csvFile)
    for group in conditionDictionary:
        for row in dataList[1:]:  # Ignores the header
            if row[conditionIndex] == group:
                conditionDictionary[group] += 1
    smallestGroups = [group for group in conditionDictionary
                      if conditionDictionary[group] == min(conditionDictionary.values())]
    return chooseRandom(smallestGroups)

def recordData(csvFile, fieldVariableList):
    # Opens experiment data file to be appended to
    data = open(csvFile, 'a')
    data.write(','.join(fieldVariableList) + '\n')
    data.close()
