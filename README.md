# Sentiment-Analysis-Youtube-Comments
Uses Google's v3 API to get the top 100 relevant comments and do a sentiment analysis on each comment and then, finally return the 'Average' sentiment. The application is hosted using Salesforce Heroku which is a Platform as a Service (PaaS). <br>

Link to the app: https://youtube-comments-sentiment.herokuapp.com/ <br>

To use the app, just enter the url of the youtube video (whose sentiment is to be analyzed) and click "Check the Sentiment" button.

Working:
1) The user enters the url of the youtube video,whose 'average sentiment' has to be determined. 
2) 'Cleaning' of the url string is done to obtain the 'video_id' of the video. 
3) The video_id is then given as an input to Google's v3 API, which is used to fetch 100 'most relevant' (Youtube has its own algorithm to determine whether a comment is 'relevant' or not) comments on the youtube video whose url has been given by the user. 
4) Once the comments are fetched, they are appended to a dataframe using pandas library. 
5) Then, all the comments are cleaned (e.g. any 'mention' or a 'link' is replaced by '@' or 'http-link' respectively). 
6) After this, each comment is fed into the NLTK (Natural Language Toolkit) library's 'SentimentIntensityAnalyzer' method, which gives us the 'compound polarity score'. The compound polarity score or 'sentiment score' ranges from -1 to +1, the higher the 'sentiment score' the positive the comment is. 
7) After receiving the sentiment score of all comment, "average sentiment score" is calculated. 
8) This, 'average sentiment score' is then binned into one of the nine categories (in ascending of the sentiment score): 'Extremely Negative' (very close to -1), 'Very Negative', 'Negative', 'Neutral-Negative', 'Neutral', 'Neutral-Positive', 'Positive', 'Very Positive' and 'Extremely Positive' (close to +1). Now, the final sentiment along with the 'Average sentiment score' is returned and displayed to the user.

Time taken to process one request (processing top 100 relevant comment and returning final sentiment and average sentiment score) is around 2 seconds to 5 seconds.
