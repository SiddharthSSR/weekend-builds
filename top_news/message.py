import os
from time import sleep
from twilio.rest import Client
from scrap import get_newsapi_articles, get_newsdata_articles

# account_sid = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_ACCOUNT_SID  = "ACae93fd0e0ce729eb40a3026fa5797992"
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_AUTH_TOKEN  = "0cf1ce457d3ea5ee3fc402f30b15bbef"
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

TWILIO_PHONE_NUMBER = '+15074317268'
USER_PHONE_NUMBER = '+919873347409'

MAX_MESSAGE_LENGTH = 1400

# Define a function to send a message with the specified body
def send_message(message_body):
    message = client.messages.create(to=USER_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER, body=message_body)
    print(f"Message sent to {USER_PHONE_NUMBER} with SID {message.sid}")

def send_news_to_user():
    newsapi_result = get_newsapi_articles()
    newsdata_result = get_newsdata_articles()

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message_body = "Here are the latest news results:\n"

    # Combine the newsapi_result and newsdata_result lists
    all_articles = newsapi_result + newsdata_result

    # Initialize an empty list to hold message chunks
    message_chunks = []

    # Loop over the articles and split them into chunks that are no longer than MAX_MESSAGE_LENGTH characters
    current_chunk = "Here are the latest news results:\n" # Start with the header
    for article in all_articles:
        article_text = f"\n{article['title']}\n{article['description']}\n{article['url']}\n\n"
        if len(current_chunk) + len(article_text) > MAX_MESSAGE_LENGTH:
            message_chunks.append(current_chunk) # Add the current chunk to the list
            current_chunk = "" # Start a new chunk with just the current article
        current_chunk += article_text # Add the current article to the current chunk

    # Add the final chunk to the list
    if current_chunk:
        message_chunks.append(current_chunk)

    # Send each chunk as a separate message
    for chunk in message_chunks:
        send_message(chunk)

if __name__ == "__main__":
    try:
        send_news_to_user()
    except Exception as e:
        print(f"An error occurred: {e}")