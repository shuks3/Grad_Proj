# grad_proj
Netflix introduced streaming services in 2007 as an initiative in it’s evolving marketing strategies. This has created the opportunity to mine huge chunks of user
data and analyze user-streaming behavior.

Backend.py : contains backend code to process database file<br />
Analysis.py : contains EDA and predictions<br />
User_Interface.py : Contains frontend code to load UI<br />

Project Flow:<br />
● Creating DataBase:<br />
   Imported csv present in a non normalised database form is converted into then its normalized database.<br />
   Database consists of two tables - 1. Titles and Title Details<br />
   These two tables are further utilized for creating dataframe for the regression process.<br />
  ER Diagram:<br />
  ![image](https://user-images.githubusercontent.com/89943462/148662708-6e8e2572-3e61-40a4-952b-d1d4613522ba.png)

 ● Data Preprocessing<br />

  Replacing missing values of runtime with mean.<br />
  Encoding the categorical variable Country using {United States/ United Kingdom/ Japan/ France/ Canada : 1, Others : 2}<br />
  Encoding the categorical variable Language using {English/ French/ Japanese/Spanish/ German : 1, Others : 2}<br />
  Encoding the categorical variable Genre using {Drama/ Comedy/ Action/Romance/ Thriller : 1, Others : 2}<br />
  Encoding the categorical variable Kind using {movie : 1, tv series : 2}<br />
  
  ● Exploratory Data Analysis:<br />
    Genre, Language and Country wise data distribution : Drama is the most preferred genre, English is the most preferred language, and the United States has the most number of releases.
    Number of shows released in the last 10 years and kind of shows that were released the most (movies were released more than tv series): There is a steady rise in the number of releases in the coming year. Possibly, Netflix’s viewer base has increased due to the shift in ‘work-from-home’ and remote working culture. Unable to participate in social engagements, users are instead spending their time on streaming movies and shows on netflix.<br />
    2022 and 2023 show very low values as these two years have future data. This is predicted using time series analysis.<br />
     
Prediction Methods:<br />
Logistic Regression : Regression model was used to predict imdb scores. Kind (Movie/ TV Series) has a strong positive association with the Rating, Country has a strong negative association with the rating.<br />
![image](https://user-images.githubusercontent.com/89943462/148662776-d7742552-9462-4ff1-848b-e6a6a2e0060e.png)<br />

Time Series Analysis and Forecasting: Augmented Dickey-Fuller unit root test was run on the dataset to understand the stationarity of data. ARMA model was utilized to predict the estimated releases in the upcoming years. Approximately 90 releases each were predicted in the year 2022 and 2023.<br />
![image](https://user-images.githubusercontent.com/89943462/148662796-7cfa0710-4c77-4046-9a25-035fbe8668f7.png)

      
