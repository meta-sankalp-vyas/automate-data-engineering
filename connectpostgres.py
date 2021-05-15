import psycopg2
import sys
sys.path.append(".")
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation

class connectpostgres:
	def __init__(self,configLine,configDelimiter,configFileName):
		self.configFileName=configFileName
		self.configLine=configLine
		self.configDelimiter=configDelimiter
		self.dbConnection=None
		self.dbCursor=None
		self.hostName=None
		self.portValue=None
		self.dbName=None
		self.userName=None
		self.password=None
		
	def getConfigLine(self):
		return self.configLine

	def getConfigFileName(self):
		return self.configFileName

	def getConfigDelimiter(self):
		return self.configDelimiter

	def getDBCursor(self):
		if self.dbConnection is None:
			self.establishConnection()
		self.dbCursor = self.dbConnection.cursor()
		return self.dbCursor

	def establishConnection(self):
		self.readConfig()
		utility = Utility()
		utility.writeLogs(ResourceLocation.LogFileLocation.value, LogMessage.DBConnection.value, "","a", False)
		self.dbConnection = psycopg2.connect(host= self.hostName, port = self.portValue, database= self.dbName, user= self.userName, password= self.password)
		if self.dbConnection is None:
			utility.writeLogs(ResourceLocation.LogFileLocation.value, LogMessage.DBConnectionError.value, "","a", True)
		else:
			utility.writeLogs(ResourceLocation.LogFileLocation.value, LogMessage.DBConnectionSuccess.value, "","a", True)

	def readConfig(self):
		# Read the file and config the connection variables
		file = FileUtil(self.configFileName,"r")
		dbConfiguration = file.getFileContent()
		config = dbConfiguration[int(self.configLine)]
		configArray = config.split(self.configDelimiter)
		self.hostName = configArray[0]
		self.portValue = configArray[1]
		self.dbName = configArray[2]
		self.userName = configArray[3]
		self.password = configArray[4]
	
	def closeDBConnection(self):
		self.dbCursor.close()
		self.dbConnection.close()
		self.dbCursor=None
		self.dbConnection=None

	def executeSQL(self, sqlQuery):
		self.getDBCursor()
		self.dbCursor.execute(sqlQuery)

	def executeSQLAndFetchAll(self, sqlQuery):
		self.executeSQL(sqlQuery)
		return self.dbCursor.fetchall()

	def copyFromCSVs(self, file, tableName, seperator):
		self.getDBCursor().copy_from(file, tableName, sep=seperator)
		return True

	def commitTransaction(self):
		if self.dbConnection is not None:
			self.dbConnection.commit()

	def rollBackTransaction(self):
		if self.dbConnection is not None:
			self.dbConnection.rollback()
