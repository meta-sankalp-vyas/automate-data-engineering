import time
import enum
import sys
sys.path.append(".")
from fileutil import fileutil as FileUtil

class logmessage(enum.Enum):
	ApplicationStarted = "Application Started"
	Seperator = "========================================================="
	Completed = "Execution Completed."
	DBConnection = "Establishing Connection with the DB..."
	DBConnectionSuccess = "Successfully Connected."
	DBConnectionError = "Error. Connection not established with the DB."
	Files = "Files: "
	DBDatabaseCreationCommands = "Database Table Commands Created: "
	DBDatabaseSQLScriptCreated = "SQL Script Logged."
	DBDatabaseCreation = "Creating Database Schema..."
	DBDatabaseCreationSuccess = "Database Created."
	DBDatabaseCreationError = "Error. Database Creation encountered a problem."

class resourcelocation(enum.Enum):
	LogFileLocation = "./logs/log.txt"
	DatabaseLocation = "./database-csvs/"
	DatabaseScript = "./logs/SQLScriptTable.sql"
	DatabaseRecordsScript = "./logs/SQLScriptTableRecords.sql"
	DatabaseConfig = "database-config.txt"

class processlocation(enum.Enum):
	ProcessConfigExtractData = "./process-configurations/extract-data.csv"
	ProcessConfigExtractJoinedTableData = "./process-configurations/extract-join-table-data.csv"
	ProcessResultExtractData = "./process-result/extract-data/"
	ProcessResultExtractJoinedTableData = "./process-result/extract-join-table-data/"
	ProcessResultExtractDataQuery = "./process-result/extract-data/Queries.sql"
	ProcessResultExtractJoinedTableDataQuery = "./process-result/extract-join-table-data/Queries.sql"

class sqlcommandsphrases(enum.Enum):
	CreateSchema = "CREATE SCHEMA IF NOT EXISTS "
	DropSchema = "DROP SCHEMA IF EXISTS "
	SchemaName = "sankalp_dev"
	DropTable = "DROP TABLE IF EXISTS "
	CreateTable = "CREATE TABLE IF NOT EXISTS "
	Cascade = " CASCADE"
	PrimaryKey = " PRIMARY KEY"
	CharacterVarying = " character varying "
	Copy = "COPY "
	FROM = " FROM "
	CopyCSVDelimiter= "DELIMITER ',' CSV HEADER;"

class utility:

	def writeLogs(self, fileLocation, content, message, access, doComplete):
		t = time.localtime()
		logCommands = FileUtil(fileLocation,access)
		logCommands.writeFileContent(time.strftime("%H:%M:%S", t) + " : " + message + "\n" + content + "\n")
		if doComplete == True:
			logCommands.writeFileContent("\n" + logmessage.Seperator.value + "\n")

	def writeCommandSqlScript(self, content, fileLocation):
		fileTo = FileUtil(fileLocation, "w")
		fileTo.writeFileContent(content)