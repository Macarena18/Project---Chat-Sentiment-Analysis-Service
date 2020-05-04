from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re
from src.helpers.errorHandler import APIError, errorHandler
from flask import request

#Connection to Mongo
client = MongoClient(DBURL)
db = client.get_database()

@app.route("/users/create/<new_username>")
# create new username
def CreateUser(new_username):
    usernames=(db.users.distinct("user_name")) # get all usernames that exist
    new_userid = max(db.users.distinct("user_id"))+1 # Create new user_id
    #Check if username exist
    if new_username in usernames:
        print("ERROR")
        raise APIError ("I´m sorry this username already exists. Try again with another username.")
    else: # Create new user
        username_details={"user_id": new_userid,"user_name":new_username}
        db.users.insert_one(username_details)
        return dumps(f"Sucess! user_id:{new_userid},user_name:{new_username}")

        
@app.route("/chats/create/<new_chatname>")
# create new chat with users
def CreateChat(new_chatname):
    chatnames=(db.chats.distinct("chat_name"))
    new_chatid = max(db.chats.distinct("chat_id"))+1 # create new chat_id
    users_list_id = list(db.chats.distinct("user_id"))
    #Check if username exist in chat
    if new_chatname in chatnames:
        print("ERROR")
        raise APIError ("I´m sorry this chat name already exists.")
    # Create new chat
    chat_details={"chat_id": new_chatid,"chat_name":new_chatname,"users":[]}
    db.chats.insert_one(chat_details)
    #Include users in chat
    if request.args:
        for param in request.args:
            user = request.args[param] # create param
            user_id = db.users.find_one({'user_name':user},{'user_id':1})['user_id'] # get user_id for the username (param)
            db.chats.update({'chat_name': new_chatname },{'$addToSet': {'users': user_id } }) #include user_id in chat
    return dumps(f"Success! chat_id:{new_chatid},chat_name:{new_chatname}, users:{user_id}")


@app.route("/chats/<chatname>/adduser/<username>")
# add user to a chat

def AddUserChat(chatname,username):
    usernames = db.users.distinct("user_name") # get all usernames that exist
    user_id = db.users.find_one({'user_name':username},{'user_id':1})['user_id'] # get the user_id for the username
    chatnames = db.chats.distinct("chat_name") # get all chatnames that exist
    chat_id = db.chats.find_one({'chat_name':chatname},{'chat_id':1})['chat_id'] #get the chat_id for the chatname
    #Check if username and chatname exist
    if username  not in usernames:
        print("ERROR")
        raise APIError ("I´m sorry this user doesn´t exist.")
    if chatname  not in chatnames:
        print("ERROR")
        raise APIError ("I´m sorry this chat doesn´t exist.")
    #Check if user_id  exist in chat
    chat_users = db.chats.find({"chat_name": chatname},{"users": 1})
    if user_id in [user["users"] for user in chat_users][0]:
        raise APIError ("I´m sorry. This username already exists in this chat.")
    #Add new user in chat
    db.chats.update({'chat_id': chat_id },{'$addToSet': {'users': user_id } })
    return dumps(f"Success! chat_id:{chat_id},chat_name:{chatname}, users:{user_id}, new_user:{username}")


@app.route("/chats/<chatname>/addmessage/<username>")
# Add message to a chat
def AddMessageChat(chatname,username):
    usernames = db.users.distinct("user_name") # all usernames that exist
    user_id = db.users.find_one({'user_name':username},{'user_id':1})['user_id'] # get the user_id for the user
    chatnames = db.chats.distinct("chat_name") # all chatnames that exist
    chat_id = db.chats.find_one({'chat_name':chatname},{'chat_id':1})['chat_id'] # get the chat_id for the chat
    new_messageid = max(db.messages.distinct("message_id"))+1 #create new message_id
    # create param
    messagetext = request.args["messagetext"] 

    #Check chatname and  username exist
    if username  not in usernames: #
        print("ERROR")
        raise APIError ("I´m sorry this user doesn´t exist.")
    if chatname  not in chatnames:
        print("ERROR")
        raise APIError ("I´m sorry this chat doesn´t exist.")
    
    #Check if user_id in chat  
    chat_users = db.chats.find({"chat_name": chatname},{"users": 1})
    if user_id not in [user["users"] for user in chat_users][0]:
        raise APIError ("I´m sorry. This user is not in this chat.")
    
    #Create new message
    message_details={"user_name": username,"user_id":user_id,"chat_id":chat_id,"chat_name":chatname,"message_id":new_messageid,"message_text":messagetext}
    db.messages.insert_one(message_details)
    return dumps(f"Success! chat_id:{chat_id},chat_name:{chatname}, user_id:{user_id}, user_name:{username},message_id:{new_messageid},message_text:{messagetext}")











