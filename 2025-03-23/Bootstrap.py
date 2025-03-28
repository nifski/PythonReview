import pandas as pd
import numpy as np
import requests

file_path = "WebScrape/recipes.csv"
df = pd.read_csv('recipes.csv')

print(df.head())

missing_values = df.isnull().sum()
print("The missing values for each column:\n", missing_values)

print(" The summary statistics as followed:\n", df.describe())

top_10_rated = df.sort_values(by="rating_val",ascending=False)
print(top_10_rated[['title', 'rating_val']])


average_ratings = df.groupby("title")["rating_avg"].mean()
top_10_recipes = average_ratings.sort_values(ascending=False).head(10)
print("The top ten average rating as followed:/n", top_10_rated)

ratings = df["rating_val"].dropna()
bootstrap_mean = [np.mean(np.random.choice(ratings, size=100, replace=True)) for _ in range(1000)]
lower_bound = np.percentile(bootstrap_mean, 2.5)
upper_bound = np.percentile(bootstrap_mean, 97.5)
print(f"95% Confidence Interval for the Average Rating: ({lower_bound:.2f}, {upper_bound:.2f})")

