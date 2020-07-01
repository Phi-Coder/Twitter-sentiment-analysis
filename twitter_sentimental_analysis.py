# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:36:33 2020

@author: GUCCHU
"""
import tweepy 
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re 
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')


# twitter api credentials
consumerKey="iAxV9oFuakIGT2IGyz1YsGtAc"
consumerSecret="dERwWkZVFRPJuH62YfSsAUfcBlfwsC05pbPeh8KzOUYPUFABlM"
accessToken="3894093733-CG2vUjNCjuyF5BxkpLuH4Us9CNtrV4jaUE1vued"
accessTokenSecret="8HQg4CjOgtt6l3K5Fbh2hqtGdrwLOMlwaR2XcsVF5bbhD"

# authentication 
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)

# set access token and access token secret
auth.set_access_token(accessToken, accessTokenSecret)

# creating the api object
api = tweepy.API(auth,wait_on_rate_limit= True)
posts = api.user_timeline(screen_name = "ElonMusk", count =1000,lang="en",tweet_mode = "extended")

print("recent tweets : \n")
i = 1
for tweet in posts[0:5]:
    print(str(i) + ") " + tweet.full_text + "\n")
    i=i+1

# creating a dataframe with column tweets 
df = pd.DataFrame([tweet.full_text for tweet in posts],columns = ['tweets'])

# function removing all non detailed information related to sentiment ex. @, # , links etc
def cleanTxt(text):
    text = re.sub(r'@[0-9a-zA-Z]+','',text) # remove @mentions
    text = re.sub(r'#','',text) # remove hashtag symbol
    text = re.sub(r'RT[\s]+','',text) # remove retweets
    text = re.sub(r'https?:\/\/[\S]+','',text) # remove hyperlink
        
    return text 
    
# cleaning unnecessary text    
df['tweets'] = df['tweets'].apply(cleanTxt)

# function to get the subjectivity (tells us how opiniated the text is!)
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# function to get the polarity ( tells how positive or negative the text is!)
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# Create columns to attach subjectivity and polarity to respective tweet
df['subjectivity'] = df['tweets'].apply(getSubjectivity)
df['polarity'] = df['tweets'].apply(getPolarity)

# plot word cloud
allwords = " ".join(tweet for tweet in df['tweets'])
wordcloud = WordCloud(width= 500,height = 300,random_state=21,max_font_size = 119).generate(allwords)

plt.imshow(wordcloud,interpolation = 'bilinear')
plt.axis('off')
plt.show()

# create function to compute analysis(positive or negative or neutral)
def getAnalysis(score):
    if score<0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"
    
df['analysis'] = df['polarity'].apply(getAnalysis)

# print out the positive tweets
j=1
sorted_df= df.sort_values(by=["polarity"],ascending='False')
for i in range(0,sorted_df.shape[0]):
    if sorted_df["analysis"][i] == "Positive":
        print(str(j) +") " +sorted_df['tweets'][i])
        j = j+1

#plot polarity and subjectivity graph 
plt.figure(figsize=(8,6))
for i  in range(0,df.shape[0]):
    plt.scatter(df['polarity'][i],df['subjectivity'][i],color="Blue")

plt.title("Sentiment analysis")
plt.xlabel("polarity")
plt.ylabel("subjectivity")
plt.show()

# get percentage of positive tweets

positive_tweets = df[df.analysis == "Positive"]
positive_tweets = positive_tweets['tweets']

percentage_positive_tweets = positive_tweets.shape[0]/df['tweets'].shape[0] *100


# get percentage of negative tweets

negative_tweets = df[df.analysis == "Negative"]["tweets"]
percentage_negative_tweets = negative_tweets.shape[0]/df['tweets'].shape[0] *100

# showing value counts 
print(df["analysis"].value_counts())








