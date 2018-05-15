import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import sys
import csv
import string
 
class TwitterClient(object):
    
    def __init__(self):        
        # input keys and tokens from the Twitter Dev Console here
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""
        
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            print('Authentication successful')
        except:
            print("Error: Authentication Failed")

        
        self.tweets = []
        self.sentiment_values={'positive':0,'negative':0,'neutral':0}
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"\
                                    "|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        
 
        try:
            extractedTweets=0
            
            while extractedTweets <=count:
                # call twitter api to fetch tweets
                fetched_tweets = self.api.search(q = query, count = count,language='en')
                print('fetched '+str(len(fetched_tweets))+' tweets\n\n\n')

                extractedTweets+=len(fetched_tweets)
                
                # parsing tweets one by one
                for i,tweet in enumerate(fetched_tweets):
                    parsed_tweet = {}
                    # saving sentiment of tweet
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                    if parsed_tweet['sentiment'] not in self.sentiment_values:
                        self.sentiment_values[parsed_tweet['sentiment']]=1
                    else:
                        self.sentiment_values[parsed_tweet['sentiment']]+=1
                        
                    

                    
                    #translate non printable characters in tweet e.g. smiley,gestures
                    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                    printabletweet=tweet.text.translate(non_bmp_map)

                    printable=set(string.printable)
                    
                    
                    # saving text of tweet
                    parsed_tweet['text'] = ''.join(filter(lambda x: x in printable,tweet.text))          

                    

                    if tweet._json['place']:
                        parsed_tweet['location']=''.join(filter(lambda x: x in printable,tweet._json['place']['full_name']))
                        print(parsed_tweet['location'])           
                    elif tweet._json['user']['location']:
                        parsed_tweet['location']=''.join(filter(lambda x: x in printable,tweet._json['user']['location']))
                        print(parsed_tweet['location'])
                    elif tweet._json['coordinates']:
                        parsed_tweet['location']=''.join(filter(lambda x: x in printable,tweet._json['coordinates']['coordinates']))
                        print(parsed_tweet['location'])
                    else:
                        parsed_tweet['location']=''
                        
                        
                    print('Analyzed '+str(i)+' Tweet')
                    
                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in self.tweets:
                            self.tweets.append(parsed_tweet)
                    else:
                        self.tweets.append(parsed_tweet)          
            
     
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

        return self.tweets


    def exportFile(self,filename):
        with open(filename,'w',encoding='ascii',newline='') as csvfile:
            csvwriter=csv.DictWriter(f=csvfile,fieldnames=['Tweet','Sentiment','Location'])
            csvwriter.writeheader()            

            for i,tweet in enumerate(self.tweets):
                if len(tweet) == 0:
                    print('Empty Tweet')
                    continue
                csvwriter.writerow({'Tweet':tweet['text'],'Sentiment':tweet['sentiment'],'Location':tweet['location']})

        
    def getPieChart(self,query):
        positive=self.sentiment_values['positive']
        negative=self.sentiment_values['negative']
        neutral=self.sentiment_values['neutral']
        
        colors = ['green', 'red', 'grey']
        sizes = [positive, negative, neutral]
        labels = 'Positive', 'Negative', 'Neutral'

        ## use matplotlib to plot the chart
        plt.pie(x=sizes,shadow=True,colors=colors,labels=labels)

        plt.title("Sentiment of Tweets about {}".format(query))
        plt.show()
 
def main():
    query=input('What would you like to search on twitter?\n')
    count=int(input('Enter Number of  tweets to query:'))
    
    # creating object of TwitterClient Class
    api = TwitterClient()

    
    # calling function to get tweets
    tweets = api.get_tweets(query = query, count = count)
    

    try:
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                                   
        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
                                   
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                                   
        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
                                   
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
     
        
        print("\n\nPositive tweets:")
##        if ptweets!=[]:
##            for i,tweet in enumerate(ptweets):
##                if i>10:
##                    break
##                print(tweet['text'].encode('utf-8'))
##     
##        
##        print("\n\nNegative tweets:")
##        if ntweets!=[]:
##            for i,tweet in enumerate(ntweets):
##                if i>10:
##                    break
##                print(tweet['text'].encode('utf-8'))

        api.getPieChart(query)
        api.exportFile(query+' twitter analysis.csv')
        
    except Exception as e:
        print(e)
 
if __name__ == "__main__":
    # calling main function
    main()
