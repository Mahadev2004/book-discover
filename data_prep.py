import pandas as pd

# Load data
books = pd.read_csv('books.csv', low_memory=False)
users = pd.read_csv('users.csv', low_memory=False)
ratings = pd.read_csv('ratings.csv', low_memory=False)

# Ensure all book titles in books DataFrame are in lowercase
books['Book-Title'] = books['Book-Title'].str.lower()

# Merge ratings with books on ISBN
ratings_with_name = ratings.merge(books, on='ISBN')

# Calculate the number of ratings and average rating for each book
num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

avg_rating_df = ratings_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)

# Merge number of ratings and average ratings dataframes
popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')

# Save the processed data
popular_df.to_pickle('popular.pkl')
books.to_pickle('books.pkl')
