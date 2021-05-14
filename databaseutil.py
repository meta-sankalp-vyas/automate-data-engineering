import os
import sys
sys.path.append(".")
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases

class databaseutil:

	def createDataTablesSQLScript(self, schemaName):
		utility = Utility()
		fileList = os.listdir(ResourceLocation.DatabaseLocation.value)
		tableHeaders = self.getTableHeader(fileList)
		createTableCommands = self.createCommandsFromHeaders(tableHeaders, fileList, schemaName)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, ("\n").join(createTableCommands), LogMessage.DBDatabaseCreationCommands.value,"a")
		self.writeCommandSqlScript(("\n").join(createTableCommands), ResourceLocation.DatabaseScript.value)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.DBDatabaseSQLScriptCreated.value,"a")

	def getTableHeader(self, fileList):
		utility = Utility()
		filePaths = []
		for fileName in fileList:
			if "csv" in fileName: 
				filePaths.append(ResourceLocation.DatabaseLocation.value + fileName)
		utility.writeLogs(ResourceLocation.LogFileLocation.value, ("\n").join(filePaths), LogMessage.Files.value,"a")
		tableHeaders = []
		for filePath in filePaths:
			fileHeader = ((FileUtil(filePath, "r")).getFileContent())[0]
			tableHeaders.append(fileHeader)
		return tableHeaders
		
	def createCommandsFromHeaders(self, tableHeaders, fileList, schemaName):
		createTableCommands = []
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
	
	def writeCommandSqlScript(self, content, fileLocation):
		sqlScript = FileUtil(ResourceLocation.DatabaseScript.value, "w")
		sqlScript.writeFileContect(content)




			


