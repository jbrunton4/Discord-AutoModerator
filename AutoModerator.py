"""
READ THIS FIRST:
You will need to change the values of TOKEN and AUTOMODCHANNELID, as well as set up a channel that only admins can view
and turn on notifs for it. Alternatively you could add a ping to the message that is sent when a nickname is flagged.

Also create a cmd_prefix.txt and a prohibited_words.txt file.

Make any changes you want (e.g. if you run it using an existing bot you might want to remove the activity change).
"""

import discord

fh = open("cmd_prefix.txt", "r")
cmd_prefix = fh.read()
if cmd_prefix == "":
    cmd_prefix = "!"
    fh = open("cmd_prefix.txt", "w")
    fh.write(cmd_prefix)
    fh.close()
fh.close()

fh = open("prohibited_words.txt", "r")
prohibited_words = fh.read().split()
fh.close()

TOKEN = ""
AUTOMODCHANNELID = 0

client = discord.Client()


@client.event
async def on_member_join(member) -> None:
    for word in prohibited_words:
        if word.strip().lower() in member.display_name.strip().lower():
            await client.get_channel(AUTOMODCHANNELID).send(f"Suspicious nickname detected: {member.mention}")

    return

@client.event
async def on_ready() -> None:
    print("Ready")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Prefix: {cmd_prefix}"))

@client.event
async def on_message(message) -> None: # I don't know how to use discord.ext.Bot well enough
    global cmd_prefix
    global prohibited_words

    if message.content.lower().startswith(f"{cmd_prefix}setprefix "):
        cmd_prefix = message.content.split()[1]
        fh = open("cmd_prefix.txt", "w")
        fh.write(cmd_prefix)
        fh.close()

        await message.channel.send(f"Set prefix to {cmd_prefix}")
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Prefix: {cmd_prefix}"))

        return

    elif message.content.lower().startswith(f"{cmd_prefix}prohibit "):
        prohibited_words.append(message.content.replace(f"{cmd_prefix}prohibit", ""))

        fh = open("prohibited_words.txt", "a")
        fh.write(f"{message.content.replace(f'{cmd_prefix}prohibit', '')} ")
        fh.close()

        fh = open("prohibited_words.txt", "r")
        prohibited_words = fh.read().split()
        fh.close()

        await message.channel.send(f"Added {message.content.replace(f'{cmd_prefix}prohibit', '')} to prohibited words.")

        return

client.run(TOKEN)
