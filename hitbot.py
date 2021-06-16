import discord
from keep_alive import keep_alive

# make non -case sensitive

client = discord.Client()


def add(last_message, user):
  s = ""
  try:
    new_lst = last_message.split("\n")
    new_lst.append(user)
    for n in new_lst:
      s += (n + "\n")
    return s
  except:
    return user

def remove(last_message, user):
  s = ""
  if len(last_message) <= 1 or last_message == "> Cannot remove last item in list.":
    return False
  new_lst = last_message.split("\n")
  if user in new_lst:
    new_lst.remove(user)
    for n in new_lst:
      s += (n + "\n")
    return s
  else:
    return None

def search(last_message, user):
  try:
    new_lst = last_message.split("\n")
    print(user + " " + user in new_lst)
    return (user in new_lst)
  except:
    return False

def help():
  return "> Here are the commands:\n.help - Pulls this page\n.add [user] - Add a specific user to the list\n.remove [user] - Removes a user from the list\n.search [user] - Searches for a user in the list."

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  last_message = await message.channel.history(limit=2).flatten()
  
  try:
    last_message = last_message[1].content
  except IndexError:
    pass
  if message.author == client.user:
    return

  args = message.content.split()
  if (len(args) > 2):
    await message.channel.purge(limit=10)
    await message.channel.send("> There cannot be spaces in usernames.")
    await message.channel.send(last_message)
  elif args[0].lower() == ".help":
    await message.channel.purge(limit=10)
    await message.channel.send(help())
    await message.channel.send(last_message)
  elif args[0].lower() == ".add":
    await message.channel.purge(limit=10)
    if search(last_message, args[1]):
      await message.channel.send(f"> {args[1]} already exists in list.")
      if len(last_message) > 1:
        await message.channel.send(last_message)
      else: pass
    else:
      await message.channel.send(add(last_message, args[1]))
  elif args[0].lower() == ".remove":
    rm = remove(last_message, args[1])
    await message.channel.purge(limit=10)
    if rm is None:
      await message.channel.send(f"> {args[1]} not in list.")
      await message.channel.send(last_message)
    elif rm == False:
      pass
    else:
      await message.channel.send(rm)
  elif args[0].lower() == ".search":
    result = search(last_message, args[1])
    await message.channel.purge(limit=10)
    if result:
      await message.channel.send(f"> {args[1]} is in list.")
      await message.channel.send(last_message)
    else:
      await message.channel.send(f"> {args[1]} not in list.")
      await message.channel.send(last_message)
  else:
    await message.delete()

keep_alive()

client.run('{ redacted }')
