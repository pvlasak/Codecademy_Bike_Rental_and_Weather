#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import numpy as np
import re
import glob
from datetime import datetime
from datetime import time
import seaborn as sns
import matplotlib.pyplot as plt 
import sqlalchemy


# Data are read by glob function and append to list. Final dataframe is create by using of `pd.concat` function

# In[2]:


list_trip_data = []

files = glob.glob("./bike-rental-starter-kit/data/JC-[0-9]*-citibike-tripdata.csv")
#print(files)[]

for file in files:
    data = pd.read_csv(file)
    list_trip_data.append(data)
df_trip_data = pd.concat(list_trip_data).reset_index().drop(labels = ["index"], axis = 1).sort_values("Start Time")


# # Bike Trip Data

# ## Diagnosis and basic analytics of bike trip data

# Dataframe containing trip data for the whole year 2016 and is assembled from montly `*.csv` files:

# In[3]:


df_trip_data.head()


# **Basic statistical values of dataframe**

# In[4]:


df_trip_data.describe()


# **Columns in the dataframe are:**

# In[5]:


df_trip_data.columns


# First dataframe row:

# In[6]:


df_trip_data.iloc[max(df_trip_data.index)]


# Last dataframe row:

# In[7]:


df_trip_data.iloc[min(df_trip_data.index)]


# **User types and counts in the dataset are:**

# In[8]:


df_trip_data["User Type"].value_counts()


# **Unique names of the start stations:**

# In[9]:


np.sort(df_trip_data["Start Station Name"].unique())


# **Unique names of the end stations:**

# In[10]:


np.sort(df_trip_data["End Station Name"].unique())


# **Data types**

# In[11]:


df_trip_data.dtypes


# Columns are renamed to get names without blanks. 

# In[12]:


df_trip_data.rename(columns = {'Trip Duration' : 'Trip_Duration',                                'Start Time' : 'Start_DateTime',                               'Stop Time' : 'Stop_DateTime',                               'Start Station ID' : 'Start_Station_ID',                               'Start Station Name' : 'Start_Station_Name',                               'Start Station Latitude' : 'Start_Station_Latitude',                                'Start Station Longitude' : 'Start_Station_Longitude',                                'End Station ID' : 'End_Station_ID',                                'End Station Name' : 'End_Station_Name',                                'End Station Latitude' : 'End_Station_Latitude',                                'End Station Longitude' : 'End_Station_Longitude',                               'Bike ID' : 'Bike_ID',                                'User Type' : 'User_Type',                                'Birth Year' : 'Birth_Year',                               }, inplace = True)


# Columns `Start_Date` and `Stop_Date` can be converted to `datetime` datatype and time and date objects can be saved as new colums.  

# In[13]:


df_trip_data['Start_Date'] = df_trip_data.apply(lambda row: datetime.strptime(row["Start_DateTime"], "%Y-%m-%d %H:%M:%S").date(), axis = 1)
df_trip_data['Start_Time'] = df_trip_data.apply(lambda row: datetime.strptime(row["Start_DateTime"], "%Y-%m-%d %H:%M:%S").time(), axis = 1)
df_trip_data['Stop_Date'] = df_trip_data.apply(lambda row: datetime.strptime(row["Stop_DateTime"], "%Y-%m-%d %H:%M:%S").date(), axis = 1)
df_trip_data['Stop_Time'] = df_trip_data.apply(lambda row: datetime.strptime(row["Stop_DateTime"], "%Y-%m-%d %H:%M:%S").time(), axis = 1)
df_trip_data['Start_DateTime'] = df_trip_data.apply(lambda row: datetime.strptime(row["Start_DateTime"], "%Y-%m-%d %H:%M:%S"), axis = 1)
df_trip_data['Stop_DateTime'] = df_trip_data.apply(lambda row: datetime.strptime(row["Stop_DateTime"], "%Y-%m-%d %H:%M:%S"), axis = 1)


# In[14]:


df_trip_data.head()


# **Analytics of the dataframe content**

# In[15]:


