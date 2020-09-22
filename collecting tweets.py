import keys
import tweepy as tw
import preprocessor as p
from stop_words import get_stop_words
import string
from nltk.tokenize import word_tokenize
import pandas as pd


# Creating and Configuring an OAuthHandler to Authenticate with Twitter
auth = tw.OAuthHandler(keys.consumer_key,
                           keys.consumer_secret)
auth.set_access_token(keys.access_token,
                      keys.access_token_secret)

# Creating an API Object
api = tw.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

# Establishing criteria for the query and its filters
search_words = '@francoislegault'
date_since = '2020-09-01'

# Collecting tweets
tweets = tw.Cursor(api.search,
                   q=search_words + "-filter:retweets",
                   lang='fr',
                   tweet_mode = 'extended',
                   since=date_since).items(10)

# Creating a list of tweets
all_tweets = [tweet.full_text for tweet in tweets]
print(all_tweets[0])

# Setting up arguments for using preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.RESERVED, p.OPT.URL,
              p.OPT.NUMBER, p.OPT.HASHTAG)

# Cleaning with a list comprehension -- mapping
clean_tweets = [p.clean(i) for i in all_tweets]
print(clean_tweets[0])

# Transforming all characters to lowercase
clean_tweets2 = [i.lower() for i in clean_tweets]
print(clean_tweets2[0])

# creating a set of stop words
french_stop_words = set(get_stop_words('french'))

# creating a set of punctuation
punc = set(string.punctuation)

# combining the 2 sets with an "or" operator (i.e. "|")
all_stops = french_stop_words | punc

# removing stop words and punctuation after tokenizing
clean_tweets3 =[]
for tweets in clean_tweets2:
    word_tokens = word_tokenize(tweets)
    word_tokens_nonum = [i for i in word_tokens if i.isalpha()]
    filtered_sentence = [i for i in word_tokens_nonum if i not in all_stops]
    clean_tweets3.append(filtered_sentence)
print(clean_tweets3[0])

clean_tweets_untok= [' '.join(i) for i in clean_tweets3]

#
column_names = ['original_tweet', 'cleaned_tweet', 'untok_tweet']
data_tuples = list(zip(all_tweets,clean_tweets3, clean_tweets_untok))
t_df = pd.DataFrame(data_tuples, columns = column_names)

# save to file
t_df.to_excel('/Users/emiliehamel/PycharmProjects/test_tweepy/data/tweets10.xlsx')

#
print("Done")