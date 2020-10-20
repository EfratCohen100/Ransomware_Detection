import pathlib
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import watchdog.events
import watchdog.observers
import time
import enchant

def ConvertEncrypedFile(self,nameFile):
	return False

def checkChangeFromFile(self, nameFile):
	for path in pathlib.Path("files").iterdir():
		nameFileFromPath = str(path)
		x = nameFileFromPath.split('\\')
		name = x[1]
		flag= False
		flagword = True
		if nameFile.__eq__(name):
			current_file = open(path, "r")
			count=0
			splitWords = current_file.read().split(" ")
			# calculate to check if exist more in 10% words that not exists in dictionary - suspicion of encryptions
			calculate = (10/100)* splitWords.__len__()
			englishWord = enchant.Dict("en_US")
			for word in splitWords:
				splitbyenter = word.split("\n")
			#	print(splitbyenter)
				for wordbyenter in splitbyenter:
					for char in wordbyenter:
						if((ord(char) != 32 )&( (-1 < ord(char) < 48) or (57 < ord(char) < 65) or (90 <ord(char) < 97))):
							flag = True
					if(flag):
						print("File:", current_file.name, "has been changed, invalid- contains non-ascii characters!- suspected of encryption!")
						break
				if (flag):
					break
				else:
					if(wordbyenter =="" or englishWord.check(wordbyenter)):
						continue
					else:
						count += 1
						continue
			if (flag):
				break
			if (count > calculate):
				flagword = False
				print("File:", current_file.name, "has been changed- Contains non-English words suspected of encryption!")
				break

			if(flagword == True):
				print("File:", current_file.name,"has been changed- Legal Change!")
				break

class Handler(watchdog.events.PatternMatchingEventHandler):
	def __init__(self):
		# Set the patterns for PatternMatchingEventHandler
		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.txt'],
															ignore_directories=True, case_sensitive=False)

	def on_modified(self, event):
		ev=str(event.src_path)
		x=ev.split('\\')
		nameFile=x[1]
		#print(nameFile)
		checkChangeFromFile(self,nameFile)
		#print("Watchdog received modified event - % s." % event.src_path)
		# Event is modified, you can process it now


if __name__ == "__main__":
	src_path = "files"
	event_handler = Handler()
	observer = watchdog.observers.Observer()
	observer.schedule(event_handler, path=src_path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()


