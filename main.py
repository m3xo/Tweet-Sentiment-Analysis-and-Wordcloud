import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys
import re

api_key = "api"
api_key_secret = "secret api"

access_token = "access"
access_token_secret = "secret access"

#connect to api and app
auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler)

search_term = 'tommy fury'
#how many tweets
tweet_amount = 100

tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang='en').items(tweet_amount)

polarity = 0
positive = 0
neutral = 0
negative = 0

#print and cleanup tweets printed, replace rt with blank
for tweet in tweets:
    final_text = tweet.text.replace('RT', '')
    if final_text.startswith(' @'):
        position = final_text.index(':')
        final_text = final_text[position+2:]
    if final_text.startswith('@'):
        position = final_text.index(' ')
        final_text = final_text[position+2:]
    final_text = re.sub(r"http\S+", "", final_text)
    print(final_text)
    ##create txt file of tweets for wordcloud
    word_cl_text = open("output.txt", "a", encoding="utf-8")
    print(final_text, file=word_cl_text)
    word_cl_text.close()
    #polarity
    analysis = TextBlob(final_text)
    tweet_polarity = analysis.polarity
    if tweet_polarity > 0:
        positive +=1
    elif tweet_polarity < 0:
        negative +=1
    else:
        neutral +=1
    polarity += tweet_polarity

print(polarity)
print(f"Tweets: \nPositive: {positive} \nNeutral: {neutral} \nNegative: {negative}")

##wordcloud
wc_text = open('output.txt', mode='r', encoding='utf-8').read()
stopwords = STOPWORDS

wc = WordCloud(
    background_color='white',
    stopwords=stopwords,
    height=600,
    width=400
)

wc.generate(wc_text)
#store to a file
wc.to_file('final_wordcloud.png')

#erase text file so we have a blank slate for next run
text_file = open("output.txt", "r+")
text_file.truncate(0)
text_file.close()