from src.app import app
from pymongo import MongoClient
from src.config import DBURL
import re
import pandas as pd
from bson.json_util import dumps
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")

#Connection to Mongo
client = MongoClient(DBURL)
db = client.get_database()

@app.route("/chats/<chatname>/sentiment")
# create report that extracts sentiment from chat messages
def ChatSentiment(chatname):
    sia=SentimentIntensityAnalyzer()
    messages_text=[]
    messages_scores=[]
    #Check if chatname exist
    namechatreg = re.compile(f"^{chatname}", re.IGNORECASE)
    chat_message = db.messages.find({"chat_name":chatname},{"_id":0,"user_name":1,"user_id":1,"message_id":1,"message_text":1})
    if not chat_message:
        print("ERROR")
        raise Error404("Chatname not found")

    for message in chat_message:  
        messages_text.append(message["user_name"]+":" + message["message_text"]) # create list with usernames+messages of a chat
        messages_scores.append(sia.polarity_scores(message["message_text"])) #create list with polarity scores of chat messages
    # create daframe with message scores
    data_messages=pd.DataFrame(messages_scores)
    data_messages=data_messages.rename(columns={'neg':'Negative', 'neu':'Neutral', 'pos':'Positive'})
    #calculate scores mean of all chat messages and create new dataframe with means
    means=data_messages.mean(axis = 0) 
    sentiment_means=pd.DataFrame(means)
    sentiment_means.columns=["Sentiment scores"]
    #Create Chat Sentiment Report 
    sentiment_scores=sentiment_means["Sentiment scores"]
    chat_sentiment={}
    for score in sentiment_scores:
        chat_sentiment["Negative"]=round(sentiment_scores[0],2)
        chat_sentiment["Neutral"]=round(sentiment_scores[1],2)
        chat_sentiment["Positive"]=round(sentiment_scores[2],2)
    report={}
    report["Chat Sentiment"]= chat_sentiment
    report["Sentiment Messages"]={"Messages":messages_text,"Polarity_scores":messages_scores}
    return dumps(report)

@app.route("/users/<username>/sentiment")
# create report that extracts sentiment from user messages
def UserSentiment(username):
    sia=SentimentIntensityAnalyzer()
    messages_text=[]
    messages_scores=[]
    #Check if username exist
    namereg = re.compile(f"^{username}", re.IGNORECASE)
    user_message = db.messages.find({"user_name":username},{"_id":0,"chat_name":1,"chat_id":1,"message_id":1,"message_text":1})
    if not user_message:
        print("ERROR")
        raise Error404("Username not found")

    for message in user_message:  
        messages_text.append(message["chat_name"]+":" + message["message_text"]) # create list with chatnames+messages of a user
        messages_scores.append(sia.polarity_scores(message["message_text"])) #create list with polarity scores of user messages
    # create daframe with message scores
    data_messages=pd.DataFrame(messages_scores)
    data_messages=data_messages.rename(columns={'neg':'Negative', 'neu':'Neutral', 'pos':'Positive'})
    #calculate scores mean of all user messages and create new dataframe with means
    means=data_messages.mean(axis = 0) 
    sentiment_means=pd.DataFrame(means)
    sentiment_means.columns=["Sentiment scores"]
    #Create User Sentiment Report 
    sentiment_scores=sentiment_means["Sentiment scores"]
    chat_sentiment={}
    for score in sentiment_scores:
        chat_sentiment["Negative"]=round(sentiment_scores[0],2)
        chat_sentiment["Neutral"]=round(sentiment_scores[1],2)
        chat_sentiment["Positive"]=round(sentiment_scores[2],2)
    report={}
    report["User Sentiment"]= chat_sentiment
    report["Messages Sentiment"]={"Messages":messages_text,"Polarity_scores":messages_scores}
    return dumps(report)
  


  