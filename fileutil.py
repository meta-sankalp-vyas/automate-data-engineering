import csv
class fileutil:
	def __init__(self,fileLocation,access):
		self.fileLocation=fileLocation
		self.fileAccess=access

	def getFileLocation(self):
		return self.fileLocation

	def getFileAccess(self):
		return self.fileAccess

	def getFileContent(self):
		readFileConfiguration = open(self.fileLocation,self.fileAccess,encoding="utf8")
		fileContent = readFileConfiguration.readlines()
		return fileContent

	def writeFileContent(self, content):
		writeFileConfiguration = open(self.fileLocation,self.fileAccess,encoding="utf8")
		writeFileConfiguration.write(content)
		writeFileConfiguration.close()
		return 1>0
	
	def readFile(self):
		readFileConfiguration = open(self.fileLocation,self.fileAccess,encoding="utf8")
		fileContent = readFileConfiguration.read()
		return fileContent

	def getFile(self):
		return open(self.fileLocation,self.fileAccess,encoding="utf8")

	def getCSVReader(self):
		csvReader = None
		returnArray = []
		with open(self.fileLocation) as csv_file:
			csvReader = csv.reader(csv_file, delimiter=',', quotechar='|')
			line_count = 0
			for row in csvReader:
				returnArray.append("|,|".join(row))
				line_count += 1
		return returnArray

		
