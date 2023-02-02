Data about bike trips from multiple CSV files have been loaded as single Pandas Dataframe, which 
has been diagnozed with regard to the blank fields and suspicious data.
Data types in each individual column have been checked and converted to desired data type if necessary.

Sqlalchemy module is used to establish connection to Postgres SQL Database running on localhost. 
Schema of SQL Database was designed and suitable constraints were defined. 
Dataframes from Pandas were successfuly imported into the Postgres via sqlalchemy and several 
SQL queries were created to get interesting outcomes. SQL commands sequence is saved in attech .sql file. 








