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
from tkinter import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

### Importing the module
import analysis

### Predict the rating
def result_from_regreesion(kind, genre, country, language, runtime):
    predicted_rating = analysis.fetch_regression_result(kind, genre, country, language, runtime)
    return predicted_rating

def show_result():
    kind = kind_field.get()
    genre = genre_field.get()
    country = country_field.get()
    language = language_field.get()
    runtime = runtime_field.get()
    if kind == "" or genre == "" or country == "" or language == "" or runtime == "":
        error_message.grid(row=11, column=1)
    else:
        error_message.grid_remove()
        rating_result.set(result_from_regreesion(kind, genre, country, language, runtime))
    
def show_plot(plot_name):
    if plot_name == "Distribution of the variable - Kind":
        image = cv2.imread("Images\\KindDistribution.png")
        cv2.imshow('Distribution of the variable - Kind', image)
        cv2.waitKey(0)
    elif plot_name == "Understanding the top 10 genres":
        image = cv2.imread("Images\\GenreDistribution.png")
        cv2.imshow('Understanding the top 10 genres', image)
        cv2.waitKey(0)
    elif plot_name == "Shows released in the past 10 years":
        image = cv2.imread("Images\\YearDistribution.png")
        cv2.imshow('Shows released in the past 10 years', image)
        cv2.waitKey(0)
    elif plot_name ==  "Top 10 countries with maximum releases":
        image = cv2.imread("Images\\CountryDistribution.png")
        cv2.imshow('Top 10 countries with maximum releases', image)
        cv2.waitKey(0)
    elif plot_name == "Top 10 languages with Netflix releases":
        image = cv2.imread("Images\\LanguageDistribution.png")    
        cv2.imshow('Top 10 languages with Netflix releases', image)
        cv2.waitKey(0)
    elif plot_name == "Time Series Analysis of Movies":
        image = cv2.imread("Images\\MovieTimeSeries.png")    
        cv2.imshow('Time Series Analysis of Movies', image)
        cv2.waitKey(0)
    elif plot_name == "Time Series Analysis of TV Series":
        image = cv2.imread("Images\\TVSeriesTimeSeries.png")    
        cv2.imshow('Time Series Analysis of TV Series', image)
        cv2.waitKey(0)
    
# on change dropdown value
def change_dropdown(*args):
    plot_name = tk_variable.get()
    show_plot(plot_name)

if __name__ == "__main__":
    root = Tk()
    root.geometry('500x300')
    root.title('Netflix Data Analysis')
    
    # Start Analysis
    analysis.start_analysis()
    # Setup Heading
    heading = Label(root, text = "Netflix Data Analyzer and Rating Predictor", font = ('Calibri 15 bold'))
    heading.grid(row=1, column=1)
    
    # Create a Tkinter variable
    tk_variable = StringVar(root)

    # List of options
    choices = ['','Distribution of the variable - Kind', 'Understanding the top 10 genres', 'Shows released in the past 10 years', 'Top 10 countries with maximum releases', 'Top 10 languages with Netflix releases', 'Time Series Analysis of Movies', 'Time Series Analysis of TV Series']
    tk_variable.set('Select an option') # set the default option
    popupLabel = Label(root, text = "Select which plot you want to observe: ")
    popupLabel.grid(row = 2, column = 1)
    popupMenu = OptionMenu(root, tk_variable, *choices)
    popupMenu.grid(row = 3, column = 1)

    # link function to change dropdown
    tk_variable.trace('w', change_dropdown)
    
    # Setup Labels
    kind_label = Label(root, text = "Kind: ")
    genre_label = Label(root, text = "Genre: ")
    country_label = Label(root, text = "Country: ")
    language_label = Label(root, text = "Language: ")
    runtime_label = Label(root, text = "Runtime: ")
    rating_label = Label(root, text = "Rating: ")
     
    # Setup Labels' layout
    kind_label.grid(row = 4)
    genre_label.grid(row = 5)
    country_label.grid(row = 6)
    language_label.grid(row = 7)
    runtime_label.grid(row = 8)
    rating_label.grid(row = 9)
    
    # Setup Fields
    rating_result = StringVar(root)
    kind_field = Entry(root, justify = 'left')
    genre_field = Entry(root, justify = 'left')
    country_field = Entry(root, justify = 'left')
    language_field = Entry(root, justify = 'left')
    runtime_field = Entry(root, justify = 'left')
    rating_field = Entry(root, textvariable = rating_result, justify = 'left')
    
    
    # Setup Fields' layout
    kind_field.grid(row = 4, column = 1)
    genre_field.grid(row = 5, column = 1)
    country_field.grid(row = 6, column = 1)
    language_field.grid(row = 7, column = 1)
    runtime_field.grid(row = 8, column = 1)
    rating_field.grid(row = 9, column = 1)
    
    submit = Button(root, text = "Predict", fg = "White", bg = "#E50914", command = show_result)
    submit.grid(row = 10, column = 1)
    
    error_message = Label(root, text="Input value should not be empty", fg="red")

    # Bind Fields with Enter button
    kind_field.bind("<Return>", lambda event: genre_field.focus())
    genre_field.bind("<Return>", lambda event: country_field.focus())
    country_field.bind("<Return>", lambda event: language_field.focus())
    language_field.bind("<Return>", lambda event: runtime_field.focus())
    runtime_field.bind("<Return>", lambda event: runtime_field.focus())
    rating_field.bind("<Return>", lambda event: submit.focus())
    submit.bind("<Return>", lambda event: show_result())

    root.mainloop()