import nltk
from django.conf import settings
from pynytimes import NYTAPI
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

nyt = NYTAPI(settings.API_KEY, parse_dates=True)


def get_sentiment(content):
    sentiment = sid.polarity_scores(content)

    return {
        "compound": sentiment["compound"],
        "pos": sentiment["pos"],
        "neg": sentiment["neg"],
        "neu": sentiment["neu"]
    }


def get_articles(search, start, end):
    try:
        docs = nyt.article_search(
            query = search,
            dates = {
                "begin": start,
                "end": end
            },
            options = {
                "sort": "relevance",

                # Filter query option for Editorials or Guest Essays in Opinion section
                "fq": "section.name: Opinion AND (typeOfMaterials:(Editorial OR Op-Ed) OR kicker:Guest Essay)"
            }
        )
    except Exception:
        return []

    articles = []
    
    for doc in docs:
        articles.append({
            "uri": doc["uri"],
            "url": doc["web_url"],
            "snippet": doc["snippet"],
            "headline": doc["headline"]["main"],
            "timestamp": doc["pub_date"],
        })

    return articles


def get_topics(results=10):
    topics = set()

    try:
        articles = nyt.top_stories(section = "Opinion")
    except Exception:
        return topics
    
    for i in range(results):
        topics.add(' '.join(articles[i]["des_facet"][0].strip().lower().split()))
    
    return topics