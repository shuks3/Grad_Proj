"""
Project Name :
Group Number :14
Group Members :
    1. Gadige Vishal Sai
    2. Li-Hsuan Hsieh
    3. Soumya Shukla
    4. Chinmay Katpatal
File Name : user_interface.py
"""

### Importing the packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from IPython.display import display, HTML
import pandas as pd
import sqlite3
from sqlite3 import Error

### Global variable
filename = 'Dataset/imdb.csv'

### Fetch data from the csv file
def fetch_data_from_csv(filename):
    ### Initialize values
    titles = []
    rows = []
    
    ### Reading the csv file
    with open(filename, 'r') as csv_file:
        ### Creating a csv reader object
        csv_reader = csv.reader(csv_file)
        
        ### Extracting the titles from the first row
        titles = next(csv_reader)
        
        ### Extracting each record one by one
        for each_record in csv_reader:
            rows.append(each_record)
    return titles, rows

### Helper function to create a connection
def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)
    return conn

### Helper function to create a table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

### Helper function to execute a sql statement
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()
    return rows

### Convert list to a string seperated with commas
def list_to_string(rows, index):
    string_data = []
    for each_row in rows:
        string_value = each_row[index].lstrip("[\"")
        string_value = string_value.rstrip("]\"")
        string_data.append(string_value)
    return string_data

### Fetching id data from the csv file
def fetch_id():
    titles, rows = fetch_data_from_csv(filename)
    id_index = titles.index('id')
    id_data = []
    for each_row in rows:
        id_data.append(int(each_row[id_index]))
    return id_data

### Fetching title data from the csv file
def fetch_title():
    titles, rows = fetch_data_from_csv(filename)
    title_index = titles.index('title')
    title_data = []
    for each_row in rows:
        title_data.append(each_row[title_index])
    return title_data

### Fetching year data from the csv file
def fetch_year():
    titles, rows = fetch_data_from_csv(filename)
    year_index = titles.index('year')
    year_data = []
    for each_row in rows:
        if each_row[year_index] != '':
            year_data.append(int(each_row[year_index]))
        else:
            year_data.append(0)
    return year_data

### Fetching kind data from the csv file
def fetch_kind():
    titles, rows = fetch_data_from_csv(filename)
    kind_index = titles.index('kind')
    kind_data = []
    for each_row in rows:
        kind_data.append(each_row[kind_index])
    return kind_data

### Fetching genre data from the csv file
def fetch_genre():
    titles, rows = fetch_data_from_csv(filename)
    genre_index = titles.index('genre')
    genre_data = []
    for each_row in rows:
        if each_row[genre_index] != '':
            genre_data.append(each_row[genre_index])
        else:
            genre_data.append('')
    
    ### Converting the list to string seperated with the commas
    for index in range(len(genre_data)):
        string_value = genre_data[index].lstrip("[\"")
        string_value = string_value.rstrip("]\"")
        genre_data[index] = string_value
    return genre_data

### Fetching rating data from the csv file
def fetch_rating():
    titles, rows = fetch_data_from_csv(filename)
    rating_index = titles.index('rating')
    rating_data = []
    for each_row in rows:
        if each_row[rating_index] != '':
            rating_data.append(float(each_row[rating_index]))
        else:
            rating_data.append(0)
    return rating_data

### Fetching vote data from the csv file
def fetch_vote():
    titles, rows = fetch_data_from_csv(filename)
    vote_index = titles.index('vote')
    vote_data = []
    for each_row in rows:
        if each_row[vote_index] != '':
            vote_data.append(int(each_row[vote_index]))
        else:
            vote_data.append(0)
    return vote_data

### Fetch country data from the csv file
def fetch_country():
    titles, rows = fetch_data_from_csv(filename)
    country_index = titles.index('country')
    country_data = []
    for each_row in rows:
        if each_row[country_index] != '':
            country_data.append(each_row[country_index])
        else:
            country_data.append('')
    
    ### Converting the list to string seperated with the commas
    for index in range(len(country_data)):
        string_value = country_data[index].lstrip("[\"")
        string_value = string_value.rstrip("]\"")
        country_data[index] = string_value
    return country_data

### Fetch language data from the csv file
def fetch_language():
    titles, rows = fetch_data_from_csv(filename)
    language_index = titles.index('language')
    language_data = []
    for each_row in rows:
        if each_row[language_index] != '':
            language_data.append(each_row[language_index])
        else:
            language_data.append('')
    
    ### Converting the list to string seperated with the commas
    for index in range(len(language_data)):
        string_value = language_data[index].lstrip("[\"")
        string_value = string_value.rstrip("]\"")
        language_data[index] = string_value
    return language_data

### Fetch runtime data from the csv file
def fetch_runtime():
    titles, rows = fetch_data_from_csv(filename)
    runtime_index = titles.index('runtime')
    runtime_data = []
    for each_row in rows:
        if each_row[runtime_index] != '':
            runtime_data.append(int(each_row[runtime_index]))
        else:
            runtime_data.append(0)
    return runtime_data

### Insert data into IMDB table
def insert_into_imdb(conn, values):
    sql = "INSERT INTO IMDB(Id, Title, Year, Kind, Genre, Rating, Vote, Country, Language, Runtime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid

