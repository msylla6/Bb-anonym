# Compiled by Mihai Boicu based on code created by:
# 2021 July-August
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing) 
# 2022 March-
# - Anushree Manoharrao (session-key.py - documentation,comments) 

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

            
