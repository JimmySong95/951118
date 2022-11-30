import requests
import os
import json
from google.cloud import language_v1

bearer_token = 'my token'  ## please change here to your own bearer_token

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params = {'query': '(from:elonmusk -is:reply) ','tweet.fields': 'author_id'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
def main():
    text_content = []
    json_response = connect_to_endpoint(search_url, query_params)
    data1=json.dumps(json_response, indent=4, sort_keys=True)
    data2 = json.loads(data1)
    for index in data2['data']:
        text_content.append(index['text'])
    print(text_content)






    client = language_v1.LanguageServiceClient()
    for i in text_content:
        text = i
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        sentiment = client.analyze_sentiment(
            request={"document": document}
            ).document_sentiment
        print("Text: {}".format(text))
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

if __name__ == "__main__":
    main()
