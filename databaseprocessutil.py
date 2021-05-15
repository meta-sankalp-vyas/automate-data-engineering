import os
import sys
import pandas as pd
sys.path.append(".")
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import logmessage as LogMessage
from utility import resourcelocation as ResourceLocation
from utility import processlocation as ProcessLocation
from utility import sqlcommandsphrases as SQLCommandsPhrases

class databaseprocessutil:

    def processToExtractData(self, dbConnection):
        print("Processing")
        utility = Utility()
        queriesConfigList = self.getConfiguration(ProcessLocation.ProcessConfigExtractData.value)
        queries = self.createQueries(queriesConfigList, "simple")
        utility.writeCommandSqlScript(("\n").join(queries), ProcessLocation.ProcessResultExtractDataQuery.value)
        queriesIndex = 1
        for query in queries:
            result = dbConnection.executeSQLAndFetchAll(query)
            print(result)
            fileName = ProcessLocation.ProcessResultExtractData.value + "Query" + (str)(queriesIndex) + ".csv"
            #utility.writeCommandSqlScript(("\n").join(result), (str)(fileName))
            df = pd.DataFrame(result)
            df.to_csv(fileName)
            queriesIndex += 1
        print("Processing Completed")
            

    def processToExtractJoinedData(self):
        print("Processing")

    def getConfiguration(self, fileLocation):
        fileRead = FileUtil(fileLocation, "r")
        return fileRead.getFileContent()

    def createQueries(self, queriesConfigList, method):
        queries = []
        if method == "simple":
            index = 0
            for queryConfig in queriesConfigList:
                if index != 0:
                    configInputs = queryConfig.split(",")
                    print(configInputs)
                    queryToExecute = "SELECT * FROM " + configInputs[0]
                    if (configInputs[1] and configInputs[1].strip()):
                        queryToExecute += " WHERE " + configInputs[1]
                    if (configInputs[2] and configInputs[2].strip()):
                        queryToExecute += " ORDER BY " + configInputs[2]
                    if (configInputs[3] and configInputs[3].strip()):
                        queryToExecute += " LIMIT " + configInputs[3]
                    queries.append(queryToExecute)
                    print(queryToExecute)
                index += 1
        else:
            print("Hello")
        return queries