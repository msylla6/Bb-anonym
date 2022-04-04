# New object is created for session key, assignment key, user key and section key
class AnonymKey:
    sessionKey = SessionKey()
    assignmentKey = AssignmentKey()
    userKey = UserKey()
    sectionKey = SectionKey(sessionKey)

#It starts with executing the save function of section key and user key which generates the anonymized values for sessionkeys and userkeys
	def save(self):
        self.sectionKey.save()
        self.userKey.save()

#the anaonymized user ids in userkeys.txt are printed
    def print(self):
        print("*****")
        print("*** ANONYMIZATION KEY ***")
        self.userKey.print()