print("Average trip duration is {} minutes.".format(np.round(df_trip_data.Trip_Duration.mean()/60, 1)))
print("Median of the trip duration is {} minutes.".format(np.round(df_trip_data.Trip_Duration.median()/60, 1)))
print("Longest trip duration is approximately {} days.".format(np.round(df_trip_data.Trip_Duration.max()/(3600*24), 0)))
print("Shortest trip duration is approximately {} seconds.".format(np.round(df_trip_data.Trip_Duration.min(), 0)))
print("There is in total {} start stations in data set.".format(np.round(len(df_trip_data.Start_Station_Name.unique()), 0)))
print("There is in total {} stop stations in data set.".format(np.round(len(df_trip_data.End_Station_Name.unique()), 0)))
print("There is in total {} unique bike IDs in data set.".format(np.round(len(df_trip_data.Bike_ID.unique()), 0)))
print("There is in total {} bike trip records.".format(np.round(df_trip_data.Trip_Duration.count()), 0))
print("{} % of customers have not declared their gender, {} % of customers are registered as male, {} % are registered as female."       .format(np.round(df_trip_data.Gender.value_counts()[0]/df_trip_data.Trip_Duration.count()*100,1),              np.round(df_trip_data.Gender.value_counts()[1]/df_trip_data.Trip_Duration.count()*100,1),              np.round(df_trip_data.Gender.value_counts()[2]/df_trip_data.Trip_Duration.count()*100,1)))

print("There is in total {} unique start station names in dataset.".format(len(df_trip_data["Start_Station_Name"].unique())))
print("There is in total {} unique end station names in dataset.".format(len(df_trip_data["End_Station_Name"].unique())))
print("Types of customers are {}".format(df_trip_data["User_Type"].unique()))
print('Oldest customer was born in {}. This value is considered as suspicious.'.format(int(np.min(df_trip_data.Birth_Year.dropna().unique()))))
print('Youngest customer was born in {}.'.format(int(np.max(df_trip_data.Birth_Year.dropna().unique()))))


# In[16]:


np.min(df_trip_data.Birth_Year.dropna().unique())


# **Bike trip with longest duration:**

# In[17]:


df_trip_data.iloc[[df_trip_data["Trip_Duration"].idxmax()]]


# **Bike trip with shortest duration:**

# In[18]:


df_trip_data.iloc[[df_trip_data["Trip_Duration"].idxmin()]]


# **Number of duplicated rows**

# In[19]:


df_trip_data.duplicated().sum()


# **Columns containing NA values:**

# In[20]:


df_trip_data.isnull().sum()


# **Number of Non-NA values is:**

# In[21]:


df_trip_data.count()


# ## Study of  NAN values in dataframe

# NAN values can be found in the columns `User_Type` and `Birth_Year`.

# In[22]:


df_trip_data_na = df_trip_data[["User_Type", "Birth_Year", "Start_Date"]]


# In[23]:


df_trip_data_na['Month'] = pd.DatetimeIndex(df_trip_data_na['Start_Date']).month


# In[24]:


df_trip_data_na


# In[25]:


df_trip_data_na.loc[df_trip_data_na['Birth_Year'].isnull(), 'Birth_Year_NA'] = True
df_trip_data_na.loc[df_trip_data_na['User_Type'].isnull(), 'User_Type_NA'] = True


# NAN values have been found in two columns: Birth_Year and User_Type. Number of NAN values were counted for each month and plotted as bar chart. 

# In[26]:


df_trip_data_na_plot = df_trip_data_na[['Birth_Year_NA', 'User_Type_NA', 'Month']].groupby("Month").sum().reset_index()


# ### Number of NAN values in the Birth_Year column

# In[27]:


na_values_plot_birth_y = sns.catplot(data = df_trip_data_na_plot, x = 'Month', y = 'Birth_Year_NA', kind = 'bar',                             height = 4,                             aspect = 1.0)
na_values_plot_birth_y.set(title = "Number of NA Values in 'Birth_Year' column per Month");


# ### Number of NAN values in the User_Type column

# In[28]:


na_values_plot_usr_type = sns.catplot(data = df_trip_data_na_plot, x = 'Month', y = 'User_Type_NA', kind = 'bar',                             height = 4,                             aspect = 1.0)
na_values_plot_usr_type.set(title = "Number of NA Values in 'User_Type' column per Month");


# In[29]:


trip_per_month = df_trip_data_na[["Start_Date", "Month"]].groupby("Month").count().reset_index()
trip_per_month


# ### Monthly overview of bike rides

# In[30]:


trip_per_month_plot = sns.catplot(data = trip_per_month, x = 'Month', y = 'Start_Date', kind = 'bar',                             height = 4,                             aspect = 1.0)
trip_per_month_plot.set(title = "Number of bike trips column per Month");


