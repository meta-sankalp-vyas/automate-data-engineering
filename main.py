import sys
sys.path.append(".")
from connectpostgres import connectpostgres as DBConnectionUtil
from databaseutil import databaseutil as DBUtil
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases

# Establish a connection to the database by creating a cursor object
# The PostgreSQL server must be accessed through the PostgreSQL APP or Terminal Shell

# Config Line in the databas-config file that is to be used to establish the connection
util = Utility()
util.writeLogs(ResourceLocation.LogFileLocation.value,LogMessage.ApplicationStarted.value,"","w")
configToBeUsed = input("Line no of the Config to be used: ")

dbConnection = DBConnectionUtil(configToBeUsed, ":", "database-config.txt")
#result = dbConnection.executeSQLAndFetchAll("""SELECT * FROM \"sankalp-dev\".\"Certification Status\" LIMIT 10""")
#print(result)
#dbConnection.closeDBConnection()

dbutil = DBUtil()
dbutil.createDataTablesSQLScript(SQLCommandsPhrases.SchemaName.value)
sqlRead = FileUtil(ResourceLocation.DatabaseScript.value, "r")
util.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.DBDatabaseCreation.value,"a")		
dbConnection.executeSQL(sqlRead.readFile())
dbConnection.commitTransaction()
dbConnection.closeDBConnection()
util.writeLogs(ResourceLocation.LogFileLocation.value, "", LogMessage.Completed.value,"a")