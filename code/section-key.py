#Mouhamed Sylla
#This section of the code is nessecary for this research because the section of the class in question has to be randomized
#If the section is not randomized it is easy to tell which student is from which because the section divides students up by classes.
#Firstly needs to access the data and seperate the different sections by making them strings and giving value numbers to hold them such as
#sections[1] and close. Next save the file and loads seesion key file and uses isfile to make sure the keyfile exist
#After making sure the file exist the code moves onto loading and once loaded randomizing the section uses while loop
#to keep randomizing sections untill there is a section number that does not exist in the dictionary. The equation is
#(sessionCode * 100 + random.random() * 100)


class SectionKey:
    keyFileName = "../key/sectionKeys.txt"
    sessionKey: SessionKey

    dictionary = {}

    #Loads data and reads file
    def load(self):
        file = open(self.keyFileName, "r")
        lines = file.readlines()
        for line in lines:
            sections = line.split(" ")
            self.dictionary[str(sections[0])] = sections[1]
        file.close()

    #opens file, writes in file, and sorts values.
    def save(self):
    #Uses "w" to write in file and then self.dictionary.keys to access the dictionary for the keys in the file
        file = open(self.keyFileName, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    #Loads seesion key file and uses isfile to make sure file exist
    def __init__(self, sessionKey):
        self.sessionKey=sessionKey
        if os.path.isfile(self.keyFileName):
            self.load()


    def get(self, section):
        # check if section already used in sectionDict
        if section in self.dictionary.keys():
            return self.dictionary[section]
        # define new code
        #splitting parts between a period from section part and session part to differentiate the section and time
        parts = section.split(".")
        sectionPart = int(parts[0])
        sessionPart = int(parts[1])
        sessionCode = self.sessionKey.dictionary[sessionPart]
        sectionCode = -1

        #Uses while loop to check if it has a section code and keeps randomizing sections untill there is a section
        #number that does not exist in the dictionary. Once there is a section that does not exist breaks from file and
        #return to dictionary
        while True:
            sectionCode = int(sessionCode * 100 + random.random() * 100)
            if not sectionCode in self.dictionary.values():
                break
        self.dictionary[section] = sectionCode
        # return code
        return self.dictionary[section]