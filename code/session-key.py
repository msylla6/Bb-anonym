# Compiled by Mihai Boicu based on code created by:
# 2021 July-August
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing)
# 2022 March-
# - Anushree Manoharrao (session-key.py - documentation,comments)s
# - Mouhamed Sylla import random, os, and json. Random is used to randomize keys and data. Json is needed to be imported to
#parse the data that we get from the files with the keys and data so it is easier to divey up data and give random numbers to
#keep privacy EX. student data comes in list json makes it an array and moves forward. For the session key there needs to be
#a configurated file to generate keys if there is no file that the file is randomly generated with keys. def load(Self)
#used to open the file and read the data only after this is done the user needs to save the file and then input data
#Once the file is input the data gets allocated and generated for startyear, endyear, lastkey, minstep, maxstep and semster
#following the generate code there is then added randomization code to keep privacy of students lastKey += random.randint(minStep, maxStep)
# finally #Initialize and checks if file exist if does not generates a new data it saves it.

import random
import os
import json


# Session Anonymization Key

class SessionKey:
    # configuration file to be used to generate the keys
    configFileName = "../config/session-config.json"

    # randomly generated file for session keys
    keyFileName = "../key/sessionKeys.txt"

    # a map between a session (i.e. semester) and its code
    # example (200040, 198) will link Summer semester in 2000 with the code 198
    dictionary = {}

    #open file and read data
    def load(self):
        file = open(self.keyFileName)
        lines = file.readlines()
        for line in lines:
            sessions = line.split(" ")
            self.dictionary[int(sessions[0])] = int(sessions[1])
        file.close()

    #Save file and input data into files
    def save(self):
        # print("No session keys file found, creating new file!")
        file = open(self.keyFileName, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    #Generate data
    def generate(self):
        configFile = open(self.configFileName, )
        configData = json.load(configFile)

        startYear = configData['start_year']
        endYear = configData['end_year']
        lastKey = configData['start_key']
        minStep = configData['min_step']
        maxStep = configData['max_step']
        semesters = configData['semesters_list']

        #for loop to start year and end year keeps going and adding 1
        #dictionary allows user to add value to dictionary equal t lastKey
        for i in range(startYear, endYear + 1):
            for sem in semesters:
                self.dictionary[(i * 100 + sem)] = lastKey
                lastKey += random.randint(minStep, maxStep)

        # print("lastKey: ",lastKey)
        # print("sessionDict: ", sessionDict)

    #Initialize and checks if file exist if does not generates a new data it saves it.
    def __init__(self):
        if os.path.isfile(self.keyFileName):
            self.load()
        else:
            self.generate()
            self.save()

