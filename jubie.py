import os, os.path
import sys
import asyncio
import discord
asyncio.set_event_loop(asyncio.new_event_loop())
import aiohttp
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id)+') | Connected to '+str(len(client.guilds))+' servers | Connected to '+ str(len(set(client.get_all_members()))) +' users')
    print('--------')
    print("Discord.py verison: " + discord.__version__)
    #await client.change_presence(activity=discord.Game("Prepping some houseplants")) 

@client.event
async def on_raw_reaction_add(reaction):
    #get data
    emoji, messageid, channelid, user1=reaction.emoji, reaction.message_id, reaction.channel_id, reaction.user_id

    #pull message
    ch = client.get_channel(671167077930762250)
    channelis = client.get_channel(channelid)
    message = await channelis.fetch_message(messageid)

    if message.author.id == 671166284842663996:
        return # Prevent bot messages being blobbed

    #count votes
    num_votes=0
    for reaction in message.reactions:
        if emoji.id == 669391790901821450:
            num_votes= reaction.count
    #find the user that last blobbed a message and the original author
    user= client.get_user(user1)
    user0 = message.author
    guild = client.get_guild(624036526157987851)
    member=guild.get_member(user1)
    #send to blobboard
    if str(emoji) == "<:blob:669391790901821450>" and num_votes >= 3 and not ("snom" in str(message.reactions)) and channelid != 680496814361018429:
        embed=discord.Embed(title=message.content, color=0x3271a8, description="in #"+channelis.name)
        embed.set_author(name=str(user0), icon_url=user0.avatar_url)
        for attachment in message.attachments:
            embed.set_image(url=attachment.url)
        embed.set_footer(text="Blobbed by: " + str(user))
        try:
            await ch.send(embed=embed)
            await message.add_reaction("<:snom:670359030597943316")
        except:
            await channelis.send("<:jesswhy:666419794001657897> the message was too long to blob")
            await message.add_reaction("<:snom:670359030597943316")
    elif channelid==680496814361018429:
        if messageid == 680501120988086277:
            role=guild.get_role(680498313988276244)
            await member.add_roles(role)

    notifsquad=0
    if channelid == 680496814361018429:
        for reaction in message.reactions:
            notifsquad+=reaction.count
    await client.change_presence(activity=discord.Game("Got " + str(notifsquad) + " members in the notification squad")) 

@client.event
async def on_raw_reaction_remove(reaction):
    emoji, messageid, channelid, user1=reaction.emoji, reaction.message_id, reaction.channel_id, reaction.user_id
    guild = client.get_guild(624036526157987851)
    member=guild.get_member(user1)
    if channelid==680496814361018429:
        if messageid == 680501120988086277:
            role=guild.get_role(680498313988276244)
            await member.remove_roles(role)

    notifsquad=0
    ch = client.get_channel(680496814361018429)
    message = await ch.fetch_message(680501120988086277)
    for reaction in message.reactions:
        notifsquad+=reaction.count
    await client.change_presence(activity=discord.Game("Got " + str(notifsquad) + " members in the notification squad")) 

client.run("heck you, get your own token.")