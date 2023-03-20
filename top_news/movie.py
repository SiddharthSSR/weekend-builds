import sys
import requests

TMDB_API_KEY = "YOUR-TMDB-API-KEY"
NYT_API_KEY = "YOUR-NYT-API-KEY"

def movie_reviews(title):
    # Search for the movie
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(search_url)
    search_results = response.json()["results"]
    if len(search_results) == 0:
        print("Movie not found.")
    else:
        movie_id = search_results[0]["id"]

        # Get the movie's reviews
        reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}"
        response = requests.get(reviews_url)
        reviews_results = response.json()["results"]

        return [{
            "Author": review['author'],
            "Rating": review['author_details']['rating'],
            "Review": review['content'],
        } for review in reviews_results]

def main(title):
    review = movie_reviews(title)

    for i, article in enumerate(review):
            article_text = f"Review {i+1}:\n{article['Author']}\n{article['Rating']}\n{article['Review']}\n"
            print(article_text)

if __name__ == "__main__":
    query = sys.argv[1].strip()
    try:
        main(query)
    except Exception as e:
         print(e)
