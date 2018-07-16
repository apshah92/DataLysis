# DataLysis
A data analysis application in Python to perform sentiment analysis on twitter data. 

Program fetches twitter data on any topic or user using tweepy search API.Then preprocesses each tweet to remove emojis, links etc to  extract tweet text out of it. 

Once processed, it runs a sentiment analysis is run on each tweet and determines sentiment value for each. The sentiment value is classified as positive, negative or neutral. This set of data is used to measure general public opinion about particular topic or user.

For example, Tesla motors and Audi tweet analysis are attached with this.

Note: You have to create a developer account on tweeter to get access keys and token. These values are to be put into keys and tokens variables in program before executing.
