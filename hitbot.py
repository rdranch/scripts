import discord
from keep_alive import keep_alive

client = discord.Client()

def exists(user):
  user = user + "\n"
  with open('list.txt', 'r+') as f:
    return user in f.readlines()

def remove(user):
  with open('list.txt', 'r+') as f:
    user = user + "\n"
    lines = f.readlines()
    f.seek(0)
    f.truncate(0)
    lines.remove(user)
    f.writelines(lines)
        

def add(user):
  user = user + "\n"
  with open('list.txt', 'a+') as f:
    f.write(user)

def list():
  msg = "Here is the list:\n"
  with open('list.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
      msg += line
    return msg

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  args = message.content.split()
  if args[0] == '.list':
    msg = list()
    await message.channel.send(msg)
  elif args[0] == ".help":
    await message.channel.send("Here are the commands:\n.help\n.list\n.add\n.remove\n.search")
  elif args[0] == '.add' and len(args) == 2:
    if exists(args[1]):
      await message.channel.send("This user is already in the list.")
    else:
      add(args[1])
      await message.channel.send("{user} has been added to the list.".format(user=str(args[1])))
  elif args[0] == '.remove' and len(args) == 2:
    if exists(args[1]):
      remove(args[1])
      await message.channel.send("{user} has been removed from the list.".format(user=str(args[1])))
    else:
      await message.channel.send("User is not in the list.")
  elif args[0] == '.search' and len(args) == 2:
    if exists(args[1]):
      await message.channel.send("{user} is in the list.".format(user=str(args[1])))
    else:
      await message.channel.send("{user} is not in the list.".format(user=str(args[1])))
  elif args[0][0] == ".":
    await message.channel.send("Incorrect arguments.")
  else:
    await message.delete()

keep_alive()

client.run('ODA5ODg1Njk4MDIyNDQxMDAx.YCbm1Q.DDVbysy-Z2bgo3bLa_TujiBIbMU')
