import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

headlines_df = pd.read_csv('newdata.csv')
headlines_df.dropna(subset=['Headline'], inplace=True)  # Drop rows with empty headline entries
headlines_array = np.array(headlines_df)
np.random.shuffle(headlines_array)
headlines_list = list(headlines_array[:, 1])

# Getting the tokenizer and the model
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Tokenize the headlines
inputs = tokenizer(headlines_list, padding=True, truncation=True, return_tensors='pt', max_length=512, add_special_tokens=True)

# Perform inference
outputs = model(**inputs)

# Postprocess with softmax
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

# Model classes
model_classes = model.config.id2label

# Format the results as a pandas data frame
positive = predictions[:, 0].tolist()
negative = predictions[:, 1].tolist()
neutral = predictions[:, 2].tolist()

table = {'Headline': headlines_list,
         "Positive": positive,
         "Negative": negative,
         "Neutral": neutral}

df = pd.DataFrame(table, columns=["Headline", "Positive", "Negative", "Neutral"])

sentiment = df[['Positive', 'Negative', 'Neutral']].idxmax(axis=1)
df['Dominant_Sentiment'] = sentiment.apply(lambda x: x)

# Print the updated dataframe
print(df)

original_sentiment = headlines_df['sentiment']

# Map sentiment values to numerical values for easier comparison
sentiment_mapping = {'Positive': 0, 'Negative': 1, 'Neutral': 2}
original_sentiment = original_sentiment.map(sentiment_mapping)

# Map the predicted dominant sentiment values to numerical values
predicted_sentiment = df['Dominant_Sentiment'].map(sentiment_mapping)

# Calculate accuracy
accuracy = (original_sentiment == predicted_sentiment).mean()
print(f"Accuracy: {accuracy * 100:.2f}%")
