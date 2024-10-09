#!/usr/bin/env python
# coding: utf-8

# In[104]:


pip install modin[all]


# In[195]:


# Import dependencies
import os
#import pandas as pd
import modin.pandas as pd
import numpy as np
from pathlib import Path


# In[201]:


# Read the data into a Pandas DataFrame
#remote_data = pd.read_csv("./Impact_of_Remote_Work_on_Mental_Health.csv")
remote_data = pd.read_csv("C:/Users/nprab/OneDrive/Desktop/Remote-Work-and-Mental-Health/Resources/Impact_of_Remote_Work_on_Mental_Health.csv")
remote_data.head(10)


# In[ ]:


remote_data_load = pd.read_csv("./Impact_of_Remote_Work_on_Mental_Health.csv")
#remote_data_load = Path('C:/Users/nprab/OneDrive/Desktop/Remote-Work-and-Mental-Health/Impact_of_Remote_Work_on_Mental_Health.csv')
remote_data_load


# In[ ]:


# Get a brief summary of the remote_data DataFrame.
remote_data.info()


# In[ ]:


#check for duplicates
remote_data.duplicated().sum()


# In[113]:


#check for null values
remote_data.isnull().sum()


# In[115]:


#Use the fillna() function to replace NaN values in the 'Mental_Health_Condition' column with Healthy.
remote_data['Mental_Health_Condition'] = remote_data['Mental_Health_Condition'].fillna('Healthy')
remote_data


# In[117]:


remote_data['Physical_Activity'] = remote_data['Physical_Activity'].fillna('sedentary')
remote_data


# In[119]:


#check for null values
remote_data.isnull().sum()


# In[121]:


# Export the DataFrame as a CSV file.
remote_data.to_csv('challenges.csv', index=False)


# In[122]:


# Group by Region and the Stress_Level
region = pd.DataFrame(remote_data)
#stress_count = region.groupby(['Region','Stress_Level']).size().unstack(fill_value=0)

stress_count = remote_data.groupby(['Region', 'Stress_Level']).size().reset_index(name='count')

stress_count


# In[123]:


data = {
    'Region': ['Africa', 'Asia', 'Europe', 'North America', 
               'Oceania', 'South America'],
    'High': [310 , 252, 298, 256,  282 ,288],
    'Low' :[282, 281, 261, 266, 291, 264],
    'Medium' : [268, 296, 281, 255, 294, 275]    
}
region_stress = pd.DataFrame(data)
region_stress


# In[124]:


# Create the DataFrame
data = {
    'Region': ['Africa', 'Asia', 'Europe', 'North America', 
               'Oceania', 'South America'],
    'High': [310, 252, 298, 256, 282, 288],
    'Low': [282, 281, 261, 266, 291, 264],
    'Medium': [268, 296, 281, 255, 294, 275]    
}
region_stress = pd.DataFrame(data)

# Create the total column

region_stress['Total'] = region_stress[['High' ,'Low' ,'Medium']].sum(axis=1)


# Display the updated DataFrame
#print(region_stress)
region_stress


# In[128]:


region_stress.to_csv('region.csv' , index=False)


# In[130]:


# Group by Work_Location and the Mental_Health_Condition
work_loc = remote_data.groupby(['Work_Location','Mental_Health_Condition']).size().reset_index(name = 'mental_health_count')

# Sort the results to find the worst job loc
awful_work_loc_df = work_loc.sort_values(by='Work_Location')

# Print the job loc with the worst mental health condition
#print(worst_job_loc)
awful_work_loc_df


# In[133]:


# Replace the conditions
remote_data['Mental_Health_Condition'] = remote_data['Mental_Health_Condition'].replace(
    {'Anxiety': 'Unhealthy', 'Depression': 'Unhealthy', 'Burnout': 'Unhealthy'}
)

# Group by Work_Location and the modified Mental_Health_Condition
work_loc = remote_data.groupby(['Work_Location', 'Mental_Health_Condition']).size().reset_index(name='mental_health_count')

# Sort the results to find the worst job location
awful_work_loc_df = work_loc.sort_values(by='Work_Location')

# Print the DataFrame 
awful_work_loc_df


# In[135]:


awful_work_loc_df.to_csv('location.csv', index=False)


# In[136]:


data = {
    'Work_Location': ['Hybrid', 'Hybrid', 'Onsite', 'Onsite', 'Remote', 'Remote'],
    'Mental_Health_Condition': ['Healthy', 'Unhealthy', 'Healthy', 'Unhealthy', 'Healthy', 'Unhealthy'],
    'mental_health_count': [400, 1249, 376, 1261, 420, 1294]
}

# Create a DataFrame
work_loc = pd.DataFrame(data)

# Group by 'Work_Location' and 'Mental_Health_Condition' and sum the counts
grouped_df = work_loc.groupby(['Work_Location', 'Mental_Health_Condition'])['mental_health_count'].sum()

# Unstack the grouped DataFrame to create separate columns for each condition
col_split = grouped_df.unstack(fill_value=0).reset_index()

# Rename the columns for clarity
col_split.columns.name = None  # Remove the name of the columns index
work_loc_df = col_split.rename(columns={'Healthy': 'Healthy_Count', 'Unhealthy': 'Unhealthy_Count'})

# Display the resulting DataFrame
#print(work_loc_df)
work_loc_df


# In[139]:


# Export the DataFrame as a CSV file.
work_loc_df.to_csv('work_location.csv',index=False)


# In[141]:


get_ipython().system('pip install --upgrade sqlalchemy')


# In[143]:


import psycopg2
import pandas as pd
from sqlalchemy import create_engine
# username = 'postgres'
# password = 'postgres'
# hostname = 'localhost'
# port = '5432'
# db = 'remote_health_db'


# In[145]:


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/mental_health_db')


# In[147]:


#region_stress = pd.read_csv('C:/Users/nprab/OneDrive/Desktop/Remote-Work-and-Mental-Health/region.csv')
region_stress = pd.read_csv('./region.csv')
region_stress


# In[173]:


#write the contents of the DataFrame region_stress to a SQL database table named 'region'.
region_stress.to_sql( 'region', con=engine, if_exists = 'replace' )


# In[175]:


# pd.read_sql() function to execute a SQL query that selects all records from the 'region' table.
# The result of this query is returned as a new DataFrame, which allows you to work with the data in Pandas after it has been retrieved from the SQL database

pd.read_sql('select * from region', engine)


# In[177]:


work_loc_df = pd.read_csv('./work_location.csv')
work_loc_df


# In[179]:


#write the contents of the DataFrame work_loc_df to a SQL database table named 'work_location'.
work_loc_df.to_sql( 'work_location', con=engine, if_exists = 'replace' )


# In[191]:


# pd.read_sql() function to execute a SQL query that selects all records from the 'work_location' table.
# The result of this query is returned as a new DataFrame, which allows you to work with the data in Pandas after it has been retrieved from the SQL database
pd.read_sql('select * from work_location', engine)


# In[183]:


remote_data = pd.read_csv('./challenges.csv')
remote_data


# In[189]:


#write the contents of the DataFrame remote_data to a SQL database table named 'challenges'.
remote_data.to_sql( 'challenges', con=engine, if_exists = 'replace' )


# In[193]:


# pd.read_sql() function to execute a SQL query that selects all records from the 'work_location' table.
# The result of this query is returned as a new DataFrame, which allows you to work with the data in Pandas after it has been retrieved from the SQL database

pd.read_sql('select * from challenges', engine)


# In[ ]:




