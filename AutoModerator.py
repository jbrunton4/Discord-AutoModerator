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

def isValid(username:str) -> bool:

    for word in prohibited_words:
        if word.strip().lower() in username.strip().lower():
            return False

    return True

async def displaywarning(channel:discord.TextChannel, Desc:str = "", Fields:list = [], Footer:str = "") -> None:
    embed = discord.Embed(
        title = "WARNING",
        description = Desc,
        colour = discord.Colour.orange()
    )

    embed.set_footer(text=Footer)

    for x in Fields:
        embed.add_field(name = x[0], value=x[1], inline=True)

    await channel.send(embed=embed)

async def displayembed(channel:discord.TextChannel, Title:str = "", Desc:str = "", Fields:list = [], Footer:str = "") -> None:
    embed = discord.Embed(
        title = Title,
        description = Desc,
        colour = discord.Colour.blue()
    )

    embed.set_footer(text=Footer)

    for x in Fields:
        embed.add_field(name = x[0], value=x[1])

    await channel.send(embed=embed)


@client.event
async def on_member_join(member:discord.Member) -> None:
    if not isValid(member.display_name):
        await displaywarning(client.get_channel(AUTOMODCHANNELID), "Suspicious nickname detected",
                             [["`Nicknamed`", member.display_name],
                              ["`Truly`", member.name]])

    return

@client.event
async def on_member_update(before:discord.Member, after:discord.Member) -> None:
    if before.display_name != after.display_name and not isValid(after.display_name):
        await displaywarning(client.get_channel(AUTOMODCHANNELID), "Suspicious nickname detected", [["`Now`", after.display_name],
                                                                                                    ["`Formerly`", before.display_name],
                                                                                                    ["`Truly`", after.name]])

@client.event
async def on_ready() -> None:
    print("Ready")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Prefix: {cmd_prefix}"))


@client.event
async def on_message(message) -> None: # I don't know how to use discord.ext.Bot well enough
    global cmd_prefix
    global prohibited_words

    if message.content.lower().startswith(f"{cmd_prefix}help"):
        await displayembed(message.channel, "HELP", "Help menu for nickname checker", [["`help`", "Displays this menu"],
                                                                                        ["`setprefix [x]`", "Sets the command prefix to `[x]`"],
                                                                                        ["`prohibit [word]`", "Prohibits `[word]` in nicknames."],
                                                                                        ["`allow [word]`", "Remove `[word]` from prohibited words."]],
                                                                                        f"Reminder: The command prefix is `{cmd_prefix}`")

    elif message.content.lower().startswith(f"{cmd_prefix}setprefix "):

        old = cmd_prefix

        cmd_prefix = message.content.split()[1]
        fh = open("cmd_prefix.txt", "w")
        fh.write(cmd_prefix)
        fh.close()

        await displayembed(message.channel, "INFORMATION", "Command prefix changed", [["`From`", old],
                                                                                      ["`To`", cmd_prefix]])

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

        await displayembed(message.channel, "INFORMATION", "Added a new prohibited word", [["`New word`", message.content.replace(f'{cmd_prefix}prohibit', '')],
                                                                                      ["`Set by`", message.author.mention]])

        return

    elif message.content.lower().startswith(f"{cmd_prefix}allow "):

        fh = open("prohibited_words.txt", "r")
        old = fh.read()
        fh.close()

        new = old.replace(((message.content.replace(f"{cmd_prefix}allow ", "").strip()) + " "), "")

        fh = open("prohibited_words.txt", "w")
        fh.write(new)
        fh.close()

        await displayembed(message.channel, "INFORMATION", "Removed a prohibited word",
                           [["`Newly allowed word`", message.content.replace(f'{cmd_prefix}allow ', '')],
                            ["`Allowed by`", message.author.mention]])

        return


client.run(TOKEN)
