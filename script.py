import aiml
import os
import time, sys
#from gtts import gTTS
from pygame import mixer
import pyttsx
import warnings
import speech_recognition as sr

class Script:

	"""
	def speak(self, jarvis_speech):
	  self.tts = gTTS(text=jarvis_speech, lang='en')
	  self.tts.save('jarvis_speech.mp3')
	  self.mixer.init()
	  self.mixer.music.load('jarvis_speech.mp3')
	  self.mixer.music.play()
	  while mixer.music.get_busy():
	      self.time.sleep(1)"""

	def offline_speak(self, jarvis_speech):		
		engine = pyttsx.init()
		rate = engine.getProperty('rate')
		voice = engine	.getProperty('voices')
		engine.setProperty('rate', 160)
		engine.setProperty('voice', voice[10].id)
		engine.say(jarvis_speech)
		engine.runAndWait()

	def listen(self):
	    r = sr.Recognizer()
	    with sr.Microphone() as source:	
		#r.pause_threshold = 0.5
		r.adjust_for_ambient_noise(source, duration = 1)        
		audio = r.listen(source)
	    try:
		print r.recognize_google(audio)
		return r.recognize_google(audio)
	    except sr.UnknownValueError:
		self.offline_speak("I couldn't understand what you said! Would you like to repeat?")
		return(self.listen())
	    except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

	
	def start(self):
		
		mode = "text"
		if len(sys.argv) > 1:
		    if sys.argv[1] == "--voice" or sys.argv[1] == "voice":
			try:
			    import speech_recognition as sr
			    mode = "voice"
			except ImportError:
			    print("\nInstall SpeechRecognition to use this feature.\nStarting text mode\n")

		terminate = ['bye','buy','shutdown','exit','quit','gotosleep','goodbye']


		kernel = aiml.Kernel()

		if os.path.isfile("bot_brain.brn"):
		    kernel.bootstrap(brainFile = "bot_brain.brn")
		else:
		    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
		    kernel.saveBrain("bot_brain.brn")

		while True:
		    if mode == "voice":
			#print(mode)
			print("Talk to Digital Assistance : ")
			self.offline_speak('Talk to Digital Assistance : ')       
			self.response = self.listen()
		    else:
			self.response = raw_input("Talk to Digital Assistance : ")
		    if self.response.lower().replace(" ","") in terminate:
			break
		    jarvis_speech = kernel.respond(self.response)
		    print "Digital Assistance: " + jarvis_speech
		    self.offline_speak(jarvis_speech)
		    

obj1 = Script()
obj1.start()