# **Conclusion about missing values**
# 
# Number of nan values in the 'Birth_Year' column correlates with the number of bike trips in each month. Data are missing in random manner and no clear reason why data are missing. Dropping the rows with nan values should be less impactfull on analytics.

# ## Identification of suspicious values

# **Suspicious values in the Birth Year column**

# In[31]:


df_trip_data.query("Birth_Year == 1900")


# **Bike trips that took longer than 24 hours:**

# In[32]:


print("Number of bike trips that took more than 24 hours is {}. ".format(len(df_trip_data.query("Trip_Duration > 86400"))))


# top 10 longest trips:

# In[33]:


df_trip_data.query("Trip_Duration > 86400").sort_values("Trip_Duration", ascending = False).head(10)


# ## Station traffic

# Traffic intensity in each station can be estimated as a sum of entries and exits recordered in the dataset. 

# In[34]:


df_station_exits = (df_trip_data.assign(number_of_station_exits = 1)
 .groupby('Start_Station_Name')
 .agg({'number_of_station_exits': 'sum'})
 .sort_values('number_of_station_exits', ascending = False)
)


# In[35]:


df_station_entries = (df_trip_data.assign(number_of_station_entries = 1)
 .groupby('End_Station_Name')
 .agg({'number_of_station_entries': 'sum'})
 .sort_values('number_of_station_entries', ascending = False)
)

df_station_traffic = df_station_entries.join(df_station_exits, how = 'left').    assign(Total_number_of_visits = df_station_entries.number_of_station_entries + df_station_exits.number_of_station_exits).reset_index()


# ### Busiest Stations

# Busiest stations are those that have largest number of visits.

# In[36]:


busiest_stations = df_station_traffic.sort_values("Total_number_of_visits", ascending = False).head(10)
quiet_stations = df_station_traffic.sort_values("Total_number_of_visits", ascending = True).head(10)


# In[37]:


fig, axes = plt.subplots(1,1, figsize=(12,6))
(ax1) = axes
busiest_stations.plot.bar(x="End_Station_Name", y = "Total_number_of_visits", color = 'g', ax = ax1);
busiest_stations


# ### Most quiet stations

# Stations with the lowest number of visits are considered to be the most quiet ones. 

# In[38]:


quiet_stations


# In[39]:


fig, axes = plt.subplots(1,1, figsize=(12,6))
(ax1) = axes
quiet_stations.plot.bar(x="End_Station_Name", y = "Total_number_of_visits", color = 'g', ax = ax1);


# ### Inactive stations

# In[40]:


print("There is still {} stations that have only few entry records without any exit recorded."
     .format(df_station_traffic.query("Total_number_of_visits.isnull()").shape[0]))


# *Those stations are considered to be inactive.*

# In[41]:


df_station_traffic.query("Total_number_of_visits.isnull()").End_Station_Name


# ## Dataframe cleaning

# All rows with NAN values can be dropped. 

# In[42]:


df_trip_data.dropna(inplace = True) 


# `Column Birth_Year can be converted to integer datatype.`

# In[43]:


df_trip_data = df_trip_data.astype({'Birth_Year' : 'int64'})


# Main dataframe can be merged with the dataframe containing the information about the station traffic.

# In[44]:


df_trip_data_clean = df_trip_data.merge(df_station_traffic, on = "End_Station_Name")


# Trip records containing the inactive stations are dropped. 

# In[45]:


df_trip_data_clean.dropna(subset = ["Total_number_of_visits"], inplace = True)


# Suspicious record with birth year equal to 1900 is dropped.

# In[46]:


df_trip_data_clean = df_trip_data_clean.drop(df_trip_data_clean.query("Birth_Year == 1900").index, axis = 0)


# Records that took longer than 24 hours are dropped too. 

# In[47]:


df_trip_data_clean = df_trip_data_clean.drop(df_trip_data_clean.query("Trip_Duration > 86400").index, axis = 0)


# Shape of dataframe is:

# In[48]:


df_trip_data_clean.shape


# Columns `number_of_station_exits` and `Total_number_of_visits` can be converted to integer data type. 

# In[49]:


df_trip_data_clean = df_trip_data_clean.astype({'number_of_station_exits' : 'int64',                                                'Total_number_of_visits' : 'int64'})


# In[50]:


df_trip_data_clean.dtypes


# In[146]:


df_trip_data_clean.head()


# ## Preparation of dataframe data for SQL Database 

