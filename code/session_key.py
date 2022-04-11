# Compiled by Mihai Boicu based on code created by:
# 2021 July-August
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing)
# 2022 March-April
# - Anushree Manoharrao (session-key.py - documentation,comments)
# - Mouhamed Sylla (comment code)
# - Mihai Boicu (update code/comments for clarity)

import random
import os
import json

# Session Anonymization Key
class SessionKey:

    # configuration file to be used to generate the keys
    CONFIG_FILE_NAME = "../config/session-config.json"

    # key file with randomly generated keys for sessions
    KEY_FILE_NAME = "../key/sessionKeys.txt"

    # a map between a session (i.e. semester) and its anonymized code
    # example (200040, 198) will link Summer semester in 2000 with the code 198
    dictionary = {}

    # load the generated key file and initialize the dictionary
    def load(self):
        file = open(self.KEY_FILE_NAME)
        lines = file.readlines()
        for line in lines:
            parts = line.split(" ")
            self.dictionary[int(parts[0])] = int(parts[1])
        file.close()

    # save the key file based on the current dictionary
    def save(self):
        # print("No session keys file found, creating new file!")
        file = open(self.KEY_FILE_NAME, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    # generate a new dictionary (assumed empty)
    def generate(self):
        configFile = open(self.CONFIG_FILE_NAME, )
        configData = json.load(configFile)

        startYear = configData['start_year']
        endYear = configData['end_year']
        lastKey = configData['start_key']
        minStep = configData['min_step']
        maxStep = configData['max_step']
        semesters = configData['semesters_list']

        # for all years in the configuration range
        for i in range(startYear, endYear + 1):
            # for all the semesters
            for sem in semesters:
                # update the last key to a new valid key
                lastKey += random.randint(minStep, maxStep)
                # save the semester and key in dictionary
                self.dictionary[(i * 100 + sem)] = lastKey

        # debug info
        # print("lastKey: ",lastKey)
        # print("sessionDict: ", sessionDict)

    # initialize the class
    # load the keys in dictionary if key file exist
    # or generate and save the key file otherwise
    def __init__(self):
        if os.path.isfile(self.KEY_FILE_NAME):
            self.load()
        else:
            self.generate()
            self.save()