### Create a non_normalized database
def create_non_normalized_database_table(conn):
    ### Create Table - IMDB
    create_imdb = "CREATE TABLE IMDB (Id INT, Title VARCHAR2(100), Year INT, Kind VARCHAR2(100), Genre VARCHAR2(200), Rating DECIMAL(4, 2), Vote INT, Country VARCHAR2(200), Language VARCHAR2(200), Runtime INT, PRIMARY KEY (Id));"
    with conn:
        create_table(conn, create_imdb)
    
    ### Fetch all the values
    id_data = fetch_id()
    title_data = fetch_title()
    year_data = fetch_year()
    kind_data = fetch_kind()
    genre_data = fetch_genre()
    rating_data = fetch_rating()
    vote_data = fetch_vote()
    country_data = fetch_country()
    language_data = fetch_language()
    runtime_data = fetch_runtime()
    
    ### Insert data into IMDB
    for index in range(len(id_data)):
        row_values = (id_data[index], title_data[index], year_data[index], kind_data[index], genre_data[index], rating_data[index], vote_data[index], country_data[index], language_data[index], runtime_data[index])
        insert_into_imdb(conn, row_values)
    
    ### Save the data
    conn.commit()

### Insert data into Titles table
def insert_into_titles(conn, values):
    sql = "INSERT INTO Titles(TitleId, Title, Year, Rating, Vote, Runtime) VALUES(?, ?, ?, ?, ?, ?);"
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid

### Create a normalized database and add Titles table - id, title, year, rating, vote, runtime
def create_titles_table(conn):
    ### Create Table - Titles
    create_titles = "CREATE TABLE Titles (TitleId INT, Title VARCHAR2(200) NOT NULL, Year INT, Rating DECIMAL(4, 2) NOT NULL, Vote INT NOT NULL, Runtime INT NOT NULL, PRIMARY KEY (TitleId));"
    with conn:
        create_table(conn, create_titles)
    
    ### Fetch all the values
    id_data = fetch_id()
    title_data = fetch_title()
    year_data = fetch_year()
    rating_data = fetch_rating()
    vote_data = fetch_vote()
    runtime_data = fetch_runtime()
    
    ### Insert data into Titles
    for index in range(len(id_data)):
        row_values = (id_data[index], title_data[index], year_data[index], rating_data[index], vote_data[index], runtime_data[index])
        insert_into_titles(conn, row_values)
        
    ### Save the data
    conn.commit()

### Insert data into TitleDetails table
def insert_into_title_details(conn, values):
    sql = "INSERT INTO TitleDetails(Id, TitleId, Title, Kind, Genre, Country, Language) VALUES(?, ?, ?, ?, ?, ?, ?);"
    cur = conn.cursor()
    cur.execute(sql, values)
    return cur.lastrowid

### Add TitleDetails table - TitleId, Title, Kind, Genre, Country, Language
def create_title_details_table(conn):
    ### Create Table - TitleDetails
    create_title_details = "CREATE TABLE TitleDetails (Id INT, TitleId INT, Title VARCHAR2(200) NOT NULL, Kind VARCHAR2(100) NOT NULL, Genre VARCHAR2(100), Country VARCHAR2(100), Language VARCHAR2(100), PRIMARY KEY (Id), FOREIGN KEY (TitleID) REFERENCES Titles(TitleId));"
    with conn:
        create_table(conn, create_title_details)
    
    
    ### Fetch all the values
    title_id_data = fetch_id()
    title_data = fetch_title()
    kind_data = fetch_kind()
    genre_data = fetch_genre()
    country_data = fetch_country()
    language_data = fetch_language()
    
    ### Modify kind_data
    for index in range(len(kind_data)):
        if 'movie' in kind_data[index]:
            kind_data[index] = 'movie'
        else:
            kind_data[index] = 'tv series'
    
    ### Modify genre_data
    modified_genre = []
    for genres in genre_data:
        if genres != '':
            modified_genre.append(genres.split(', '))
        else:
            modified_genre.append(['Unknown'])
    
    ### Modify country_data
    modified_country = []
    for countries in country_data:
        if countries != '':
            modified_country.append(countries.split(', '))
        else:
            modified_country.append(['Unknown'])
    
    ### Modify language_data
    modified_language = []
    for languages in language_data:
        if languages != '':
            modified_language.append(languages.split(', '))
        else:
            modified_language.append(['Unknown'])

    ### Insert data into TitleDetails
    id = 1
    for index in range(len(title_data)):
        for each_genre in modified_genre[index]:
            for each_country in modified_country[index]:
                for each_language in modified_language[index]:
                    row_values = (id, title_id_data[index], title_data[index], kind_data[index], each_genre, each_country, each_language)
                    insert_into_title_details(conn, row_values)
                    id += 1
    
    ### Save the data
    conn.commit()
                    
### Functions to be called in analysis.py    
def setup_database():
    ### Create a connection for the non_normalized database and create IMDB table
    non_normalized_connection = create_connection('non_normalized.db', True)
    create_non_normalized_database_table(non_normalized_connection)
    non_normalized_connection.close()
    
    ### Create a connection for the normalized database and create Titles, TitleDetails table
    normalized_connection = create_connection('normalized.db', True)
    create_titles_table(normalized_connection)
    create_title_details_table(normalized_connection)
    normalized_connection.close()