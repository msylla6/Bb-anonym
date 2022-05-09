# H1 Anonymizing the Course Sections
Contributers:
•	Mouhamed Sylla (Documentation) Spring 2022
# H1 Understanding how to configure the class section key
The class section is used to randomize the section code (i.e. 10851.202110) of a GMU course. This code will be randomized using the sesession anonymized key for the session part (e.g., 395 for 202110), and will generate a random number from 0 to a max value for the section code (i.e. 10851). The final code will be obtained by the formula:
•	sesessioncode * maxvalue + section code
Based on the number of section that you plan to anonymize in each session, you may change the max value in the code (i.e., MAX_SECTIONS_PER_SESSION). Its default value is 100.
This section code appears in the name of the files when downloaded from the Blackboard, or must be added to the name of some files. For instance a grade book downloaded file will contain the section code in its name.
# H1 Sample of output in section_key
.11233.202110, 
10851.202110,
11067.202110
These numbers were generated in the same way of the input of:
def main():
	    sessionKey = session_key.SessionKey()
	    sectionKey = section_key.SectionKey(sessionKey)
	    print(sectionKey.get("11233.202110"))
	    print(sectionKey.get("10851.202110"))
	    print(sectionKey.get("11067.202110"))
	    sectionKey.save()
	

	if __name__ == '__main__':
	    main()

and formula of:
•	sesessioncode * maxvalue + section code

•	Sample of output in sectionkeys.txt Print(sectionKey.get(“11233.202110”)) Print(sectionKey.get(“10851.202110”)) Print(sectionKey.get(“11067.202110”)) With the output being 11233.202110, 10851.202110, and 11067.202110. 202110 is the session got from session_key and the first 5 numbers being the randomized number for the section with the equation of (sessionCode * 100 +random.random() *100) example "11233.202110" is associated with 12345 where 123 is the code for session 202110 and 45 is the code for section 11233 The Output is then put into the sectionkey.txt file


# H1Understanding how to call the class section key
To use the anonymized section key you must:
•	create a session key instance (only one must be created for your anonymized code)
import session_key

def main():
  sessionKey = session_key.SessionKey()
•	import the class
import section_key;
•	create only one instance of the class (do not duplicate the call)
sectionKey = section_key.SectionKey(sessionKey)
Always this class will be used in tandem with the session key file and you must create only one instance of each for your entire code.
# H1 Understanding how the class section key is coded
Imports associated with Section Import OS Import random Import session_key To make the class, sectionkey, work you need: Session_key: Used after the session key has ran and is used to connect the session with the section There is a maximum of 100 sections per session Config/session-config.json: Keeps the configuration data on how to generate the anoymized values for the session Section_key_test.py: Used to show how the keys look after generated Sectionkeys.txt: This is where the keys are held after being saved and generated Moch Test for Section md import session_key import section_key
Understand how to call the Section Key Import section_key.py Use session to create section call section to see if anonym saved the file then Create the instance of the class and do not duplicate the call

