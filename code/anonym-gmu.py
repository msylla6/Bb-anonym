# Compiled by Mihai Boicu based on code created by:
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing)

import random
import os
import json
import shutil
from datetime import date
import csv

# Session Anonymization Key

class SessionKey:
    keyFileName = "../key/sessionKeys.txt"
    configFileName = "../config/session-config.json"

    dictionary = {}

    def load(self):
        file = open(self.keyFileName)
        lines = file.readlines()
        for line in lines:
            sessions = line.split(" ")
            self.dictionary[int(sessions[0])] = int(sessions[1])
        file.close()

    def save(self):
        # print("No session keys file found, creating new file!")
        file = open(self.keyFileName, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    def generate(self):
        configFile = open(self.configFileName,)
        configData = json.load(configFile)

        startYear = configData['start_year']
        endYear = configData['end_year']
        lastKey = configData['start_key']
        minStep = configData['min_step']
        maxStep = configData['max_step']
        semesters = configData['semesters_list']

        for i in range(startYear,endYear+1):
            for sem in semesters:
                self.dictionary[(i*100+sem)] = lastKey
                lastKey += random.randint(minStep, maxStep)

        # print("lastKey: ",lastKey)
        # print("sessionDict: ", sessionDict)

    def __init__(self):
        if os.path.isfile(self.keyFileName):
            self.load()
        else:
            self.generate()
            self.save()

# Assignment Anonymization Key 

class AssignmentKey:
    configurationFileName = '../predefined-key/assignment-config.json'
    defaultTotalZeroPoints = 1

    dictionary = {}

    def load(self):
        configFile = open(self.configurationFileName,)
        configData = json.load(configFile)
        assignmentArray = configData['assignments']
        for group in assignmentArray:
            self.dictionary[group['name']] = group['code']
        configFile.close()

    def __init__(self):
        self.load()

    def getGC(self, gcName):
        pointsSplit = gcName.split("[")
        pointsPart = pointsSplit[1].split(' ')[2]
        points = 0.0
        if pointsPart == 'up':
            points = float(pointsSplit[1].split(' ')[4])
        else:
            points = float(pointsPart)      

        nameSplit = pointsSplit[0].split('-')[0].split('(')[0]
        name = str(nameSplit).strip()  # + ' [' + points + ']'
        if points == 0:
            points == self.defaultTotalZeroPoints
        if name in self.dictionary:
            return self.dictionary[name], points
        else:
            #print("Assignment name: " + anonAssiName + " not found within config file")
            #print("Defaulting assignment name.")
            return "IGNORE", points

    def getQR(self, qrName):
        print(qrName)
        name = qrName.strip()
        if name in self.dictionary:
            return self.dictionary[name]
        else:
            return "IGNORE"

# User Anonymization Key 

class UserKey:
    configFileName = "../config/user-config.json"
    keyFileName = "../key/userKeys.txt"
    minUserCode=None
    maxUserCode=None

    dictionary = {}

    def loadConfig(self):
        userConfigFile = open(self.configFileName)
        userConfigData = json.load(userConfigFile)
        self.minUserCode = userConfigData['min_key']
        self.maxUserCode = userConfigData['max_key']
        userConfigFile.close()

    def load(self):
        # print("Grabbing User Keys!")
        file = open(self.keyFileName)
        lines = file.readlines()
        for line in lines:
            elements = line.split(' ')
            self.dictionary[(elements[0])] = int(elements[1])
        file.close()

    def save(self):
        file = open(self.keyFileName, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    def __init__(self):
        self.loadConfig()
        if os.path.isfile(self.keyFileName):
            self.load()

    def get(self, id):
        # check if section already used in sectionDict
        if id in self.dictionary.keys():
            return self.dictionary[id]
        # define new code              
        while True:
            code = random.randint(self.minUserCode, self.maxUserCode)
            if not code in self.dictionary.values():
                break
        self.dictionary[str(id)] = code
        return code

    def print(self):
        print("*****")
        print("*** USER KEY")
        print("*** User Key Config ***")
        print("Min User Code: "+str(self.minUserCode))
        print("Max User Code: "+str(self.maxUserCode))

# Section Anonymization Key

class SectionKey:
    keyFileName = "../key/sectionKeys.txt"
    sessionKey: SessionKey

    dictionary = {}

    def load(self):
        file = open(self.keyFileName, "r")
        lines = file.readlines()
        for line in lines:
            sections = line.split(" ")
            self.dictionary[str(sections[0])] = sections[1]
        file.close()

    def save(self):
        file = open(self.keyFileName, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    def __init__(self, sessionKey):
        self.sessionKey=sessionKey
        if os.path.isfile(self.keyFileName):
            self.load()

    def get(self, section):
        # check if section already used in sectionDict
        if section in self.dictionary.keys():
            return self.dictionary[section]
        # define new code
        parts = section.split(".")
        sectionPart = int(parts[0])
        sessionPart = int(parts[1])
        sessionCode = self.sessionKey.dictionary[sessionPart]
        sectionCode = -1
        while True:
            sectionCode = int(sessionCode * 100 + random.random() * 100)
            if not sectionCode in self.dictionary.values():
                break
        self.dictionary[section] = sectionCode
        # return code
        return self.dictionary[section] 

# Anonymization Key 

class AnonymKey:
    sessionKey = SessionKey()
    assignmentKey = AssignmentKey()
    userKey = UserKey()
    sectionKey = SectionKey(sessionKey)

    def save(self):
        self.sectionKey.save()
        self.userKey.save()

    def print(self):
        print("*****")
        print("*** ANONYMIZATION KEY ***")
        self.userKey.print()

# Anonymization Process Class

class AnonymProcess:
    inboxFolder = '../inbox/'
    outboxFolder = '../outbox/'
    archiveFolder = '../archive/'

    key = AnonymKey()

    inboxFiles = []

    def initInboxFiles(self):
        try:
            self.inboxFiles = os.listdir(self.inboxFolder)
        except FileNotFoundError:
            exit("You do not have an inbox folder!")

    def initOutboxFolder(self):
        try:
            os.listdir(self.outboxFolder)
        except FileNotFoundError:
            exit("You do not have an outbox folder!")

    def __init__(self):
        self.initInboxFiles()
        self.initOutboxFolder()

    def printInboxFiles(self):
        print("*****")
        print("INBOX files:")
        for entry in self.inboxFiles:
            print(entry)
    
    def print(self):
        self.key.print()
        self.printInboxFiles()
    
    def gcProcessFileName(self, fileName):
        outputName = "gc_"
        inputArray = fileName.split("_")
        if len(inputArray) != 4:
            exit("Unexpected file name"+fileName)
        # section
        outputName += str(self.key.sectionKey.get(inputArray[1]))
        # type 
        outputName += "_" + inputArray[2] + "_"
        # date-time
        dateArray = inputArray[3].split("-")
        # 2021-06-24-09-37-32
        # 0    1  2  3  4  5
        stringName = str(fileName)
        yearName = stringName[9:13]
        sectionY = int(yearName)
        fileY = int(int(dateArray[0]))
        dayDiff = 400
        if fileY == sectionY:
            term=str(inputArray[1])[11]
            month=1
            if term=="1":
                month=1
            elif term=="4":
                month=5
            elif term=="7":
                month=8
            f_date = date(fileY, month, 15)
            l_date = date(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))
            delta = l_date - f_date
            dayDiff = delta.days + 1
        outputName += str(dayDiff) + "-" + dateArray[3] + "-" + dateArray[4] + ".csv"
        return outputName
    
    def gcProcess(self,inputFile, format):
        inputFileName=str(inputFile)
        outputFileName=self.gcProcessFileName(inputFileName)
        print("Process GC file: "+str(inputFileName))
        print("Output GC file: "+str(outputFileName))
 
        inboxFile = self.inboxFolder+inputFileName
        outboxFile = self.outboxFolder + str(outputFileName)
        archiveFile = self.archiveFolder + inputFileName

        data = []
        points = []
        counter = 0
        ffiledate = date(2021, 6, 1)
        with open(inboxFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # print("DEBUG: row[0]="+row[0])
                # print("DEBUG: row[1]="+row[1])
                data.append([])
                if counter == 0:
                    for columnIndex in range(0, len(row)):
                        if columnIndex >= 6:
                            assignmentName, assignmentPoints = self.key.assignmentKey.getGC(row[columnIndex])
                            points.append(assignmentPoints)
                            data[counter].append(assignmentName)
                        elif columnIndex < 2 or columnIndex == 5 or columnIndex == 3 or columnIndex == 4:
                            pass
                        else:
                            data[counter].append(row[columnIndex])
                else:
                    data[counter].append(self.key.userKey.get(row[2]))
                    # print("DEBUG: row[4]="+row[4])
                    # rowDate = row[4]
                    # lfiledate = date(int(rowDate[0:4]), int(rowDate[5:7]), int(rowDate[8:10]))
                    # delta = lfiledate - ffiledate
                    # dayDiff = delta.days + 1
                    # data[counter].append(str(dayDiff))

                    for columnIndex in range(6, len(row)):
                        try: 
                            val = float(row[columnIndex])
                            if format=="percent":
                                val = val/points[columnIndex-6]
                            data[counter].append(val)                            
                        except:
                            data[counter].append("")

                counter += 1

        with open(outboxFile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

        shutil.move(inboxFile, archiveFile)   

    def qrProcessFileName(self, fileName):
        outputName = "qr_"
        inputArray = fileName.split("_")
        # section
        outputName += str(self.key.sectionKey.get(inputArray[1]))
        # type
        inputArray2 = inputArray[2].split("-")
        assiname = inputArray2[0]
        assiname = (self.key.assignmentKey.getQR(assiname))
        outputName += "_" + assiname + ".csv"
        return outputName

    def qrProcessData(self, fileName):
        data = []  # this data array will be used to store the data in the csv file
        counter = 0  # counter for the algorithm, will act as the row counter
        with open(fileName, newline='') as csvfile:  # grabs the file that exists at original, opens it
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
                    data[counter].append(self.key.userKey.get(row[2]))

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

    def qrProcess(self,inputFile):
        inputFileName=str(inputFile)
        outputFileName=self.qrProcessFileName(inputFileName)
        print("Process QR file: "+str(inputFileName))
        print("Output QR file: "+str(outputFileName))
        original = r'../inbox/' + str(inputFile)
        target = r'../outbox/' + outputFileName
        archive = r'../archive/' + str(inputFile)
        data = self.qrProcessData(original)
        with open(target, 'w', newline='') as csvfile:  # creates a new csv file at target path
            writer = csv.writer(csvfile)  # writer starts writing into file
            for row in data:
                if row:# for every row in the 2d array data (row is an array here)
                    writer.writerow(row)  # writes row, the 1d array, into the file
        shutil.move(original, archive) 

    
    def aaProcessFileName(self, fileName):
        outputName = "aa_"
        inputArray = fileName.split("_")
        # section
        outputName += str(self.key.sectionKey.get(inputArray[1]))
        # type
        assiname = inputArray[2]
        assiname = assiname.split("-")[0]
        assiname = (self.key.assignmentKey.getQR(assiname))
        outputName += "_" + assiname + ".csv"
        return outputName

    def aaProcessData(self, fileName):
        data = []  # this data array will be used to store the data in the csv file
        counter = 0  # counter for the algorithm, will act as the row counter
        with open(fileName, newline='') as csvfile:  # grabs the file that exists at original, opens it
            reader = csv.reader(csvfile)  # reader scans through original file
            for row in reader:  # loops through every row in reader (row is an array of the columns for the row)
                data.append([])  # data appends another array, making it a 2d array
                if counter == 0:  # if this is the first row (column headers)
                    data[counter].append("User ID")
                    data[counter].append("Grade")
                    data[counter].append("Attempt")
                    data[counter].append("Duration")
                else:  # if this is not the first row (actual data of the students)
                # print(row)
                    data[counter].append(self.key.userKey.get(row[2]))
                    data[counter].append(row[3])
                    data[counter].append(row[4])
                    data[counter].append(row[7])
                counter += 1  # increments counter, signifying to go to the next row, stepping the 2d array when it is called
        return data

    def aaProcess(self,inputFile):
        inputFileName=str(inputFile)
        outputFileName=self.aaProcessFileName(inputFileName)
        print("Process AA file: "+str(inputFileName))
        print("Output AA file: "+str(outputFileName))
 
        original = r'../inbox/' + str(inputFile)
        target = r'../outbox/' + outputFileName
        archive = r'../archive/' + str(inputFile)
        data = self.aaProcessData(original)
        with open(target, 'w', newline='') as csvfile:  # creates a new csv file at target path
            writer = csv.writer(csvfile)  # writer starts writing into file
            for row in data:
                if row:# for every row in the 2d array data (row is an array here)
                    writer.writerow(row)  # writes row, the 1d array, into the file
        shutil.move(original, archive) 

    # format: "points" or "percent"
    def run(self, format):
        for inFile in self.inboxFiles:
            inFileName = str(inFile)
            if inFileName == "-1":  # th
                break
            if inFileName.startswith("gc_"):
                self.gcProcess(inFile, format)
            elif inFileName.startswith("qr_"):
                self.qrProcess(inFile)
            elif inFileName.startswith("aa_"):
                self.aaProcess(inFile)
            elif not inFileName.startswith("."):
                print("Unknown type of file: "+inFileName)
        self.key.save()

def establishConfig():
    assiConfig = open('../predefined-key/assignment-config.json')
    assiArray = json.load(assiConfig)['assignments']
    unlimitedArray = []
    twoTrialsArray = []
    oneTrialArray = []
    for dict in assiArray:
        if 'Cumulative' in dict['name']:
            unlimitedArray.append(dict['code'])
        elif 'Final Exam' in dict['name']:
            oneTrialArray.append(dict['code'])
        elif 'Quiz' in dict['name']:
            twoTrialsArray.append(dict['code'])
    print('Unlimited Assignments: ', unlimitedArray)
    print('One Trial Assignments: ', oneTrialArray)
    print('Two Trial Assignments: ', twoTrialsArray)
    return unlimitedArray, oneTrialArray, twoTrialsArray

def main():
    process = AnonymProcess()
    process.run("percent")

    # unlimitedArray, oneTrialArray, twoTrialsArray = establishConfig()
    # process.print()

if __name__ == '__main__':
    main()
