import discord
from keep_alive import keep_alive

client = discord.Client()

def exists(user):
  with open('list.txt') as f:
      lines = f.readlines()
      user = user + "\n"
      if user in lines:
        return True
      return False

def remove(user):
  if exists(user):
    with open('list.txt', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        for i in lines:
          if i.strip("\n") != user:
            f.write(i)
        f.truncate()
  else:
    return -1

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return


  args = message.content.split()
  if args[0] == '.list':
    msg = "Here is the list:\n"
    with open('list.txt') as f:
      lines = f.readlines()
      for line in lines:
        msg += line
      await message.channel.send(msg)
  elif args[0] == ".help":
    await message.channel.send("Here are the commands:\n.help\n.list\n.add\n.remove")
  elif args[0] == '.add' and len(args) == 2:
    if exists(args[1]):
      await message.channel.send("This user is already in the list.")
    else:
      f = open("list.txt", "a+")
      f.write(args[1]+"\n")
      f.close()
      await message.channel.send("{user} has been added to the list.".format(user=str(args[1])))
  elif args[0] == '.remove' and len(args) == 2:
    if remove(str(args[1])) == -1:
      await message.channel.send("User is not in the list.")
      pass
    else:
      remove(str(args[1]))
      await message.channel.send("{user} has been removed from the list.".format(user=str(args[1]))) 
  elif args[0][0] == ".":
    await message.channel.send("Incorrect arguments.")
  else:
    pass

keep_alive()

client.run('ODA5ODg1Njk4MDIyNDQxMDAx.YCbm1Q.ZZ7269kqDqkbiPQdFflcGb3UVEs')
