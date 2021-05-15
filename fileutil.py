class fileutil:
	def __init__(self,fileLocation,access):
		self.fileLocation=fileLocation
		self.fileAccess=access

	def getFileLocation(self):
		return self.fileLocation

	def getFileAccess(self):
		return self.fileAccess

	def getFileContent(self):
		readFileConfiguration = open(self.fileLocation,self.fileAccess)
		fileContent = readFileConfiguration.readlines()
		return fileContent

	def writeFileContent(self, content):
		writeFileConfiguration = open(self.fileLocation,self.fileAccess)
		writeFileConfiguration.write(content)
		writeFileConfiguration.close()
		return 1>0
	
	def readFile(self):
		readFileConfiguration = open(self.fileLocation,self.fileAccess)
		fileContent = readFileConfiguration.read()
		return fileContent

	def getFile(self):
		return open(self.fileLocation,self.fileAccess)