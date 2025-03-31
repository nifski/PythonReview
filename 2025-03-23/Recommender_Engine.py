import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# this loads the recipe dataset
file_path = "recipes.csv"
df = pd.read_csv(file_path)

# these are the feautures we are looking at
features = ['title', 'rating_avg', 'rating_val', 'total_time', 'category', 'cuisine', 'ingredients']

# this fills NaN values to prevent errors
df[features] = df[features].fillna("")

# this create a column called combined features which combines features above
df["combine_features"] = df[features].astype(str).agg(' '.join, axis=1)
print(df["combine_features"].head())

# this will convert text into a matrix
vectorizer = CountVectorizer(stop_words="english")
count_matrix = vectorizer.fit_transform(df["combine_features"])

# this computes a cosine similarity
cosine_sim = cosine_similarity(count_matrix)

# this converts to a pandas DataFrame with "recipe titles" as index AND columns
cosine_sim_df = pd.DataFrame(cosine_sim, index=df["title"], columns=df["title"])

# this saves a similarity matrix to a CSV file
cosine_sim_df.to_csv("cosine_similarity.csv")

# this prints a confirmation message that the file was saved
print("Cosine similarity matrix saved as 'cosine_similarity.csv'")

# this is a function to get recipe recommendations
def get_recommendations(recipe_title, top=10):
    if recipe_title not in df["title"].values:
        return "Recipe not found in the dataset."

    # this gets similarity scores for the given recipe
    sim_scores = cosine_sim_df[recipe_title].sort_values(ascending=False)
    
    # this gets the top similar recipes (excluding itself)
    recommended_recipes = sim_scores.iloc[1:top+1].index.tolist()
    
    return recommended_recipes

recipe_name = "Chicken and coconut curry"
# this is a test using chicken and coconut curry to test the recommender engine
recommended_recipes = get_recommendations(recipe_name)
print(f"Recipes similar to '{recipe_name}': {recommended_recipes}")
