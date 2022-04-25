Section.md
Understanding how to configure the class Section Key
The class section Is used to randomize the section portion on the GMU database when handling student grades. This class can be used for many different uses such as randomizing sections in any grade system and to be used in tandem with the session key file.

Imports associated with Section
Import OS
Import random
Import session_key
To make the class, sectionkey, work you need:
Session_key: Used after the session key has ran and is used to connect the session with the section  There is a maximum of 100 sections per session
Config/session-config.json: Keeps the configuration data on how to generate the anoymized values for the session
Section_key_test.py: Used to show how the keys look after generated 
Sectionkeys.txt: This is where the keys are held after being saved and generated
Moch Test for Section md
import session_key	
		import section_key
		

		def main():
		    sessionKey = session_key.SessionKey()
		    sectionKey = section_key.SectionKey(sessionKey)
		    print(sectionKey.get("11233.202110"))
		    print(sectionKey.get("10851.202110"))
		    print(sectionKey.get("11067.202110"))
		    sectionKey.save()
		

		if __name__ == '__main__':
		    main()

Sample of output in sectionkeys.txt
Print(sectionKey.get(“11233.202110”))
Print(sectionKey.get(“10851.202110”))
Print(sectionKey.get(“11067.202110”))
With the output being
11233.202110, 10851.202110, and 11067.202110.
202110 is the session got from session_key and the first 5 numbers being the randomized number for the section with the equation of (sessionCode * 100 +random.random() *100)
example "11233.202110" is associated with 12345 where 123 is the code for session 202110 and 45 is the code for section 11233
 The Output is then put into the sectionkey.txt file

Understand how to call the Section Key
Import section_key.py
Use session to create section  call section to see if anonym saved the file then Create  the instance of the class and do not duplicate the call

