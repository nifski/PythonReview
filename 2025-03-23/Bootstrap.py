import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt


# this is the file path
file_path = "WebScrape/recipes.csv"
# this reads the data from our csv file
df = pd.read_csv('recipes.csv')

print(df.head())
# this will print the top few columns just for confirmation that the csv file is being read

missing_values = df.isnull().sum()
print("The missing values for each column:\n", missing_values)
# this will check for missing values for each column and gives us the total missing values

print(" The summary statistics as followed:\n", df.describe())
# this will print the summary of the data in the csv file

top_10_rated = df.sort_values(by="rating_val",ascending=False)
print(top_10_rated[['title', 'rating_val']])
# this will print the top ten rated recipes, the rating value is used as criteria to pick between recipes, and it is not in ascending order

average_ratings = df.groupby("title")["rating_avg"].mean()
top_10_recipes = average_ratings.sort_values(ascending=False).head(10)
print("The top ten average rating as followed:/n", top_10_rated)
# this prints the top 10 recipes ratings, in desceneding order

ratings = df["rating_val"].dropna()
# this extracts rating value from the datsaset and removes missing values
bootstrap_mean = [np.mean(np.random.choice(ratings, size=100, replace=True)) for _ in range(1000)]
# this creates 1000 bootstrap samples, each sample includes 100 random selected ratings, with replacement
# in the long run this will allow the mean values from each bootstrap sample be stored inside of the bootstrap mean
lower_bound = np.percentile(bootstrap_mean, 2.5)
upper_bound = np.percentile(bootstrap_mean, 97.5)
# this will compute the upper and lower bounds  within the 95% interval
print(f"95% Confidence Interval for the Average Rating: ({lower_bound:.2f}, {upper_bound:.2f})")
# this prints the 95% confidence interval for the average rating
# I embedded the values directly into the upper and lower bounds using the f string

# this will allow us visualise the relationship between number of ratings and the average ratings
plt.figure (figsize=(10,6))
plt.scatter (df["rating_val"],df["rating_avg"], alpha=0.5)
plt.xlabel ("Number of Ratings")
plt.ylabel ("Average Ratings")
plt.title ("Average Rating vs Number of Ratings")
plt.grid (True)
plt.show()


