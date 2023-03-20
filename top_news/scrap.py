import sys
import requests
from newsapi import NewsApiClient
from newsdataapi import NewsDataApiClient

NYT_API_KEY = "YOUR-NYT-API-KEY"
NEWS_API_KEY = 'YOUR-NEWS-API-KEY'
NEWSDATA_API_KEY = 'YOUR-NEWSDATA-API-KEY'

def get_articles(api_client, query):
    articles = api_client.get_everything(q=query, language='en')
    return articles['articles']

def get_newsapi_articles(query):
    news_api_client = NewsApiClient(api_key=NEWS_API_KEY)
    articles = get_articles(news_api_client, query)
    articles = articles[:5]
    return [{
        "title": article['title'],
        "description": article['description'],
        "url": article["url"],
        "content": article.get("content"),
        "source": article["source"]["name"],
    } for article in articles]

def get_newsdata_articles(query):
    newsdata_api_client = NewsDataApiClient(apikey=NEWSDATA_API_KEY)
    articles = newsdata_api_client.news_api(q=query, language="en", page="1679107295264e99bdbc3fc93f7c27e1f3a7b3491c")['results']
    articles = articles[:5]
    return [{
        "title": article['title'],
        "description": article['description'],
        "url": article["link"],
        "source": article["source_id"],
    } for article in articles]

def nyt_news(query):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key={NYT_API_KEY}&q={query}"
    response = requests.get(url)
    data = response.json()

    # Process the news search results
    if "response" in data:
        return [{
            "title": result['headline']['main'],
            "abstract": result['abstract'],
            "url": result['web_url'],
            "pub_date": result['pub_date'],
        } for result in data["response"]["docs"]]
    else:
        print("No results found.")

def main(query):
    newsapi_result = get_newsapi_articles(query)
    newsdata_result = get_newsdata_articles(query)
    nyt_story = nyt_news(query)

    all_articles = newsapi_result + newsdata_result

    print("NEWS")
    for i, article in enumerate(all_articles):
            article_text = f"Article {i+1}:\n{article['title']}\n{article['description']}\n{article['url']}\n"
            print(article_text)

    print("NYT")
    for i, article in enumerate(nyt_story):
            article_text = f"Article {i+1}:\n{article['title']}\n{article['abstract']}\n{article['url']}\n{article['pub_date']}\n"
            print(article_text)


if __name__ == "__main__":
    query = sys.argv[1]
    print(query)
    try:
        main(query)
    except Exception as e:
         print(e)
