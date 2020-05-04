from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re
from src.helpers.errorHandler import errorHandler, Error404

#Connection to Mongo
client = MongoClient(DBURL)
db = client.get_database()

@app.route("/", methods=["GET"])
#return welcome message
def Welcome():
    return "Welcome to the API - Chat Sentiment Analysis Service"

@app.route("/chats",methods=["GET"])
# return all the different chats in the dataset
def getChats():
    chat_list = db.chats.find({},{"_id":0,"chat_id":1,"chat_name":1})
    return dumps(chat_list)

@app.route("/users",methods=["GET"])
#return all usernames in the dataset
def getUsers():
    user_list = db.users.find({},{"_id":0,"user_id":1,"user_name":1})
    return dumps(user_list)

@app.route("/users/<name>",methods=["GET"])
@errorHandler
# return messages for an specific username
def getUserMessage(name):
    namereg = re.compile(f"^{name}", re.IGNORECASE)
    user_message = db.messages.find({"user_name":namereg},{"_id":0,"chat_name":1,"chat_id":1,"message_id":1,"message_text":1})
    if not user_message:
        print("ERROR")
        raise Error404("Username not found")
    return dumps(user_message)

@app.route("/chats/<chatname>",methods=["GET"])
# return messages for an specific chat
def getChatMessage(chatname):
    namechatreg = re.compile(f"^{chatname}", re.IGNORECASE)
    chat_message = db.messages.find({"chat_name":namechatreg},{"_id":0,"user_name":1,"user_id":1,"message_id":1,"message_text":1})
    if not chat_message:
        print("ERROR")
        raise Error404("Chatname not found")
    return dumps(chat_message)

@app.route("/messages", methods=["GET"])
#return all messages in the dataset
def getMessages():
    return dumps(db.messages.find({},{"_id":0}))
