import sys, traceback
sys.path.append(".")
from connectpostgres import connectpostgres as DBConnectionUtil
from databaseutil import databaseutil as DBUtil
from databaseprocessutil import databaseprocessutil as DBProcessUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases
from error import Error as Error

util = Utility()
util.writeLogs(ResourceLocation.LogFileLocation.value,"","","w", False)
util.writeLogs(ResourceLocation.LogFileLocation.value,LogMessage.ApplicationStarted.value,"","a", True)

dbutil = DBUtil()
dbProcessUtil = DBProcessUtil()
configToBeUsed = None
schemaName = None
while True:
	try:
		configToBeUsed = (int)(input("Line no of the Config to be used: "))
		if configToBeUsed < 0:
			configToBeUsed = -(configToBeUsed)
			print("Reading Value as " + (str)(configToBeUsed))
		break
	except Exception:
		print("Require an Integer as an Input")

if configToBeUsed is not None:
	try:
		dbConnection = DBConnectionUtil(configToBeUsed, ":", ResourceLocation.DatabaseConfig.value)
		dbConnection.readConfig()
		if dbConnection.getSchemaName() is None:
			schemaName = SQLCommandsPhrases.SchemaName.value
		else:
			schemaName = dbConnection.getSchemaName()
	except Exception as e:
		er = Error("Database cofiguration not set. Please check credentials", traceback.format_exc())
		er.handleError()

	while True:  
		userInput = input("1.) Do you want to build the Schema and load the data to the DB?\n"
				+"2.) Process the Loaded records based on the Set Configuration.\n"
				+"3.) Change the DB Configuration.\n"
				+"4.) Alter DB with Alter Scripts.\n"
				+"5.) Exit\n"
				)  
		if userInput == "5":  
			util.writeLogs(ResourceLocation.LogFileLocation.value,"Exiting","","a", True)
			print("Exiting....")
			#time.sleep(1)
			#util.clear_screen()
			break
		elif userInput == "1":
			if schemaName is not None:
				try:
					util.writeLogs(ResourceLocation.LogFileLocation.value,"Loading Data","","a", False)
					dbutil.createSchema(dbConnection, schemaName)
					#time.sleep(2)
					dbutil.loadDataFromCSV(dbConnection, schemaName)
					#time.sleep(2)
					#util.clear_screen()
				except Exception as e:
					er = Error("Something went wrong. Unable to Load CSVs to Database. Please check Logs and Schema Queries generated.\n Hint:" + (str)(e), traceback.format_exc())
					er.handleError()
					dbConnection.rollBackTransaction()
			else:
				print("Please change the DB Configuration to Correct one.")
		elif userInput == "2":
			if schemaName is not None:
				try:
					util.writeLogs(ResourceLocation.LogFileLocation.value,"Processing Data","","a", False)
					dbProcessUtil.processToExtractData(dbConnection)
					print("Data Extracted")
					#time.sleep(2)
					#util.clear_screen()
				except Exception as e:
					er = Error("Something went wrong. Unable to Process the configuration files. Please check Logs and Queries generated in Process Result Folder.\n Hint:" + (str)(e), traceback.format_exc())
					er.handleError()
					dbConnection.rollBackTransaction()
			else:
				print("Please change the DB Configuration to Correct one.")
		elif userInput == "3":
			util.writeLogs(ResourceLocation.LogFileLocation.value,"Change Configuration","","a", False)
			while True:
				try:
					configToBeUsed = (int)(input("Line no of the Config to be used: "))
					if configToBeUsed < 0:
						configToBeUsed = -(configToBeUsed)
						print("Reading Value as " + (str)(configToBeUsed))
					break
				except Exception:
					print("Require an Integer as an Input")
			try:
				dbConnection = DBConnectionUtil(configToBeUsed, ":", ResourceLocation.DatabaseConfig.value)
				dbConnection.readConfig()
				if dbConnection.getSchemaName() is None:
					schemaName = SQLCommandsPhrases.SchemaName.value
				else:
					schemaName = dbConnection.getSchemaName()
			except Exception as e:
				schemaName = None
				configToBeUsed = None
				er = Error("Database cofiguration not set. Please check credentials or the Entry.", traceback.format_exc())
				er.handleError()
				dbConnection.rollBackTransaction()
			#time.sleep(2)
			#util.clear_screen()
		elif userInput == "4":
			if schemaName is not None:
				try:
					util.writeLogs(ResourceLocation.LogFileLocation.value,"Alter DB","","a", False)
					dbutil.loadAlterSQL(dbConnection)
					print("Alter Table Finished")
					#time.sleep(2)
					#util.clear_screen()
				except Exception as e:
					er = Error("Something went wrong. Unable to Process the Alterable file. Please check Logs.\n Hint:" + (str)(e), traceback.format_exc())
					er.handleError()
					dbConnection.rollBackTransaction()
			else: 
				print("Please change the DB Configuration to Correct one.")
else:
	print("Ended")



