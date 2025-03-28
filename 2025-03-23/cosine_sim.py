import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
file_path = "recipes.csv"
df = pd.read_csv(file_path)

# Define features to combine
features = ['title', 'rating_avg', 'rating_val', 'total_time', 'category', 'cuisine', 'ingredients']

# Fill NaN values to prevent errors
df[features] = df[features].fillna("")

# Create a column called combined features
df["combine_features"] = df[features].astype(str).agg(' '.join, axis=1)
print(df["combine_features"].head())

# Convert text into a matrix
vectorizer = CountVectorizer(stop_words="english")
count_matrix = vectorizer.fit_transform(df["combine_features"])

# Compute cosine similarity
cosine_sim = cosine_similarity(count_matrix)

# Convert to DataFrame with "recipe titles" as index and columns
cosine_sim_df = pd.DataFrame(cosine_sim, index=df["title"], columns=df["title"])

# Save similarity matrix to a CSV file
cosine_sim_df.to_csv("cosine_similarity.csv")

print("Cosine similarity matrix saved as 'cosine_similarity.csv'")

# Function to get recipe recommendations
def get_recommendations(recipe_title, top=10):
    if recipe_title not in df["title"].values:
        return "Recipe not found in the dataset."

    # Get similarity scores for the given recipe
    sim_scores = cosine_sim_df[recipe_title].sort_values(ascending=False)
    
    # Get top N similar recipes (excluding itself)
    recommended_recipes = sim_scores.iloc[1:top+1].index.tolist()
    
    return recommended_recipes

recipe_name = "Chicken and coconut curry"
recommended_recipes = get_recommendations(recipe_name)
print(f"Recipes similar to '{recipe_name}': {recommended_recipes}")
