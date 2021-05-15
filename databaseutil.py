import os
import sys
sys.path.append(".")
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases

class databaseutil:

	def createSchema(self, dbConnection):
		utility = Utility()
		self.createDataTablesSQLScript(SQLCommandsPhrases.SchemaName.value)
		sqlRead = FileUtil(ResourceLocation.DatabaseScript.value, "r")
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.DBDatabaseCreation.value,"a", False)		
		self.executeAndCommitToDatabase(dbConnection, sqlRead)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.Completed.value,"a", True)

	def loadDataFromCSV(self, dbConnection, schemaName):
		utility = Utility()
		fileList = os.listdir(ResourceLocation.DatabaseLocation.value)
		filePaths = self.getFilePaths(fileList)
		insertSQLs = []
		for filePath in filePaths:
			file = (FileUtil(filePath, "r")).getFile()
			dbConnection.copyFromCSVs(file, schemaName + "." + (((filePath.split("/"))[2]).split("."))[0], ",")
			dbConnection.commitTransaction()
		dbConnection.closeDBConnection()
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.Completed.value,"a", True)
		print("Loading Data")

	def createDataTablesSQLScript(self, schemaName):
		utility = Utility()
		fileList = os.listdir(ResourceLocation.DatabaseLocation.value)
		tableHeaders = self.getTableHeader(fileList)
		createTableCommands = self.createCommandsFromHeaders(tableHeaders, fileList, schemaName)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, ("\n").join(createTableCommands), LogMessage.DBDatabaseCreationCommands.value,"a", False)
		utility.writeCommandSqlScript(("\n").join(createTableCommands), ResourceLocation.DatabaseScript.value)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.DBDatabaseSQLScriptCreated.value,"a", False)

	def getTableHeader(self, fileList):
		utility = Utility()
		filePaths = self.getFilePaths(fileList)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, ("\n").join(filePaths), LogMessage.Files.value,"a", False)
		tableHeaders = []
		for filePath in filePaths:
			fileHeader = ((FileUtil(filePath, "r")).getFileContent())[0]
			tableHeaders.append(fileHeader)
		return tableHeaders

	def getFilePaths(self, fileList):
		filePaths = []
		for fileName in fileList:
			if "csv" in fileName: 
				filePaths.append(ResourceLocation.DatabaseLocation.value + fileName)
		return filePaths
		
	def createCommandsFromHeaders(self, tableHeaders, fileList, schemaName):
		createTableCommands = []
		createTableCommands.append(SQLCommandsPhrases.DropSchema.value + " " + schemaName + SQLCommandsPhrases.Cascade.value + ";\n")
		createTableCommands.append(SQLCommandsPhrases.CreateSchema.value + " " + schemaName + ";\n")
		tableIndex = 0
		for tableHeader in tableHeaders:
			tableColumns = tableHeader.split(",")
			dropCommand = SQLCommandsPhrases.DropTable.value + schemaName + "." + (fileList[tableIndex]).split(".")[0] + SQLCommandsPhrases.Cascade.value + ";"
			createCommand = SQLCommandsPhrases.CreateTable.value + schemaName + "." + (fileList[tableIndex]).split(".")[0] +" ("
			tableColumnIndex = 0
			for tableColumn in tableColumns:
				createCommand += " " + tableColumn + SQLCommandsPhrases.CharacterVarying.value
				if tableColumnIndex == 0:
					createCommand += SQLCommandsPhrases.PrimaryKey.value + ","
				elif len(tableColumns) > (tableColumnIndex + 1):
					createCommand += ","
				tableColumnIndex += 1
			createCommand += ");"
			createTableCommands.append(dropCommand)
			createTableCommands.append(createCommand)
			tableIndex += 1
		return createTableCommands

	def executeAndCommitToDatabase(self, dbConnection, sqlRead):
		dbConnection.executeSQL(sqlRead.readFile())
		dbConnection.commitTransaction()
		dbConnection.closeDBConnection()




			


