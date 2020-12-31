# A Discord Bot that detects messages in a Discord channel that may indicate that the sender is sad or depressed, and replies with motivational/encouraging messages.

import discord
import os
import requests
import json
import random
from replit import db 
from keep_alive import keep_alive

client = discord.Client()

#a list of words to watch out for
sad_words = ["sad","pain","unhappy","upset","miserable"]

#a list of extreme words that may indicate that the sender of the message is feeling certain urges and may require help
flag_words = ["depressing","kms","depressed","kill myself","suicide","suicidial","i want to die","i wanna die","depressin","kill my self"]

#standard messages to reply with when the user sends a word from sad_words in the chat
starter_encouragements = [
  "You're trying the best you can, hang in there buddy :)",
  "You're a great person, don't let anything diminish that!",
  "The people around you love you, they all just have different ways of showing it."
]

if "responding" not in db.keys():
  db["responding"] = True

# lets us update the database of encouraging messages the user can receive
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

# deletes an encouraging message at a certain index in the list of encouraging messages
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if (len(encouragements) > index):
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # if the bot is on, then it will respond to sad words in messages
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    # if a message contains any of the key words, it'll send any random message from the list of messages.
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  # if a message contains serious words that may cause a red flag, then the bot will notice and output a specific message with links to phone numbers that you can text/call to help
  if any(word.lower() in msg for word in flag_words):
    await message.channel.send("If you're in need of immediate help, please reach out to a friend or a loved one, or text the Crisis Text Line at 686868. You're not alone in your struggle and there's people that care about you, so please get help if you feel that you need it. You can visit the link below for more resources:" + "\n" + " https://windsoressex.cmha.ca/mental-health/suicide-prevention/awareness-month/get-help/")

  # a command that adds the ability to add a user inputted messages to the list of messages
  if msg.startswith("$addmsg"):
    encouraging_message = msg.split("$addmsg ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouragment added!")

  # a command that adds the ability to delete a user inputted message that have been added by users in the channel.
  if msg.startswith("$delmsg"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("delmsg", 1)[1]) - 1
      delete_encouragement(index)
      encouragements = db["encouragements"]
      lst = ""
      for i in range(len(encouragements)):
        lst += str(i+1) + ". " + encouragements[i] + "\n"
      if len(encouragements) == 0:
        await message.channel.send("There are no user added messages.")
      elif len(encouragements) < index:
        await message.channel.send("There is no message at the number given.")
      else:
        await message.channel.send("The user added messages are:" + "\n" + lst)

  # a command that returns the list of possible motivational/encouraging messages that have been added by users in the channel.
  if msg.lower() == ("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      lst = ""
      for i in range(len(encouragements)):
        lst += str(i+1)+ ". " + encouragements[i] + "\n"
      if lst == "":
        message.channel.send("There are no user added messages.")
    await message.channel.send("The user added messages are:" + "\n" + lst)

  # a command that gives us the ability to turn off the bot responding to possible sad messages
  if msg.lower() == "$responding-off":
      db["responding"] = False
      await message.channel.send("Responding is off!")

  # a command that gives us the ability to turn on the bot responding to possible sad messages
  if msg.lower() == "$responding-on":
      db["responding"] = True
      await message.channel.send("Responding is on!")

  # a command that gives a list of all commands
  if msg == "$commands":
    await message.channel.send("The commands are: " + "\n" + "1. '$responding-on' turns on the ability for the to respond to messages." + "\n" + "2. '$responding-off' turns off the ability for the bot to respond to messages." + "\n" + "3. '$addmsg' lets users add motivational/encouraging messages to the bot." + "\n" + "4. '$delmsg' lets users delete motivational/encouraging messages from the bot by inputting the number of the message they want to delete." + "\n" + "5. '$list' displays all the user added messages.")

keep_alive()
client.run(os.getenv('TOKEN')) #gets our bot token from an environmental variable
# the above command just runs our bot with the the Bot Token that we get from the Discord Developer Portal
