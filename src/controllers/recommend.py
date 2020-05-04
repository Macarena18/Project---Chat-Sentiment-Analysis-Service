import pandas as pd
from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance

client = MongoClient(DBURL)
db = client.get_database()

@app.route("/users/<username>/recommend")
# Recommend similar users
def RecommendUsers(username):
    # create dict with list of users and messages
    messages={}
    list_users = list(db.users.find({}, {'_id':0, 'user_name':1}))
    for user in list_users:
        user_message = list(db.messages.find({"user_name":user["user_name"]},{"_id":0,"message_text":1}))
        messages[user["user_name"]]= " ".join([text["message_text"] for text in user_message])
    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(messages.values())
    matrix = sparse_matrix.todense()
    messages_df=pd.DataFrame(matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=messages.keys())
    #Identify top 3 similar users
    similarity_matrix = distance(messages_df, messages_df)
    sim_df = pd.DataFrame(similarity_matrix, columns=messages.keys(), index=messages.keys())
    recommend_user=sim_df[username].sort_values(ascending=False)[1:].head(3)
    return dumps(dict(recommend_user))


