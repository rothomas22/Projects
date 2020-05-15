import os
import requests
from  chclasses import *

from flask import Flask, session,  jsonify, render_template, request, redirect, url_for 
from flask_session import Session
from flask_socketio import SocketIO, emit
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#app.config["SECRET_KEY"] = 'secret!'
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

votes = {"yes": 0, "no": 0, "maybe": 0}

channelset = set ()
channeldict = {}
channelnames = set ()
messages = []
channelclicked = None

@app.route("/", methods=["GET", "POST"])
def index():
    global channelclicked, messages, channeldict, channelset
    session["lastChannelClicked"] = ""
    channelname = ""

    if request.method == "POST":
        for x in channelset:
            print (f" channel: {x.channelname} ")
            print (f" channelid: {x.id} ")
            channelclicked = request.form.get(f"{x.id}")
            print (f" form id: {channelclicked} ")
            if channelclicked is not None:
              print (f" channel: {channelclicked} ")
              session["lastChannelClicked"] = channelclicked
              break
    else:
        session["lastChannelClicked"] = ""

    if session["lastChannelClicked"] != "":
        channelclicked = session["lastChannelClicked"]
 
    print(f"index")
    if channelclicked is not None:
        print (f" channel: {channelclicked} ")
        indkey = "channel" + str(channelclicked)
        messages = channeldict[indkey].messages
        channelname = channeldict[indkey].channelname
      
    return render_template("index.html",  channels=channelset, messages=messages, channelclicked = channelname)


@socketio.on("add channel")
def addchannel(data):
    global channelclicked, messages, channeldict, channels
    name = data["channel"]
    if name not in channelnames :
      channelnames.add(name)
      channel = Channels(name)
      indkey = "channel" + str(channel.id)
      channeldict[indkey] = channel
      channelset.add(channel)

      #votes[selection] += 1
      print(f" channelid {channel.id } channel name {name}")
      session["error_message"] = ""
      emit("new channel", {"name":name, "id": channel.id },  broadcast=True)

    else:
      session["error_message"]= "Channel name is not unique"
      err_message = session["error_message"]
      print(f"{err_message}")
      #return redirect(url_for('index'))
      #return render_template("index.html",  ) 

      emit("new channel", {"errormessage":err_message}, broadcast=False)

@socketio.on("add message")
def addmessage(data):
    global channelclicked, messages, channeldict, channelset
    id = int(data["channelid"])
    message = data["message"]
    person = data["persononame"]
    print (f" id :  {id} ")
   
    foundchannel = None

    for x in channelset:
      print (f" channel: {x.channelname} ")
      print (f" channelid: {x.id} ")
      if x.id == id:
        print (f" found channel: {x.id} ")
        foundchannel = x
        break

    indkey = "channel" + str(x.id)
    foundchannel = channeldict[indkey]
    newMessage = Message(message, person, datetime.now() )
    #print (f" channel: {channel} ")
    if foundchannel is not None:
      print (f" found channel: {foundchannel.channelname} ")
      foundchannel.add_message(newMessage)
    
    #for mychannel in channel:
     # printf(f" mychannel: {mychannel}" )
     # mychannel.add_message(newMessage)
     # foundchannel = mychannel

    fullmessage =  person + "> " + newMessage.msgdate.strftime('%Y-%m-%d %H:%M:%S')  + "> " + newMessage.messageText 
   
    #print(f" message {fullmessage}  channelid {foundchannel.id}")
    emit("new message", {"fullmessage":fullmessage, "id": foundchannel.id}, broadcast=True)

    