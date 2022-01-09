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

### Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from tqdm import tqdm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

### Importing the module
import backend



### Understanding the column - Kind
def plot_kind():
    ### Create a connection to the normalized database to use TitleDetails
    normalized_connection = backend.create_connection('normalized.db', False)
    with normalized_connection:
        sql_statement = "SELECT Kind, COUNT(Kind) AS Count FROM TitleDetails WHERE Kind != 'Unknown' GROUP BY Kind;"
        kind_df = pd.read_sql_query(sql_statement, normalized_connection)
        
    ### Plotting a bar chart for the variable - Kind
    kind_type = kind_df['Kind']
    kind_count = kind_df['Count']
    fig = plt.figure(figsize = (10, 7))
    plt.bar(kind_type, kind_count, color ='red',width = 0.4)
    plt.xlabel("Kind of shows in Netflix")
    plt.ylabel("Frequency of each kind")
    plt.title("Distribution of the variable - Kind")
    plt.savefig("Images/KindDistribution")
    
    ### Close the connection 
    normalized_connection.close()

### Understanding the column - Genre
def plot_genre():
    ### Create a connection to the normalized database to use TitleDetails
    normalized_connection = backend.create_connection('normalized.db', False)
    with normalized_connection:
        sql_statement = "SELECT Genre, COUNT(Genre) AS Count FROM TitleDetails WHERE Genre != 'Unknown' GROUP BY Genre ORDER BY Count DESC LIMIT 10;"
        genre_df = pd.read_sql_query(sql_statement, normalized_connection)
    
    ### Plotting a pie chart for the top 10 genres 
    genre_type = genre_df['Genre']
    genre_value = genre_df['Count']
    pie_explode = [0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig = plt.figure(figsize = (10, 7))
    plt.pie(genre_value, labels = genre_type, explode = pie_explode)
    plt.title("Understanding the distribution of top 10 genres")
    plt.savefig("Images/GenreDistribution")
    
    ### Close the connection
    normalized_connection.close()

### Understand the column - Year
def plot_year():
    ### Create a connection to the normalized database to use TitleDetails
    normalized_connection = backend.create_connection('normalized.db', False)
    with normalized_connection:
        sql_statement = "SELECT Year, COUNT(Year) AS Count FROM Titles WHERE Year != 0 GROUP BY Year ORDER BY Year DESC LIMIT 10;"
        year_df = pd.read_sql_query(sql_statement, normalized_connection)
        
    ### Plotting a bar chart for the past 10 years
    year_type = year_df['Year']
    year_value = year_df['Count']
    fig = plt.figure(figsize = (10, 7))
    plt.bar(year_type, year_value, color ='red', width = 0.4)
    plt.xlabel("Years")
    plt.ylabel("Shows released per year")
    plt.title("Shows released between 2014 and 2023")
    plt.savefig("Images/YearDistribution")
    
    
### Time Series Analysis - Movies
def plot_tsa_for_movies():
    year_key = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1919, 1918, 1916, 1914, 1913, 1910, 1905, 0]
    year_values = [2, 14, 102, 129, 118, 119, 103, 86, 93, 66, 73, 69, 45, 69, 44, 45, 57, 71, 301, 663, 683, 643, 623, 535, 481, 392, 317, 299, 234, 218, 206, 151, 144, 122, 117, 143, 129, 97, 96, 79, 77, 72, 83, 79, 72, 65, 56, 65, 49, 78, 73, 76, 54, 46, 48, 50, 43, 35, 41, 37, 32, 33, 22, 35, 71, 29, 32, 16, 19, 15, 18, 15, 18, 14, 13, 10, 15, 11, 15, 10, 8, 10, 4, 8, 8, 12, 6, 6, 2, 6, 4, 7, 7, 5, 4, 6, 5, 5, 4, 2, 1, 2, 1, 4, 1, 1, 1, 1, 5, 70]
    movies_released = [2, 12, 55, 55, 49, 44, 42, 22, 35, 32, 26, 39, 14, 31, 20, 22, 20, 26, 87, 269, 312, 323, 329, 286, 261, 205, 187, 167, 152, 132, 119, 94, 81, 74, 81, 97, 84, 68, 72, 62, 54, 52, 68, 58, 60, 50, 45, 55, 40, 58, 61, 68, 43, 40, 36, 39, 36, 30, 38, 34, 29, 28, 19, 32, 24, 25, 30, 15, 16, 14, 16, 11, 16, 14, 13, 9, 14, 11, 15, 10, 8, 9, 3, 7, 8, 7, 5, 6, 2, 6, 4, 7, 7, 5, 4, 6, 5, 5, 4, 2, 1, 2, 1, 4, 1, 1, 1, 1, 5, 0]
    tv_series_released = [0, 1, 17, 29, 21, 10, 14, 9, 17, 11, 19, 3, 9, 16, 5, 0, 7, 7, 9, 40, 41, 46, 54, 36, 36, 27, 25, 22, 17, 14, 29, 8, 11, 6, 6, 11, 13, 12, 5, 5, 2, 1, 5, 2, 5, 5, 4, 4, 2, 10, 4, 5, 6, 1, 5, 1, 3, 4, 0, 1, 2, 5, 1, 1, 46, 3, 2, 0, 2, 1, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    drama_released = [0, 2, 39, 50, 42, 38, 35, 23, 27, 23, 17, 18, 16, 25, 15, 9, 20, 16, 59, 202, 239, 241, 269, 245, 199, 173, 157, 117, 109, 109, 97, 69, 59, 54, 58, 60, 46, 38, 40, 37, 39, 30, 34, 37, 38, 35, 29, 36, 29, 43, 41, 41, 28, 30, 26, 20, 16, 16, 22, 22, 14, 21, 14, 23, 57, 13, 21, 8, 10, 10, 10, 10, 12, 8, 7, 6, 8, 10, 10, 4, 3, 5, 3, 3, 3, 9, 3, 2, 0, 3, 2, 4, 2, 3, 3, 5, 4, 3, 2, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
    comedy_released = [0, 3, 22, 33, 27, 25, 27, 34, 27, 22, 31, 23, 9, 24, 14, 13, 7, 8, 65, 167, 176, 172, 177, 152, 139, 113, 92, 110, 69, 72, 61, 47, 42, 38, 33, 48, 40, 33, 30, 27, 25, 24, 22, 24, 22, 21, 13, 18, 14, 13, 16, 18, 11, 12, 17, 16, 18, 12, 12, 12, 10, 13, 5, 12, 8, 5, 10, 1, 8, 3, 7, 5, 5, 4, 4, 3, 7, 0, 2, 2, 3, 5, 1, 3, 4, 3, 3, 3, 0, 2, 2, 1, 2, 3, 1, 2, 0, 1, 1, 2, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0]
    data = {'year_key': year_key,
        'year_values': year_values,
        'movies_released': movies_released,
        'tv_series_released': tv_series_released,
        'drama_released': drama_released,
        'comedy_released': comedy_released}
    netflix_data = pd.DataFrame(data)
    movies = netflix_data[["movies_released"]]
    series = netflix_data[["tv_series_released"]]
    drama = netflix_data[["drama_released"]]
    comedy = netflix_data[["comedy_released"]]
    decompose = seasonal_decompose(movies, model = 'additive', period = 7)
    plt = decompose.plot()
    plt.savefig("Images/MovieTimeSeries")
    
### Time Series Analysis - TV Series
def plot_tsa_for_series():
    year_key = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1919, 1918, 1916, 1914, 1913, 1910, 1905, 0]
    year_values = [2, 14, 102, 129, 118, 119, 103, 86, 93, 66, 73, 69, 45, 69, 44, 45, 57, 71, 301, 663, 683, 643, 623, 535, 481, 392, 317, 299, 234, 218, 206, 151, 144, 122, 117, 143, 129, 97, 96, 79, 77, 72, 83, 79, 72, 65, 56, 65, 49, 78, 73, 76, 54, 46, 48, 50, 43, 35, 41, 37, 32, 33, 22, 35, 71, 29, 32, 16, 19, 15, 18, 15, 18, 14, 13, 10, 15, 11, 15, 10, 8, 10, 4, 8, 8, 12, 6, 6, 2, 6, 4, 7, 7, 5, 4, 6, 5, 5, 4, 2, 1, 2, 1, 4, 1, 1, 1, 1, 5, 70]
    movies_released = [2, 12, 55, 55, 49, 44, 42, 22, 35, 32, 26, 39, 14, 31, 20, 22, 20, 26, 87, 269, 312, 323, 329, 286, 261, 205, 187, 167, 152, 132, 119, 94, 81, 74, 81, 97, 84, 68, 72, 62, 54, 52, 68, 58, 60, 50, 45, 55, 40, 58, 61, 68, 43, 40, 36, 39, 36, 30, 38, 34, 29, 28, 19, 32, 24, 25, 30, 15, 16, 14, 16, 11, 16, 14, 13, 9, 14, 11, 15, 10, 8, 9, 3, 7, 8, 7, 5, 6, 2, 6, 4, 7, 7, 5, 4, 6, 5, 5, 4, 2, 1, 2, 1, 4, 1, 1, 1, 1, 5, 0]
    tv_series_released = [0, 1, 17, 29, 21, 10, 14, 9, 17, 11, 19, 3, 9, 16, 5, 0, 7, 7, 9, 40, 41, 46, 54, 36, 36, 27, 25, 22, 17, 14, 29, 8, 11, 6, 6, 11, 13, 12, 5, 5, 2, 1, 5, 2, 5, 5, 4, 4, 2, 10, 4, 5, 6, 1, 5, 1, 3, 4, 0, 1, 2, 5, 1, 1, 46, 3, 2, 0, 2, 1, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    drama_released = [0, 2, 39, 50, 42, 38, 35, 23, 27, 23, 17, 18, 16, 25, 15, 9, 20, 16, 59, 202, 239, 241, 269, 245, 199, 173, 157, 117, 109, 109, 97, 69, 59, 54, 58, 60, 46, 38, 40, 37, 39, 30, 34, 37, 38, 35, 29, 36, 29, 43, 41, 41, 28, 30, 26, 20, 16, 16, 22, 22, 14, 21, 14, 23, 57, 13, 21, 8, 10, 10, 10, 10, 12, 8, 7, 6, 8, 10, 10, 4, 3, 5, 3, 3, 3, 9, 3, 2, 0, 3, 2, 4, 2, 3, 3, 5, 4, 3, 2, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
    comedy_released = [0, 3, 22, 33, 27, 25, 27, 34, 27, 22, 31, 23, 9, 24, 14, 13, 7, 8, 65, 167, 176, 172, 177, 152, 139, 113, 92, 110, 69, 72, 61, 47, 42, 38, 33, 48, 40, 33, 30, 27, 25, 24, 22, 24, 22, 21, 13, 18, 14, 13, 16, 18, 11, 12, 17, 16, 18, 12, 12, 12, 10, 13, 5, 12, 8, 5, 10, 1, 8, 3, 7, 5, 5, 4, 4, 3, 7, 0, 2, 2, 3, 5, 1, 3, 4, 3, 3, 3, 0, 2, 2, 1, 2, 3, 1, 2, 0, 1, 1, 2, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0]
    data = {'year_key': year_key,
        'year_values': year_values,
        'movies_released': movies_released,
        'tv_series_released': tv_series_released,
        'drama_released': drama_released,
        'comedy_released': comedy_released}
    netflix_data = pd.DataFrame(data)
    movies = netflix_data[["movies_released"]]
    series = netflix_data[["tv_series_released"]]
    drama = netflix_data[["drama_released"]]
    comedy = netflix_data[["comedy_released"]]
    decompose = seasonal_decompose(series, model = 'additive', period = 7)
    plt = decompose.plot()
    plt.savefig("Images/TVSeriesTimeSeries")
    
### Understand the column - Country
def plot_country():
    ### Create a connection to the normalized database to use TitleDetails
    normalized_connection = backend.create_connection('normalized.db', False)
    with normalized_connection:
        sql_statement = "SELECT Country, COUNT(Country) AS Count FROM TitleDetails WHERE Country != 'Unknown' GROUP BY Country ORDER BY Count DESC LIMIT 10;"
        country_df = pd.read_sql_query(sql_statement, normalized_connection)
    
    ### Plotting a pie chart for the top 10 countries 
    country_type = country_df['Country']
    country_value = country_df['Count']
    pie_explode = [0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig = plt.figure(figsize = (10, 7))
    plt.pie(country_value, labels = country_type, explode = pie_explode)
    plt.title("Understanding the distribution of top 10 countries")
    plt.savefig("Images/CountryDistribution")
    
    ### Close the connection
    normalized_connection.close()

### Understnd the column - Language
def plot_language():
    ### Create a connection to the normalized database to use TitleDetails
    normalized_connection = backend.create_connection('normalized.db', False)
    with normalized_connection:
        sql_statement = "SELECT Language, COUNT(Language) AS Count FROM TitleDetails WHERE Language != 'Unknown' GROUP BY Language ORDER BY Count DESC LIMIT 10;"
        language_df = pd.read_sql_query(sql_statement, normalized_connection)
    
    ### Plotting a pie chart for the top 10 languages 
    language_type = language_df['Language']
    language_value = language_df['Count']
    pie_explode = [0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fig = plt.figure(figsize = (10, 7))
    plt.pie(language_value, labels = language_type, explode = pie_explode)
    plt.title("Understanding the distribution of top 10 language")
    plt.savefig("Images/LanguageDistribution")

### Setup Regression dataframe
def setup_regression_dataframe(conn):
    with conn:
        sql_statement = """SELECT A.Kind, A.Genre, A.Country, A.Language, B.Rating, B.Runtime 
        FROM TitleDetails A INNER JOIN Titles B
        ON A.Title = B.Title;"""
        dataframe = pd.read_sql_query(sql_statement, conn)
    return dataframe

### Preprocessing the dataframe   
def preprocessing(dataframe): 
    ### Replacing missing values of runtime with mean
    runtimes = []
    mean_runtime = np.mean(dataframe['Runtime'])
    for runtime in dataframe['Runtime']:
        if runtime != 0:
            runtimes.append(runtime)
        else:
            runtimes.append(int(mean_runtime))
    dataframe['Runtime'] = runtimes
    
    ### Encoding the categorical variable Country using {United States/ United Kingdom/ Japan/ France/ Canada : 1, Others : 2}
    countries = []
    for country in dataframe['Country']:
        if country.strip("'") in ('United States', 'United Kingdom', 'Japan', 'France', 'Canada'):
            countries.append(1)
        else:
            countries.append(2)
    dataframe['Country'] = countries
    
    ### Encoding the categorical variable Language using {English/ French/ Japanese/ Spanish/ German : 1, Others : 2}
    languages = []
    for language in dataframe['Language']:
        if language.strip("'") in ('English', 'French', 'Japanese', 'Spanish', 'German'):
            languages.append(1)
        else:
            languages.append(2)
    dataframe['Language'] = languages
            
    ### Encoding the categorical variable Genre using {Drama/ Comedy/ Action/ Romance/ Thriller : 1, Others : 2}
    genres = []
    for genre in dataframe['Genre']:
        if genre.strip("'") in ('Drama', 'Comedy', 'Action', 'Romance', 'Thriller'):
            genres.append(1)
        else:
            genres.append(2)
    dataframe['Genre'] = genres
    
    ### Encoding the categorical variable Kind using {movie : 1, tv series : 2}
    kinds = []
    for kind in dataframe['Kind']:
        if kind == 'movie':
            kinds.append(1)
        else:
            kinds.append(2)
    dataframe['Kind'] = kinds
    
    ### Return dataframe
    return dataframe
    
### Encode variables given_kind, given_genre, given_country, given_language, given_runtime
def encode_variables(given_kind, given_genre, given_country, given_language, given_runtime):
    kind = 2
    genre = 2
    country = 2
    language = 2
    runtime = int(given_runtime)
    
    ### Modify kind
    if given_kind.lower() == 'movie':
        kind = 1
    
    ### Modify genre
    if given_genre.lower() in ('drama', 'comedy', 'action', 'romance', 'thriller'):
        genre = 1
    
    ### Modify country
    if given_country.lower() in ('united states', 'united kingdom', 'japan', 'france', 'canada'):
        country = 1
        
    ### Modify language
    if given_language.lower() in ('english', 'french', 'japanese', 'spanish', 'german'):
        language = 1
    
    ### Return the values
    return (kind, genre, country, language, runtime)

### Start analysis
def start_analysis():
    ### Setup database
    backend.setup_database()
    
    ### Plot figure for the variable - Kind
    plot_kind()
    
    ### Plot figure for the variable - Genre
    plot_genre()
    
    ### Plot figure for the variable - Year
    plot_year()
    
    ### Plot figure for the variable - Country
    plot_country()
    
    ### Plot figure for the variable - Language
    plot_language()

    ### Plot Time Series Analysis graph for Movies
    plot_tsa_for_movies()
    
    ### Plot Time Series Analysis graph for Series
    plot_tsa_for_series()
    
def fetch_regression_result(given_kind, given_genre, given_country, given_language, given_runtime):
    ### Setup Regression Dataframe
    normalized_connection = backend.create_connection('normalized.db', False)
    regression_df = setup_regression_dataframe(normalized_connection)
    normalized_connection.close()
    
    ### Preprocessing the regression_df
    dataframe = preprocessing(regression_df)
    
    ### Encode user entered variables
    given_kind, given_genre, given_country, given_language, given_runtime = encode_variables(given_kind, given_genre, given_country, given_language, given_runtime)
    
    ### Dividing the dataset into dependent and independent variables
    X = dataframe.iloc[:, [0, 1, 2, 3, 5]].values
    Y = dataframe.iloc[:, 4].values
    
    ### Splitting the dataset into Training and Test sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    
    ### Training Multi Linear Regression on the training set 
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, Y_train)
    
    ### Predicting the test set results
    y_pred = regressor.predict(X_test)
    
    ### Predicting the new result
    predicted_rating = regressor.predict([[given_kind, given_genre, given_country, given_language, given_runtime]])
    
    ### Return predicted rating
    return round(predicted_rating[0], 2)    