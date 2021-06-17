import os, sys, traceback
sys.path.append(".")
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases
from error import Error as Error

class databaseutil:

	def createSchema(self, dbConnection, schemaName):
		utility = Utility()
		self.createDataTablesSQLScript(schemaName)
		sqlRead = FileUtil(ResourceLocation.DatabaseScript.value, "r")
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.DBDatabaseCreation.value,"a", False)		
		self.executeAndCommitToDatabase(dbConnection, sqlRead)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.Completed.value,"a", True)

	def loadDataFromCSV(self, dbConnection, schemaName):
		print("Loading Data....")
		utility = Utility()
		fileList = os.listdir(ResourceLocation.DatabaseLocation.value)
		filePaths = self.getFilePaths(fileList, "csv", ResourceLocation.DatabaseLocation.value)
		for filePath in filePaths:
			file = (FileUtil(filePath, "r")).getFile()
			dbConnection.copyFromCSVs(file, schemaName + "." + (((filePath.split("/"))[2]).split("."))[0], ",")
			dbConnection.commitTransaction()
		dbConnection.closeDBConnection()
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.Completed.value,"a", True)
		print("Data Loaded.")

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
		filePaths = self.getFilePaths(fileList, "csv", ResourceLocation.DatabaseLocation.value)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, ("\n").join(filePaths), LogMessage.Files.value,"a", False)
		tableHeaders = []
		for filePath in filePaths:
			fileHeader = ((FileUtil(filePath, "r")).getFileContent())[0]
			tableHeaders.append(fileHeader)
		return tableHeaders

	def getFilePaths(self, fileList, getOnly, preLocation):
		filePaths = []
		for fileName in fileList:
			if getOnly in fileName: 
				filePaths.append(preLocation + fileName)
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
				createCommand += " " + tableColumn.replace(" ","_") + " " +SQLCommandsPhrases.CharacterVarying.value
				if tableColumnIndex == 0:
					createCommand += SQLCommandsPhrases.PrimaryKey.value
				if len(tableColumns) > (tableColumnIndex + 1):
					createCommand += ","
				tableColumnIndex += 1
			createCommand += ");"
			createTableCommands.append(dropCommand)
			createTableCommands.append(createCommand)
			tableIndex += 1
		return createTableCommands

	def loadAlterSQL(self, dbConnection):
		fileList = os.listdir(ResourceLocation.AlterDatabaseSQLs.value)
		index = 0
		if len(fileList) > 0:
			print("Choose the file number:\n")
			foundSQLScript = False
			for fileName in fileList:
				index += 1
				if "sql" in fileName:
					print((str)(index) + ".) " + fileName + "\n")
					foundSQLScript = True
			if foundSQLScript == True:
				exceptionFlag = False
				choosenFileIndex = input()
				filePaths = self.getFilePaths(fileList, "sql", ResourceLocation.AlterDatabaseSQLs.value)
				try:
					filePath = filePaths[(int)(choosenFileIndex) - 1]
				except Exception as e:
					er = Error("You have chosen wrong file as an Input.", traceback.format_exc())
					er.handleError()
					exceptionFlag = True
				if 	exceptionFlag == False:
					file = FileUtil(filePath,"r")
					self.executeAndCommitToDatabase(dbConnection, file)
			else:
				print("Sorry, No SQL Files Exists in the Folder.")
		else:
			print("Sorry, No SQL Files Exists in the Folder.")


	def executeAndCommitToDatabase(self, dbConnection, sqlRead):
		dbConnection.executeSQL(sqlRead.readFile())
		dbConnection.commitTransaction()
		dbConnection.closeDBConnection()




			


