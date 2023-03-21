#!/usr/bin/env python
# coding: utf-8

# In[5]:


# importing all the neccessary libraries
import os
import googleapiclient.discovery
from flask import request, Flask, render_template
import jsonify
import requests
import numpy as np
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:

            link = request.form['url_name']
            if 'youtu.be' in link:
                v_id = link.split('youtu.be/')[-1]
            
            elif 'shorts' in link:
                v_id = link.split('shorts/')[-1].split('?')[0]
                
            else:
                v_id = link.split('?v=')[-1].split('&')[0]
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            api_service_name = "youtube"
            api_version = "v3"
            DEVELOPER_KEY = "ENTER_YOUR_API_DEVELOPER_KEY"
            youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
            link_request = youtube.commentThreads().list(part="snippet", maxResults=200,  order="relevance",videoId= v_id)
            link_response = link_request.execute()
            result = link_response.copy()
            comments = []
            reply_cnt = []
            for i in range(len(result['items'])):
                comments.append(result['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
                reply_cnt.append(result['items'][i]['snippet']['totalReplyCount'])

            yt = pd.DataFrame({'Comment':comments, 'Reply_Count':reply_cnt})
            #median_reply = yt['Reply_Count'].median()
            yt2 = yt.copy()
            sia = SentimentIntensityAnalyzer()
            yt2['Sentiment'] = yt2['Comment'].apply(lambda x: sia.polarity_scores(x))
            yt2['comp_score'] = yt2['Sentiment'].apply(lambda x: x['compound'])

            def final_sent_calc(x):

                def estimator(a):
                    return float(str(a)[:6])
                def estimator2(b):
                    return float(str(b)[:7])

                if x in np.asarray(pd.Series(np.arange(-1.001, -0.778,0.0001)).apply(lambda x: estimator2(x))):
                    return 'Extremely Negative'
                elif x in np.asarray(pd.Series(np.arange(-0.778, -0.556,0.0001)).apply(lambda x: estimator2(x))):
                    return 'Very Negative'
                elif x in np.asarray(pd.Series(np.arange(-0.556, -0.333,0.0001)).apply(lambda x: estimator2(x))):
                    return 'Negative'
                elif x in np.asarray(pd.Series(np.arange(-0.333, -0.111,0.0001)).apply(lambda x: estimator2(x))):
                    return 'Neutral-Negative'
                elif x in np.asarray(pd.Series(np.arange(-0.111, 0.000,0.0001)).apply(lambda x: estimator2(x))):
                    return 'Neutral'
                elif x in np.asarray(pd.Series(np.arange(0, 0.111,0.0001)).apply(lambda x: estimator(x))):
                    return 'Neutral'
                elif x in np.asarray(pd.Series(np.arange(0.111, 0.333,0.0001)).apply(lambda x: estimator(x))):
                    return 'Neutral-Positive'
                elif x in np.asarray(pd.Series(np.arange(0.333, 0.556,0.0001)).apply(lambda x: estimator(x))):
                    return 'Positive'
                elif x in np.asarray(pd.Series(np.arange(0.556, 0.778,0.0001)).apply(lambda x: estimator(x))):
                    return 'Very Positive'
                elif x in np.asarray(pd.Series(np.arange(0.778, 1.001,0.0001)).apply(lambda x: estimator(x))):
                    return 'Extremely Positive'

            yt2['Final_Sentiment'] = yt2['comp_score'].apply(lambda x: final_sent_calc(x))
            med_score = round(yt2['comp_score'].mean(),3)
            final_sentiment = final_sent_calc(round(yt2['comp_score'].mean(),3))

            print(f"FINAL SENTIMENT: {final_sentiment} and the Sentiment Score is {med_score}")

            return render_template('index.html',prediction_text=f"For top 100 relevant comments, the final average sentiment is: {final_sentiment} and the average Sentiment Score is {med_score}")
        except:
            return render_template('index.html',prediction_text=f"Comments are Disabled.")
    else:
        print('NO ENTRY')
        return render_template('index.html')

if __name__=="__main__":
    app.run()

