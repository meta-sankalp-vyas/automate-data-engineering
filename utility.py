import time
import enum
import sys
sys.path.append(".")
from fileutil import fileutil as FileUtil

class logmessage(enum.Enum):
	ApplicationStarted = " Application Started "
	Seperator = "========================================================="
	Completed = "Execution Completed."
	DBConnection = "Establishing Connection with the DB..."
	DBConnectionError = "Error. Connection not established with the DB."
	Files = "Files: "
	DBDatabaseCreationCommands = "Database Table Commands Created: "
	DBDatabaseSQLScriptCreated = "SQL Script Logged."
	DBDatabaseCreation = "Creating Database Schema..."
	DBDatabaseCreationError = "Error. Database Creation encountered a problem."

class resourcelocation(enum.Enum):
	LogFileLocation = "./logs/log.txt"
	DatabaseLocation = "./database-csvs/"
	DatabaseScript = "./logs/SQLScriptTable.sql"

class sqlcommandsphrases(enum.Enum):
	CreateSchema = "CREATE SCHEMA "
	SchemaName = "sankalp_dev"
	DropTable = "DROP TABLE IF EXISTS "
	CreateTable = "CREATE TABLE IF NOT EXISTS "
	Cascade = " CASCADE"
	PrimaryKey = " PRIMARY KEY"
	CharacterVarying = " character varying "

class utility:

	def writeLogs(self, fileLocation, content, message, access):
		t = time.localtime()
		logCommands = FileUtil(fileLocation,access)
		logCommands.writeFileContect(time.strftime("%H:%M:%S", t) + " : " + message + "\n" + content + "\n" + logmessage.Seperator.value + "\n")