# automate-data-engineering

Issue: 
* In data comparison of reports extracted from different teams the basic model for comparison is VLOOKUP on Excel Sheet Validation.
* Applying VLookups can be transformed into a Template Based Sheet, but that would just increase the number of templates that the Team would have to manage.
* Need an automated solution, which based on the configuration provided will extract the related data from the CSV 

Solution: 
* The user will provide CSVs at a location.
* Based on a certain configuration, the records present in CSV will be compared and a resulted extracted CSV will be generated in a different location.
* Configuration and the source CSV will be kept as a safe keep, for future use. Hence saving time every time a new source file is provided to the Credential Engineering team to do the same comparison.
* PostgreSQL will be used to do a comparison of data instead of Excel Sheet VLookUps. Since it provides more options to create complex query formation, Users can keep a certain set of queries that can work upon the data-set they have loaded into the database.
* Since the Table creation is a manual task in a Database, that would need to be updated for each set of new Files that the system will be encountering, need an automated solution, which will create the basic Table and Columns in the database based on the CSV provided.
* Alter SQL script execution will be required once the basic data structure based on the CSVs provided is created.
* Based on the Configuration provided in a CSV file format, Queries will be created, and data will be extracted from the Database.


Steps:
* Download PostgreSQL.
* Download Python from this link (https://www.python.org/downloads/). You would need to configure environment variables in your PC. Run Command “pip install psycopg2”
* Clone this repository  git@github.com:meta-sankalp-vyas/automate-data-engineering.git.
* Put the CSVs in the  “database-csvs” folder.
* The “process-configurations” folder will contain the Query configuration that needs to be created. An example configuration CSV is at location "process-configurations/exract-data.csv", note that the Quote Character is “|” and the Separator is “,”. “sankalp_vyas_test” is the name of the Schema.
* You would need to specify your Postgres credential in “database-config.txt” file. You can use different schema names for different comparisons.
* To start the application, at the root folder, initiate Command Prompt and execute “python main.py”
* It will ask for a configuration, provide the entry no of the configuration you have set in the “database-config.txt” like for example in the above image, the entry is 1, but the line no is 2.
* You will be prompted a basic command option at the Terminal.
* If your CSVs are not loaded yet in the database, choose option 1, it will load all the CSVs present in “database-csvs” to the Postgres Server configuration provided. If the Schema or Table already exists, the table will be dropped first then recreated and records will be loaded. You can get the Schema Script created in the “logs” folder’s “SQLScriptTable.sql” file.
* Option 2 will process the configuration you have set in the “process-configurations” folder and write the possible records in the “process-result\extract-data” folder.
* If you have more than 1 configuration in “database-config.txt”, you can change the configuration using 3rd option.
* Once your CSVs are loaded, and you want to Alter your DB-Schema created in a specific manner, you can write a SQL Script and paste it in the “alter-scripts” folder, by choosing 4th Option you can execute the Alter Script to run on your PostgreSQL Server.