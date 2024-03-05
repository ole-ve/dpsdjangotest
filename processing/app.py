import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import torch
import wandb
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from transformers import AutoTokenizer, AutoModelForSequenceClassification

#news_file_path = 'data/queried_news.json'
news_file_path = 'data/data.json'
news_data = pd.read_json(news_file_path)

# gather news headlines to pass to the model --- HEADLINE ONLY
titles_list = news_data['title'].tolist()

# gather news headlines & full article --- HEADLINE+FULLARTICLE
news_data['full_article'] = news_data['title'] + " " + news_data['fullArticle']
articles_list = news_data['full_article'].tolist()



# load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

#inputs = tokenizer(titles_list, padding=True, truncation=True, return_tensors='pt')
inputs = tokenizer(articles_list, padding=True, truncation=True, max_length=512, return_tensors='pt')

outputs = model(**inputs)

predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions)

positive = predictions[:, 0].tolist()
negative = predictions[:, 1].tolist()
neutral = predictions[:, 2].tolist()

table = {'title': titles_list,
         'negative': negative,
         'neutral' : neutral,
         'positive': positive
         }

df = pd.DataFrame(table, columns = ["title", "negative", "neutral", "positive"])

# get the max of each sentiment
df['dominant_sentiment'] = df[['negative', 'neutral', 'positive']].idxmax(axis=1)

# get counts of sentiments
sentiment_counts = df['dominant_sentiment'].value_counts()

# create bar plot
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
plt.xlabel('Sentiment')
plt.ylabel('Number of Articles')
plt.title('Sentiment Analysis of News Titles')
plt.tight_layout() 
#plt.show()

wandb.init(project="FinBERT_Sentiment_Analysis")
wandb.run.log({"Financial News Sentiment Analysis" : wandb.Table(dataframe=df)})
wandb.run.finish()
