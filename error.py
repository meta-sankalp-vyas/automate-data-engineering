import sys
sys.path.append(".")
from utility import utility as Utility
from utility import resourcelocation as ResourceLocation

class Error(Exception):
	def __init__(self, message, content):
		self.message = message
		self.content = content
		super().__init__(self.message)

	def writeErrorLogs(self):
		Utility().writeLogs(ResourceLocation.LogFileLocation.value, self.message, self.content, "a", True)

	def screenLogs(self):
		print(self.message + "\nPlease refer logs file for detail explanation.")

	def handleError(self):
		print("===================================")
		self.writeErrorLogs()
		self.screenLogs()
		print("===================================")