import requests
import pandas as pd

twitter_data = []

payload = {
    'api_key': 'XXXX',
    'query': 'NASDAQ: AAPL',
    'num': 100
}
response = requests.get(
    'https://api.scraperapi.com/structured/twitter/search', params=payload)
data = response.json()
data.keys()
all_tweets = data['organic_results']
for tweet in all_tweets:
    twitter_data.append(tweet)

df = pd.DataFrame(twitter_data)
df.to_csv('dataset.csv', index=False)
print("File exported")