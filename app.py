from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Load processed data
popular_df = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/discover')
def discover_ui():
    return render_template('discover.html')

@app.route('/discover_books', methods=['POST'])
def discover():
    user_input = request.form.get('user_input').lower()

    # Find books containing the user input (case-insensitive search)
    filtered_books = popular_df[popular_df['Book-Title'].str.lower().str.contains(user_input)]

    # Check if we found any matches
    if filtered_books.empty:
        return render_template('discover.html', data=[{"title": "Not found", "author": "", "image": ""}])

    # Get top 5 related books
    discoveries = filtered_books.nlargest(5, 'avg_rating')

    data = []
    for _, row in discoveries.iterrows():
        data.append({
            'title': row['Book-Title'],
            'author': row['Book-Author'],
            'image': row['Image-URL-M']
        })

    return render_template('discover.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
    
