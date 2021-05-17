import sys
sys.path.append(".")
from connectpostgres import connectpostgres as DBConnectionUtil
from databaseutil import databaseutil as DBUtil
from databaseprocessutil import databaseprocessutil as DBProcessUtil
<<<<<<< HEAD
=======
from fileutil import fileutil as FileUtil
>>>>>>> cb94381d1e5b1b21e304c8cdfaa05862365ebc3e
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases

# Establish a connection to the database by creating a cursor object
# The PostgreSQL server must be accessed through the PostgreSQL APP or Terminal Shell

# Config Line in the databas-config file that is to be used to establish the connection
util = Utility()
util.writeLogs(ResourceLocation.LogFileLocation.value,"","","w", False)
util.writeLogs(ResourceLocation.LogFileLocation.value,LogMessage.ApplicationStarted.value,"","a", True)

dbutil = DBUtil()
dbProcessUtil = DBProcessUtil()
configToBeUsed = input("Line no of the Config to be used: ")
dbConnection = DBConnectionUtil(configToBeUsed, ":", ResourceLocation.DatabaseConfig.value)
dbConnection.readConfig()
if dbConnection.getSchemaName() is None:
    schemaName = SQLCommandsPhrases.SchemaName.value
else:
    schemaName = dbConnection.getSchemaName()

while True:  
    userInput = input("1.) Do you want to build the Schema and load the to the DB?\n"
                    +"2.) Process the Loaded records based on the Set Configuration.\n"
                    +"3.) Change the DB Configuration.\n"
                    +"4.) Exit\n"
                    )  
    if userInput == "4":  
        util.writeLogs(ResourceLocation.LogFileLocation.value,"Exiting","","a", True)
        util.clear_screen()
        break
    elif userInput == "1":
        util.writeLogs(ResourceLocation.LogFileLocation.value,"Loading Data","","a", False)
        dbutil.createSchema(dbConnection, schemaName)
        dbutil.loadDataFromCSV(dbConnection, schemaName)
        util.clear_screen()
    elif userInput == "2":
        util.writeLogs(ResourceLocation.LogFileLocation.value,"Processing Data","","a", False)
        dbProcessUtil.processToExtractData(dbConnection)
        util.clear_screen()
    elif userInput == "3":
        util.writeLogs(ResourceLocation.LogFileLocation.value,"Change Configuration","","a", False)
        configToBeUsed = input("Line no of the Config to be used: ")
        dbConnection = DBConnectionUtil(configToBeUsed, ":", ResourceLocation.DatabaseConfig.value)
        util.clear_screen()
