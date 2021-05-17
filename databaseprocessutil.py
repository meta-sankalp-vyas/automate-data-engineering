import sys
sys.path.append(".")
from fileutil import fileutil as FileUtil
from utility import utility as Utility
from utility import processlocation as ProcessLocation

class databaseprocessutil:

    def processToExtractData(self, dbConnection):
        print("Processing....")
        utility = Utility()
        queriesConfigList = self.getConfiguration(ProcessLocation.ProcessConfigExtractData.value)
        queries = self.createQueries(queriesConfigList, "simple")
        utility.writeCommandSqlScript(("\n").join(queries), ProcessLocation.ProcessResultExtractDataQuery.value)
        queriesIndex = 1
        for query in queries:
            fileName = ProcessLocation.ProcessResultExtractData.value + "Query" + (str)(queriesIndex) + ".csv"
            file = FileUtil(fileName, "w")
            dbConnection.copyToCSVs(file.getFile(), query, ",")
            queriesIndex += 1
        print("Processing Completed.")

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
                    queryToExecute = "SELECT * FROM " + configInputs[0]
                    if (configInputs[1] and configInputs[1].strip() and configInputs[2] and configInputs[2].strip() 
                        and configInputs[3] and configInputs[3].strip()):
                        queryToExecute += "  " + configInputs[2] + " " + configInputs[1] + " ON " + configInputs[3]
                    if (configInputs[4] and configInputs[4].strip()):
                        queryToExecute += " WHERE " + configInputs[4]
                    if (configInputs[5] and configInputs[5].strip()):
                        queryToExecute += " ORDER BY " + configInputs[5]
                    if (configInputs[6] and configInputs[6].strip()):
                        queryToExecute += " LIMIT " + configInputs[6]
                    queries.append(queryToExecute)
                index += 1
        return queries