import sys
import requests

TMDB_API_KEY = "f8907fa18d7ff9180a8c104bcd842bd4"
NYT_API_KEY = "PoNGkT98AqC6Nal3VZNQdCStlVyX7SA0"

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

# def nyt_reviews(title):
#     search_url = f"https://api.nytimes.com/svc/movies/v2/reviews/search.json?api-key={NYT_API_KEY}&query={title}"
#     response = requests.get(search_url)
#     search_results = response.json()["results"]
#     if len(search_results) == 0:
#         print("Movie not found.")
#     else:
#         review_id = search_results[0]["id"]

#         # Get the movie's reviews
#         reviews_url = f"https://api.nytimes.com/svc/movies/v2/reviews/{review_id}.json?api-key={NYT_API_KEY}"
#         response = requests.get(reviews_url)
#         reviews_results = response.json()["results"]

#         return [{
#             "Author": review['author'],
#             "Rating": review['author_details']['rating'],
#             "Review": review['content'],
#         } for review in reviews_results]

def main(title):
    review = movie_reviews(title)
    # review = nyt_reviews(title)

    for i, article in enumerate(review):
            article_text = f"Review {i+1}:\n{article['Author']}\n{article['Rating']}\n{article['Review']}\n"
            print(article_text)

if __name__ == "__main__":
    query = sys.argv[1].strip()
    try:
        main(query)
    except Exception as e:
         print(e)