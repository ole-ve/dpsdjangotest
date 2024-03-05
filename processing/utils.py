import json
from typing import List

import pandas as pd
import seaborn as sns
import torch
import wandb
from matplotlib import pyplot as plt
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


def get_sentiment(news_articles, query: str, write_to_file=False):
    # Retrieve the title from each article and create a new list from it
    news_titles = [article.get("title") for article in news_articles]
    print(news_titles)

    # load tokenizer & model
    inputs = tokenizer(news_titles, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)

    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    print(predictions)

    positive = predictions[:, 0].tolist()
    negative = predictions[:, 1].tolist()
    neutral = predictions[:, 2].tolist()

    table = {'title': news_titles,
             'negative': negative,
             'neutral': neutral,
             'positive': positive
             }

    df = pd.DataFrame(table, columns=["title", "negative", "neutral", "positive"])
    sentiment_predictions = df.to_json(orient="records")

    if write_to_file:
        normalized_file_name = f'data/sentiment_analyses/{query.lower()}.json'
        with open(normalized_file_name, 'w') as f:
            f.write(sentiment_predictions)
            # json.dump(sentiment_predictions, f)

    return sentiment_predictions

    # get the max of each sentiment
    df['dominant_sentiment'] = df[['negative', 'neutral', 'positive']].idxmax(axis=1)

    # get counts of sentiments
    sentiment_counts = df['dominant_sentiment'].value_counts()

    # create bar plot
    # sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
    # plt.xlabel('Sentiment')
    # plt.ylabel('Number of Articles')
    # plt.title('Sentiment Analysis of News Titles')
    # plt.tight_layout()
    # plt.show()

    # wandb.init(project="FinBERT_Sentiment_Analysis")
    # wandb.run.log({"Financial News Sentiment Analysis": wandb.Table(dataframe=df)})
    # wandb.run.finish()
