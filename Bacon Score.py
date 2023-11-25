# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os

name = 'IMDB movies and people.csv'
os.chdir(r'C:\Data_Projects\Tableau Movies')
file = pd.read_csv(name)
file = file[['Title', 'Person Name', 'Person Name ID','Language','Country','IMDB Url (Person)']]

# Initialize Bacon dataframe
Bacon = pd.DataFrame()


# Filter records with actor name 'Kevin Bacon' and put it in a new dataframe
Bacon = file[file['Person Name'] == 'Kevin Bacon']
# Kevin Bacon has zero degrees of separation to Kevin Bacon
Bacon['Bacon Score']=0
# Cross off the data records that moved to the new dataframe
file = file[file['Person Name'] != 'Kevin Bacon']

# Run the loop 6 times
for i in range(6):
    # Check if there are still records in the 'file' dataframe
    if file.empty:
        break
    
    # Create a list of films based on people in the Bacon List
    film_list = Bacon.drop_duplicates('Title')['Title'].tolist()
    matching_records = file[file['Title'].isin(film_list)]
    # Anbody invovled in those films has 1+i degree of association to Kevin Bacon
    matching_records['Bacon Score'] = i + 1
    # Append the matching records to the 'Bacon' dataframe
    Bacon = pd.concat([Bacon, matching_records])
    Bacon.reset_index(drop=True, inplace=True)
    # Cross off the data records that moved to the new dataframe
    file = file[file['Title'].isin(film_list) == False]

    # Create a new list of people based on films in the updated Bacon dataframe
    personnel_list = Bacon.drop_duplicates('Person Name ID')['Person Name ID'].tolist()
    # Pick up other data records (other films) these people were invovled in
    matching_records_2 = file[file['Person Name ID'].isin(personnel_list)]
    # Add these data records also have a bacon score of 1+i (the same)
    matching_records_2['Bacon Score'] = i + 1
    # Add these additional records to the Bacon dataframe
    Bacon = pd.concat([Bacon, matching_records_2])
    Bacon.reset_index(drop=True, inplace=True)
    # Remove records with Bacon Score = 2 from the 'file' dataframe
    file = file[file['Person Name ID'].isin(personnel_list) == False]

#default anyone who is left with a score of '6+'
file['Bacon Score']='6+'
Bacon = pd.concat([Bacon, file])
Bacon.reset_index(drop=True, inplace=True)

#Export the file
Bacon.to_csv('IMDB movies and people2.csv')
