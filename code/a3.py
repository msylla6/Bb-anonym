import random
import os
import json
import shutil
from datetime import date
import csv

inboxFiles = []
userDict = {}
sessData = None

assignmentNames = {}
sessionDict = {}
sectionDict = {}
sectMult = 0.03

minUser=0
maxUser=100000000

def getInboxFiles():
    global inboxFiles

    try:
        inboxFiles = os.listdir('../inbox/')
    except FileNotFoundError:
        exit("You do not have an inbox folder!")

def checkOutboxFolder():
    try:
        os.listdir('../outbox/')
    except FileNotFoundError:
        exit("You do not have an outbox folder!")

def printInboxFiles():
    global inboxFiles
    print("Here are the files to be anonymized: ")
    for entry in inboxFiles:
        print(entry)

def getUserConfigurationFile():
    global minUser
    global maxUser

    userCon = open('../config/user-config.json')
    userConData = json.load(userCon)
    minUser = userConData['min_key']
    maxUser = userConData['max_key']

def grabAssignmentConfig():
    global assignmentNames

    assiCon = open('../predefined-key/assignment-config.json',)
    assiData = json.load(assiCon)
    assignmentArray = assiData['assignments']
    for group in assignmentArray:
        assignmentNames[group['name']] = group['code']

def grabUserKeys():
    global userDict

    print("Grabbing User Keys!")
    file = open("../key/userKeys.txt")
    lines = file.readlines()
    for line in lines:
        elements = line.split(' ')
        userDict[(elements[0])] = int(elements[1])

def grabSessionKeys():
    global sessionDict

    print("Reading session keys!")
    file = open("../key/sessionKeys.txt")
    lines = file.readlines()
    for line in lines:
        sessions = line.split(" ")
        sessionDict[int(sessions[0])] = int(sessions[1])

def saveSessionKeys():
    global sessionDict


    print("No session keys file found, creating new file!")
    file = open("../key/sessionKeys.txt", "w+")
    for keyName in sorted(sessionDict.keys()):
        file.write(str(keyName) + " " + str(sessionDict[keyName]) + "\n")
    file.close()

def generateSessionKeys():
    global sessionDict

    sessCon = open('../config/session-config.json',)
    sessData = json.load(sessCon)

    startYear = sessData['start_year']
    endYear = sessData['end_year']
    lastKey = sessData['start_key']

    for i in range(startYear,endYear+1):
        for sem in sessData['semesters_list']:
            sessionDict[(i*100+sem)] = lastKey
            lastKey += random.randint(sessData['min_step'], sessData['max_step'])

    # print("lastKey: ",lastKey)
    # print("sessionDict: ", sessionDict)

def grabSectionKeys(sectionFile):
    global sectionDict

    sectionFileForRead = open("../key/sectionKeys.txt", "r")
    print("Reading section keys!")
    lines = sectionFileForRead.readlines()
    for line in lines:
        sections = line.split(" ")
        sectionDict[int(sections[0])] = int(sections[1])

    return sectionDict

def anonymizeSection(section, sectionFile):
    global sectMult
    global sectionDict

    # check if section already used in sectionDict
    if section in sectionDict.keys():
        return sectionDict[section]

    newSect = int(section * sectMult * (random.random() * 0.75 + 0.01))
    while(newSect in sectionDict.values()):
        newSect = int(section * sectMult * (random.random() * 0.75 + 0.01))

    sectionDict[section] = newSect
    sectionFile.write(str(section) + " " + str(newSect) + "\n")

    return newSect

def anonAssignment(taskName):
    taskSplit = taskName.split("[")
    headName = taskSplit[0].split('-')[0].split('(')[0]
    #points = taskSplit[1].split(' ')[2]
    anonAssiName = str(headName).strip()  # + ' [' + points + ']'
    if anonAssiName in assignmentNames:
        return assignmentNames[anonAssiName]
    else:
        print("Assignment name: " + anonAssiName + " not found within config file")
        print("Defaulting assignment name.")
        return "ASSIGNMENT NAME NOT FOUND!"

def genUserID(userFile, unName):
    numGen = random.randint(minUser, maxUser)
    while numGen in userDict.values():
        numGen = random.randint(minUser, maxUser)
    userDict[str(unName)] = numGen
    userFile.write(str(unName) + ' ' + str(numGen) + '\n')
    return numGen

def anonQRfilename(filename):
    anonname = "qr_"

    sectSess = inputArray[1].split(".")
    section = int(sectSess[0])
    session = int(sectSess[1])
    anonSection = anonymizeSection(section, sectionFile)
    anonSession = sessionDict[session]
    anonname += str(anonSection) + "."
    anonname += str(anonSession) + "_"
    inputArray2 = inputArray[2].split("-")
    assiname = inputArray2[0]
    assiname = (anonAssignment(assiname))
    anonname += assiname + ".csv"
    return anonname

def anonQRdata():
    data = []  # this data array will be used to store the data in the csv file
    counter = 0  # counter for the algorithm, will act as the row counter
    ffiledate = date(2021, 6, 1)  # sets the first date
    with open(original, newline='') as csvfile:  # grabs the file that exists at original, opens it
        reader = csv.reader(csvfile)  # reader scans through original file
        for row in reader:  # loops through every row in reader (row is an array of the columns for the row)
            data.append([])  # data appends another array, making it a 2d array
            if counter == 0:  # if this is the first row (column headers)
                for columnIndex in range(0, len(row)):  # loops through every index for the row
                    # if columnIndex >= 6:  # if the columnn index is more than 6, this is an assignment name
                    # data[counter].append(anonAssignment(row[columnIndex]))  # calls the anonAssignment method to anonymize the name
                    # appends it to the 2d array of the current row (counter)
                    if columnIndex <= 2 or columnIndex == 4 or columnIndex == 7:  # These columns need to be deleted (first name, last name, ...)
                        pass  # pass so it never gets added to the data 2d array
                    else:
                        columnName = row[columnIndex]
                        if (columnName == "Question ID"):
                            columnName = "User ID"
                        if (columnName == "Manual Score"):
                            columnName = "Points Received"
                        data[counter].append(columnName)  # this means it is a columnn that can stay unchanged
            else:  # if this is not the first row (actual data of the students)
               # print(row)
                if row and (row[2] in userDict.keys()):
                    data[counter].append(userDict[row[2]])
                elif row:
                    data[counter].append(genUserID(userFile, row[2]))
                for columnIndex in range(5, len(row) - 1):
                    rowinp = row[columnIndex]  # appends the student data from column 6 and on (student scores)
                    if (columnIndex == 5 and (rowinp.lower() == "right" or rowinp.lower() == "wrong")):
                        rowinp = "TF"
                    elif (columnIndex == 5 and (rowinp.find("__") != 1)):
                        rowinp = "FITB"
                    data[counter].append(rowinp)
                    # appends the data to the 2d array
            counter += 1  # increments counter, signifying to go to the next row, stepping the 2d array when it is called
    return data

def qrAnonymizationProgram(inputFile):
    global original
    global archive
    original = r'../inbox/' + str(inputFile)
    target = r'../outbox/' + anonQRfilename(inputFile)
    archive = r'../archive/' + str(inputFile)
    data = anonQRdata()
    with open(target, 'w', newline='') as csvfile:  # creates a new csv file at target path
        writer = csv.writer(csvfile)  # writer starts writing into file
        for row in data:
            if row:# for every row in the 2d array data (row is an array here)
                writer.writerow(row)  # writes row, the 1d array, into the file
    #shutil.move(original, archive)  # moves the original file into the archive path

def main():
    global inboxFiles
    global inputArray
    global userDict
    global userFile
    global sectionFile
    global sectionDict

    checkOutboxFolder()
    getInboxFiles()
    printInboxFiles()

    grabAssignmentConfig()
    getUserConfigurationFile()

    if os.path.isfile("../key/sessionKeys.txt"):
        grabSessionKeys()
    else:
        generateSessionKeys()
        saveSessionKeys()

    userFile = open("../key/userKeys.txt", 'a+')
    if os.path.isfile("../key/userKeys.txt"):
        grabUserKeys()
    else:
        userDict = {}

    sectionFile = open("../key/sectionKeys.txt", "a+")  # open and grab keys from the section file
    sectionDict = grabSectionKeys(sectionFile)
    print("Read section keys: ", sectionDict)  # prints the keys

    f = open("../key/anonymization-results.txt", "w+")  # this is the anonymization-results file, doesn't really matter
    f.write("initial name  =>  anonymized name\n\n")  # writes into the file

    for unanonFile in inboxFiles:
        anonName = "gc_"
        inputFile = str(unanonFile)
        if inputFile == "-1":  # th
            break
        inputArray = inputFile.split("_")
        if inputArray[0] == 'qr':
            #anonQRfilename(inputFile)
            qrAnonymizationProgram(inputFile)

        elif len(inputArray) != 4:
            print("----> Unexpected Name Format! Try again.  :(")

        else:
            sectSess = inputArray[1].split(".")
            section = int(sectSess[0])
            session = int(sectSess[1])
            anonSection = anonymizeSection(section, sectionFile)
            anonSession = sessionDict[session]

            anonName += str(anonSection) + "."
            anonName += str(anonSession) + "_"

            gType = inputArray[2]
            anonName += gType + "_"
            dateArray = inputArray[3].split("-")
            # 2021-06-24-09-37-32
            # 0    1  2  3  4  5
            f_date = date(2021, 6, 1)
            l_date = date(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))
            delta = l_date - f_date
            dayDiff = delta.days + 1
            anonName += str(dayDiff) + "-" + dateArray[3] + "-" + dateArray[4] + ".csv"
            print("---->Anonymized Name of "+inputFile+":\n     " + anonName)
            f.write(inputFile + "  =>  " + anonName + "\n")

            original = r'../inbox/'+str(inputFile)
            target = r'../outbox/' + str(anonName)
            archive = r'../archive/' + str(inputFile)

            data = []
            counter = 0
            ffiledate = date(2021, 6, 1)
            with open(original, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # print("DEBUG: row[0]="+row[0])
                    # print("DEBUG: row[1]="+row[1])
                    data.append([])
                    if counter == 0:
                        for columnIndex in range(0, len(row)):
                            if columnIndex >= 6:
                                data[counter].append(anonAssignment(row[columnIndex]))
                            elif columnIndex < 2 or columnIndex == 5 or columnIndex == 3:
                                pass
                            else:
                                data[counter].append(row[columnIndex])
                    else:
                        if row[2] in userDict.keys():
                            data[counter].append(userDict[row[2]])
                        else:
                            data[counter].append(genUserID(userFile, row[2]))
                        # print("DEBUG: row[4]="+row[4])
                        rowDate = row[4]
                        lfiledate = date(int(rowDate[0:4]), int(rowDate[5:7]), int(rowDate[8:10]))
                        delta = lfiledate - ffiledate
                        dayDiff = delta.days + 1
                        data[counter].append(str(dayDiff))

                        for columnIndex in range(6, len(row)):
                            data[counter].append(row[columnIndex])
                    counter += 1

            with open(target, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in data:
                    writer.writerow(row)

            shutil.move(original, archive)

    f.write("\nSection dictionary: " + str({v: k for k, v in sectionDict.items()}))
    f.write("\nSession dictionary: " + str(sessionDict))
    f.close()
    sectionFile.close()
    print("\nDictionary of Conversions Outputted to File \"anonymization-results.txt\"")
    print("Here is the section dictionary: ", str({v: k for k, v in sectionDict.items()}))
    print("Here is the session dictionary: ", sessionDict)


if __name__ == '__main__':
    main()