# Project---Chat-Sentiment-Analysis-Service
<src image https://github.com/Macarena18/Project-ChatSentimentAnalysisService/blob/master/images/api_creation-benefit-microservices_made_easy.png>

**Requirements**:
- Write an API in `Flask` just to store chat messages in a database like `MongoDB`(`api.py` ->> To run the server  `runServer.sh`).
- Extract **sentiment** from chat messages and perform a report over a whole conversation `sentiment.py`.
- Recommend friends to a user based on the contents from chat documents using a recommender system with `NLP` analysis. `recommend.py`
- Deploy the service with `Docker to Heroku` and store messages in a Cloud database`MongoAtlas`. (`Dockerfile`,`requirements.text`;`syncDb.sh` -> **Docker image creation**)

# How to use the API?

**API EndPoints:**

**doc `create.py`:**

- *"/users/create/`new_username`"* --> **Create a username**
- *"/chats/create/`new_chatname`?param=`username`"* --> **Create new chat with users**
- *"/chats/`chatname`/adduser/`username`"* --> **Add a user to a chat**
- *"/chats/`chatname`/addmessage/`username`?messagetext=`text`"* --> **Add a message to a chat**

**doc `get.py`:**
- *"/"* -> **API Welcome Message**
- *"/chats"* -->  **Get all chats**
- *"/users"* -->  **Get all users**
- *"/users/`name`"* --> **Get all messages from `username`**
- *"/chats/`chatname`"* --> **Get all messages from `chatname`**
- *"/messages"* --> **Get all messages**

**doc `sentiment.py`:**
- *"/chats/`chatname`/sentiment"* --> **Report that extracts all sentiments from `chatname` messages** `NLTK sentiment analysis`
- *"/users/`username`/sentiment"* --> **Report that extracts  all sentiments from `username` messages** `NLTK sentiment analysis`

**doc `recommend.py`:**
- *"/users/`username`/recommend"* --> **Recommend top 3 similar users for a `username`**