# ### Bike trips Dataframe

# ### Stations Dataframe

# In[177]:


df_stations = df_trip_data_clean[["Start_Station_ID", "Start_Station_Name", "Start_Station_Latitude", "Start_Station_Longitude"]].    drop_duplicates(subset = "Start_Station_ID").     sort_values("Start_Station_ID", ascending = True)
df_stations.rename(columns = {
                    'Start_Station_ID' : 'id', \
                    'Start_Station_Name' : 'name', \
                    'Start_Station_Latitude' : 'latitude', \
                    'Start_Station_Longitude' : 'longitude'}, inplace = True) 
df_stations.head()


# ### Users Dataframe

# In[178]:


df_users = df_trip_data_clean[["User_Type","Birth_Year", "Gender"]].drop_duplicates()


# In[179]:


ids = list(range(1, len(df_users)+1))
df_users["user_id"] = ids
df_users.head()


# ### Bike trips Dataframe

# In[180]:


df_trips = df_trip_data_clean[["Trip_Duration", "Start_DateTime", "Stop_DateTime", "Start_Station_ID", "End_Station_ID", "Bike_ID",                               "User_Type","Birth_Year", "Gender"]]


# In[181]:


df_trips = df_trips.merge(df_users, on = ["User_Type", "Birth_Year", "Gender"])
df_trips = df_trips.drop(labels = ["User_Type", "Birth_Year", "Gender"], axis = 1)
df_trips.rename(columns = { 'Trip_Duration' : 'time_duration',                            'Start_DateTime' : 'start_datetime',                            'Stop_DateTime' : 'stop_datetime',                            'Start_Station_ID' : 'start_station_id',                            'End_Station_ID' : 'end_station_id',                            'Bike_ID' : 'bike_id'}, inplace = True)
df_trips['id'] = df_trips.index
df_trips = df_trips[["id", "time_duration", "start_datetime", "stop_datetime", "start_station_id", "end_station_id", "bike_id", "user_id"]]
df_trips.head()


# ### Rename columns in Users Dataframe

# In[182]:


df_users.rename(columns = {'User_Type' : 'type',                           'Birth_Year' : 'birth_year',                            'Gender' : 'gender',                            'user_id' : 'id'}, inplace = True)
df_users


# ### Establish connection to SQL Database

# In[237]:


user = "postgres"
password = "postgres"
conn_string = f"postgresql+psycopg2://{user}:{password}@localhost:5432/Newark_Bikes"
alchemy_conn = sqlalchemy.create_engine(conn_string)


# In[184]:


#df_sql = pd.read_sql('stations', alchemy_conn, parse_dates = True)


# ### Load pandas dataframes into SQL Postgres Database

# In[185]:


with alchemy_conn.connect().execution_options(autocommit=True) as conn:
    df_users.to_sql('users', con=conn, if_exists='append', index= False)


# In[186]:


with alchemy_conn.connect().execution_options(autocommit=True) as conn:
    df_stations.to_sql('stations', con=conn, if_exists='append', index= False)


# In[187]:


with alchemy_conn.connect().execution_options(autocommit=True) as conn:
    df_trips.to_sql('bike_trips', con=conn, if_exists='append', index= False)


# # Weather Data

# In[239]:


df_weather = pd.read_csv("./bike-rental-starter-kit/data/newark_airport_2016.csv")


# In[240]:


df_weather.head()


# In[241]:


df_weather = df_weather.drop(df_weather[["STATION", "NAME", "PGTM", "WDF2", "WDF5", "WSF2", "WSF5"]], axis = 1)
df_weather.rename(columns = {
                        'DATE' : 'date', \
                        'AWND' : 'avg_wind_speed_ms', \
                        'PRCP' : 'precipitation_mm', \
                        'SNOW' : 'snowfall_mm', \
                        'SNWD' : 'snowdepth_mm',\
                        'TAVG' : 'avg_temp_f', \
                        'TMAX' : 'max_temp_f',\
                        'TMIN' : 'min_temp_f', \
                        'TSUN' : 'sunshine_min'}, inplace = True)


# In[242]:


df_weather.head()


# In[243]:


df_weather.describe()


# In[244]:


df_weather.dtypes


# ### Load pandas weather dataframe into Postgres database

# In[245]:


with alchemy_conn.connect().execution_options(autocommit=True) as conn:
    df_weather.to_sql('weather', con=conn, if_exists='append', index= False)


# In[ ]:




